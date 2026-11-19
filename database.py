"""
KaushalSetu - Database & Persistence Layer
Supports SQLite with seamless automatic JSON fallback if Windows Application Control blocks DLLs in sandboxed environments.
"""

import os
import json
import copy
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DB_PATH = os.path.join(DATA_DIR, "kaushalsetu.db")
JSON_STORE_PATH = os.path.join(DATA_DIR, "kaushalsetu_store.json")

# Test whether SQLite3 and its underlying C DLLs are allowed by system policy
USE_SQLITE = False
try:
    import sqlite3
    _test_conn = sqlite3.connect(":memory:")
    _test_conn.execute("CREATE TABLE _t (id INT)")
    _test_conn.close()
    USE_SQLITE = True
except Exception as e:
    USE_SQLITE = False


class DictRow(dict):
    """Row object accessible both via key index and dict operations."""
    def __getitem__(self, key):
        return super().get(key, None)


# -------------------------------------------------------------
# JSON File Storage Backend (Resilient Sandbox Fallback)
# -------------------------------------------------------------
def _load_json_store():
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(JSON_STORE_PATH):
        initial = {
            "workers": [],
            "experiences": [],
            "ai_mappings": [],
            "practical_assessments": []
        }
        with open(JSON_STORE_PATH, "w", encoding="utf-8") as f:
            json.dump(initial, f, indent=2)
        return initial
    try:
        with open(JSON_STORE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"workers": [], "experiences": [], "ai_mappings": [], "practical_assessments": []}


def _save_json_store(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(JSON_STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


# -------------------------------------------------------------
# SQLite Storage Backend
# -------------------------------------------------------------
def get_db_connection():
    if not USE_SQLITE:
        return None
    conn = sqlite3.connect(DB_PATH, timeout=10.0)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(DATA_DIR, exist_ok=True)
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS workers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            mobile TEXT NOT NULL,
            email TEXT,
            aadhaar_masked TEXT,
            state TEXT,
            district TEXT,
            preferred_language TEXT DEFAULT 'Hindi',
            trade TEXT NOT NULL,
            years_experience INTEGER DEFAULT 1,
            prior_education TEXT,
            status TEXT DEFAULT 'Registered',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER NOT NULL,
            experience_text TEXT NOT NULL,
            input_method TEXT DEFAULT 'text',
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ai_mappings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER NOT NULL UNIQUE,
            experience_id INTEGER,
            qp_code TEXT NOT NULL,
            qp_name TEXT NOT NULL,
            overall_confidence REAL NOT NULL,
            readiness_level TEXT,
            competency_results_json TEXT NOT NULL,
            tools_identified_json TEXT,
            suggested_json TEXT,
            gaps_json TEXT,
            is_overridden INTEGER DEFAULT 0,
            assessor_override_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS practical_assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            worker_id INTEGER NOT NULL UNIQUE,
            assessor_name TEXT NOT NULL,
            assessor_id TEXT NOT NULL,
            assessment_date TEXT NOT NULL,
            checklist_scores_json TEXT NOT NULL,
            practical_score REAL NOT NULL,
            viva_score REAL NOT NULL,
            safety_score REAL NOT NULL,
            overall_score REAL NOT NULL,
            assessor_comments TEXT,
            evidence_notes TEXT,
            decision TEXT NOT NULL,
            bridge_training_modules TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)
        conn.commit()
        conn.close()
    else:
        _load_json_store()


def seed_demo_data():
    """Populate realistic candidate pipelines for hackathon evaluation."""
    from rpl_data import SAMPLE_EXPERIENCES
    from ai_engine import analyze_worker_experience

    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM workers")
        count = cursor.fetchone()[0]
        if count == 0:
            # Ramesh Kumar
            cursor.execute("""
                INSERT INTO workers (name, mobile, email, aadhaar_masked, state, district, preferred_language, trade, years_experience, prior_education, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Certified', '2026-11-10 10:30:00')
            """, ("Ramesh Kumar", "9876543210", "ramesh@example.com", "XXXX-XXXX-4589", "Uttar Pradesh", "Varanasi", "Hindi", "electrician", 6, "10th Standard"))
            w1_id = cursor.lastrowid
            
            exp_text_1 = SAMPLE_EXPERIENCES["electrician"]
            cursor.execute("INSERT INTO experiences (worker_id, experience_text, input_method, submitted_at) VALUES (?, ?, 'voice', '2026-11-10 11:15:00')", (w1_id, exp_text_1))
            exp1_id = cursor.lastrowid

            an1 = analyze_worker_experience("electrician", exp_text_1, 6)
            cursor.execute("""
                INSERT INTO ai_mappings (worker_id, experience_id, qp_code, qp_name, overall_confidence, readiness_level, competency_results_json, tools_identified_json, suggested_json, gaps_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (w1_id, exp1_id, an1["qp_code"], an1["qp_name"], an1["overall_confidence"], an1["readiness_level"], json.dumps(an1["competency_results"]), json.dumps(an1["tools_identified"]), json.dumps(an1["suggested_competencies"]), json.dumps(an1["bridge_training_needed"])))

            ch1 = {"ELE/N6001": 85, "ELE/N6002": 90, "ELE/N6003": 88, "ELE/N6004": 82, "ELE/N9901": 92}
            cursor.execute("""
                INSERT INTO practical_assessments (worker_id, assessor_name, assessor_id, assessment_date, checklist_scores_json, practical_score, viva_score, safety_score, overall_score, assessor_comments, evidence_notes, decision, bridge_training_modules)
                VALUES (?, 'Dr. Arvind Mehta', 'ESSCI-ASSESS-8842', '2026-11-15', ?, 88.0, 85.0, 92.0, 88.2, 'Candidate displayed exemplary mastery in conduit wiring and safety.', 'Demonstrated live distribution board installation with RCCB.', 'Competent', '')
            """, (w1_id, json.dumps(ch1)))

            # Priya Sharma
            cursor.execute("""
                INSERT INTO workers (name, mobile, email, aadhaar_masked, state, district, preferred_language, trade, years_experience, prior_education, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'AI Analyzed', '2026-11-14 09:20:00')
            """, ("Priya Sharma", "9812345678", "priya@example.com", "XXXX-XXXX-9912", "Maharashtra", "Pune", "Marathi / Hindi", "plumber", 5, "8th Standard"))
            w2_id = cursor.lastrowid
            exp_text_2 = SAMPLE_EXPERIENCES["plumber"]
            cursor.execute("INSERT INTO experiences (worker_id, experience_text, input_method) VALUES (?, ?, 'text')", (w2_id, exp_text_2))
            exp2_id = cursor.lastrowid
            an2 = analyze_worker_experience("plumber", exp_text_2, 5)
            cursor.execute("""
                INSERT INTO ai_mappings (worker_id, experience_id, qp_code, qp_name, overall_confidence, readiness_level, competency_results_json, tools_identified_json, suggested_json, gaps_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (w2_id, exp2_id, an2["qp_code"], an2["qp_name"], an2["overall_confidence"], an2["readiness_level"], json.dumps(an2["competency_results"]), json.dumps(an2["tools_identified"]), json.dumps(an2["suggested_competencies"]), json.dumps(an2["bridge_training_needed"])))

            # Manoj Verma
            cursor.execute("""
                INSERT INTO workers (name, mobile, email, aadhaar_masked, state, district, preferred_language, trade, years_experience, prior_education, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'AI Analyzed', '2026-11-17 14:10:00')
            """, ("Manoj Verma", "9765432109", "manoj@example.com", "XXXX-XXXX-3341", "Madhya Pradesh", "Indore", "Hindi", "automotive", 4, "10th Standard"))
            w3_id = cursor.lastrowid
            exp_text_3 = SAMPLE_EXPERIENCES["automotive"]
            cursor.execute("INSERT INTO experiences (worker_id, experience_text, input_method) VALUES (?, ?, 'text')", (w3_id, exp_text_3))
            exp3_id = cursor.lastrowid
            an3 = analyze_worker_experience("automotive", exp_text_3, 4)
            cursor.execute("""
                INSERT INTO ai_mappings (worker_id, experience_id, qp_code, qp_name, overall_confidence, readiness_level, competency_results_json, tools_identified_json, suggested_json, gaps_json)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (w3_id, exp3_id, an3["qp_code"], an3["qp_name"], an3["overall_confidence"], an3["readiness_level"], json.dumps(an3["competency_results"]), json.dumps(an3["tools_identified"]), json.dumps(an3["suggested_competencies"]), json.dumps(an3["bridge_training_needed"])))

            # Sunita Devi
            cursor.execute("""
                INSERT INTO workers (name, mobile, email, aadhaar_masked, state, district, preferred_language, trade, years_experience, prior_education, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Registered', '2026-11-18 16:45:00')
            """, ("Sunita Devi", "9654321987", "sunita@example.com", "XXXX-XXXX-7721", "Rajasthan", "Jaipur", "Hindi", "tailor", 3, "Non-Formal"))

            conn.commit()
            conn.close()
    else:
        # JSON Storage Seed
        store = _load_json_store()
        if len(store["workers"]) == 0:
            # Ramesh Kumar
            w1 = {
                "id": 1, "name": "Ramesh Kumar", "mobile": "9876543210", "email": "ramesh@example.com",
                "aadhaar_masked": "XXXX-XXXX-4589", "state": "Uttar Pradesh", "district": "Varanasi",
                "preferred_language": "Hindi", "trade": "electrician", "years_experience": 6,
                "prior_education": "10th Standard", "status": "Certified", "created_at": "2026-11-10 10:30:00"
            }
            exp_text_1 = SAMPLE_EXPERIENCES["electrician"]
            an1 = analyze_worker_experience("electrician", exp_text_1, 6)
            store["workers"].append(w1)
            store["experiences"].append({
                "id": 1, "worker_id": 1, "experience_text": exp_text_1, "input_method": "voice", "submitted_at": "2026-11-10 11:15:00"
            })
            store["ai_mappings"].append({
                "id": 1, "worker_id": 1, "experience_id": 1, "qp_code": an1["qp_code"], "qp_name": an1["qp_name"],
                "overall_confidence": an1["overall_confidence"], "readiness_level": an1["readiness_level"],
                "competency_results_json": json.dumps(an1["competency_results"]),
                "tools_identified_json": json.dumps(an1["tools_identified"]),
                "suggested_json": json.dumps(an1["suggested_competencies"]),
                "gaps_json": json.dumps(an1["bridge_training_needed"]),
                "is_overridden": 0, "assessor_override_notes": "", "created_at": "2026-11-10 11:20:00"
            })
            store["practical_assessments"].append({
                "id": 1, "worker_id": 1, "assessor_name": "Dr. Arvind Mehta", "assessor_id": "ESSCI-ASSESS-8842",
                "assessment_date": "2026-11-15",
                "checklist_scores_json": json.dumps({"ELE/N6001": 85, "ELE/N6002": 90, "ELE/N6003": 88, "ELE/N6004": 82, "ELE/N9901": 92}),
                "practical_score": 88.0, "viva_score": 85.0, "safety_score": 92.0, "overall_score": 88.2,
                "assessor_comments": "Candidate displayed exemplary mastery in conduit wiring and safety.",
                "evidence_notes": "Demonstrated live distribution board installation with RCCB at Varanasi Training Centre.",
                "decision": "Competent", "bridge_training_modules": "", "created_at": "2026-11-15 15:30:00"
            })

            # Priya Sharma
            w2 = {
                "id": 2, "name": "Priya Sharma", "mobile": "9812345678", "email": "priya@example.com",
                "aadhaar_masked": "XXXX-XXXX-9912", "state": "Maharashtra", "district": "Pune",
                "preferred_language": "Marathi / Hindi", "trade": "plumber", "years_experience": 5,
                "prior_education": "8th Standard", "status": "AI Analyzed", "created_at": "2026-11-14 09:20:00"
            }
            exp_text_2 = SAMPLE_EXPERIENCES["plumber"]
            an2 = analyze_worker_experience("plumber", exp_text_2, 5)
            store["workers"].append(w2)
            store["experiences"].append({
                "id": 2, "worker_id": 2, "experience_text": exp_text_2, "input_method": "text", "submitted_at": "2026-11-14 10:00:00"
            })
            store["ai_mappings"].append({
                "id": 2, "worker_id": 2, "experience_id": 2, "qp_code": an2["qp_code"], "qp_name": an2["qp_name"],
                "overall_confidence": an2["overall_confidence"], "readiness_level": an2["readiness_level"],
                "competency_results_json": json.dumps(an2["competency_results"]),
                "tools_identified_json": json.dumps(an2["tools_identified"]),
                "suggested_json": json.dumps(an2["suggested_competencies"]),
                "gaps_json": json.dumps(an2["bridge_training_needed"]),
                "is_overridden": 0, "assessor_override_notes": "", "created_at": "2026-11-14 10:05:00"
            })

            # Manoj Verma
            w3 = {
                "id": 3, "name": "Manoj Verma", "mobile": "9765432109", "email": "manoj@example.com",
                "aadhaar_masked": "XXXX-XXXX-3341", "state": "Madhya Pradesh", "district": "Indore",
                "preferred_language": "Hindi", "trade": "automotive", "years_experience": 4,
                "prior_education": "10th Standard", "status": "AI Analyzed", "created_at": "2026-11-17 14:10:00"
            }
            exp_text_3 = SAMPLE_EXPERIENCES["automotive"]
            an3 = analyze_worker_experience("automotive", exp_text_3, 4)
            store["workers"].append(w3)
            store["experiences"].append({
                "id": 3, "worker_id": 3, "experience_text": exp_text_3, "input_method": "text", "submitted_at": "2026-11-17 14:35:00"
            })
            store["ai_mappings"].append({
                "id": 3, "worker_id": 3, "experience_id": 3, "qp_code": an3["qp_code"], "qp_name": an3["qp_name"],
                "overall_confidence": an3["overall_confidence"], "readiness_level": an3["readiness_level"],
                "competency_results_json": json.dumps(an3["competency_results"]),
                "tools_identified_json": json.dumps(an3["tools_identified"]),
                "suggested_json": json.dumps(an3["suggested_competencies"]),
                "gaps_json": json.dumps(an3["bridge_training_needed"]),
                "is_overridden": 0, "assessor_override_notes": "", "created_at": "2026-11-17 14:40:00"
            })

            # Sunita Devi
            w4 = {
                "id": 4, "name": "Sunita Devi", "mobile": "9654321987", "email": "sunita@example.com",
                "aadhaar_masked": "XXXX-XXXX-7721", "state": "Rajasthan", "district": "Jaipur",
                "preferred_language": "Hindi", "trade": "tailor", "years_experience": 3,
                "prior_education": "Non-Formal", "status": "Registered", "created_at": "2026-11-18 16:45:00"
            }
            store["workers"].append(w4)

            _save_json_store(store)


# -------------------------------------------------------------
# Unified Query Functions
# -------------------------------------------------------------
def create_worker(name, mobile, email, state, district, preferred_language, trade, years_experience, prior_education, aadhaar_masked=""):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO workers (name, mobile, email, state, district, preferred_language, trade, years_experience, prior_education, aadhaar_masked, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Registered')
        """, (name, mobile, email, state, district, preferred_language, trade, years_experience, prior_education, aadhaar_masked))
        worker_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return worker_id
    else:
        store = _load_json_store()
        new_id = max([w["id"] for w in store["workers"]], default=0) + 1
        worker = {
            "id": new_id, "name": name, "mobile": mobile, "email": email, "state": state,
            "district": district, "preferred_language": preferred_language, "trade": trade,
            "years_experience": years_experience, "prior_education": prior_education,
            "aadhaar_masked": aadhaar_masked, "status": "Registered",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        store["workers"].append(worker)
        _save_json_store(store)
        return new_id


def get_worker(worker_id):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM workers WHERE id = ?", (worker_id,))
        worker = cursor.fetchone()
        conn.close()
        return DictRow(dict(worker)) if worker else None
    else:
        store = _load_json_store()
        for w in store["workers"]:
            if w["id"] == worker_id:
                return DictRow(w)
        return None


def get_all_workers(trade_filter=None, status_filter=None, search_query=None):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT w.*, 
                   m.overall_confidence, m.readiness_level,
                   p.decision as practical_decision, p.overall_score as final_score
            FROM workers w
            LEFT JOIN ai_mappings m ON w.id = m.worker_id
            LEFT JOIN practical_assessments p ON w.id = p.worker_id
            WHERE 1=1
        """
        params = []
        if trade_filter and trade_filter != "all":
            query += " AND w.trade = ?"
            params.append(trade_filter)
        if status_filter and status_filter != "all":
            query += " AND w.status = ?"
            params.append(status_filter)
        if search_query:
            query += " AND (w.name LIKE ? OR w.mobile LIKE ? OR w.district LIKE ?)"
            term = f"%{search_query}%"
            params.extend([term, term, term])

        query += " ORDER BY w.id DESC"
        cursor.execute(query, params)
        rows = [DictRow(dict(r)) for r in cursor.fetchall()]
        conn.close()
        return rows
    else:
        store = _load_json_store()
        results = []
        for w in store["workers"]:
            if trade_filter and trade_filter != "all" and w["trade"] != trade_filter:
                continue
            if status_filter and status_filter != "all" and w["status"] != status_filter:
                continue
            if search_query:
                sq = search_query.lower()
                name_match = sq in w["name"].lower()
                mob_match = sq in w["mobile"]
                dist_match = sq in (w.get("district") or "").lower()
                if not (name_match or mob_match or dist_match):
                    continue

            row = copy.deepcopy(w)
            # Find AI mapping
            mapping = next((m for m in store["ai_mappings"] if m["worker_id"] == w["id"]), None)
            if mapping:
                row["overall_confidence"] = mapping.get("overall_confidence")
                row["readiness_level"] = mapping.get("readiness_level")
            else:
                row["overall_confidence"] = None
                row["readiness_level"] = None

            # Find practical assessment
            assessment = next((p for p in store["practical_assessments"] if p["worker_id"] == w["id"]), None)
            if assessment:
                row["practical_decision"] = assessment.get("decision")
                row["final_score"] = assessment.get("overall_score")
            else:
                row["practical_decision"] = None
                row["final_score"] = None

            results.append(DictRow(row))

        results.sort(key=lambda x: x["id"], reverse=True)
        return results


def save_worker_experience(worker_id, experience_text, input_method="text"):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO experiences (worker_id, experience_text, input_method)
            VALUES (?, ?, ?)
        """, (worker_id, experience_text, input_method))
        exp_id = cursor.lastrowid
        cursor.execute("UPDATE workers SET status = 'Experience Submitted' WHERE id = ?", (worker_id,))
        conn.commit()
        conn.close()
        return exp_id
    else:
        store = _load_json_store()
        new_id = max([e["id"] for e in store["experiences"]], default=0) + 1
        store["experiences"].append({
            "id": new_id, "worker_id": worker_id, "experience_text": experience_text,
            "input_method": input_method, "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        for w in store["workers"]:
            if w["id"] == worker_id:
                w["status"] = "Experience Submitted"
        _save_json_store(store)
        return new_id


def get_worker_experience(worker_id):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM experiences WHERE worker_id = ? ORDER BY id DESC LIMIT 1", (worker_id,))
        exp = cursor.fetchone()
        conn.close()
        return DictRow(dict(exp)) if exp else None
    else:
        store = _load_json_store()
        for e in reversed(store["experiences"]):
            if e["worker_id"] == worker_id:
                return DictRow(e)
        return None


def save_ai_mapping(worker_id, exp_id, analysis_result):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM ai_mappings WHERE worker_id = ?", (worker_id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("""
                UPDATE ai_mappings
                SET experience_id = ?, qp_code = ?, qp_name = ?, overall_confidence = ?,
                    readiness_level = ?, competency_results_json = ?, tools_identified_json = ?,
                    suggested_json = ?, gaps_json = ?, created_at = CURRENT_TIMESTAMP
                WHERE worker_id = ?
            """, (
                exp_id, analysis_result["qp_code"], analysis_result["qp_name"],
                analysis_result["overall_confidence"], analysis_result["readiness_level"],
                json.dumps(analysis_result["competency_results"]),
                json.dumps(analysis_result["tools_identified"]),
                json.dumps(analysis_result["suggested_competencies"]),
                json.dumps(analysis_result["bridge_training_needed"]),
                worker_id
            ))
        else:
            cursor.execute("""
                INSERT INTO ai_mappings (
                    worker_id, experience_id, qp_code, qp_name, overall_confidence,
                    readiness_level, competency_results_json, tools_identified_json,
                    suggested_json, gaps_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                worker_id, exp_id, analysis_result["qp_code"], analysis_result["qp_name"],
                analysis_result["overall_confidence"], analysis_result["readiness_level"],
                json.dumps(analysis_result["competency_results"]),
                json.dumps(analysis_result["tools_identified"]),
                json.dumps(analysis_result["suggested_competencies"]),
                json.dumps(analysis_result["bridge_training_needed"])
            ))
        cursor.execute("UPDATE workers SET status = 'AI Analyzed' WHERE id = ? AND status IN ('Registered', 'Experience Submitted')", (worker_id,))
        conn.commit()
        conn.close()
    else:
        store = _load_json_store()
        entry = next((m for m in store["ai_mappings"] if m["worker_id"] == worker_id), None)
        if entry:
            entry["experience_id"] = exp_id
            entry["qp_code"] = analysis_result["qp_code"]
            entry["qp_name"] = analysis_result["qp_name"]
            entry["overall_confidence"] = analysis_result["overall_confidence"]
            entry["readiness_level"] = analysis_result["readiness_level"]
            entry["competency_results_json"] = json.dumps(analysis_result["competency_results"])
            entry["tools_identified_json"] = json.dumps(analysis_result["tools_identified"])
            entry["suggested_json"] = json.dumps(analysis_result["suggested_competencies"])
            entry["gaps_json"] = json.dumps(analysis_result["bridge_training_needed"])
        else:
            new_id = max([m["id"] for m in store["ai_mappings"]], default=0) + 1
            store["ai_mappings"].append({
                "id": new_id, "worker_id": worker_id, "experience_id": exp_id,
                "qp_code": analysis_result["qp_code"], "qp_name": analysis_result["qp_name"],
                "overall_confidence": analysis_result["overall_confidence"],
                "readiness_level": analysis_result["readiness_level"],
                "competency_results_json": json.dumps(analysis_result["competency_results"]),
                "tools_identified_json": json.dumps(analysis_result["tools_identified"]),
                "suggested_json": json.dumps(analysis_result["suggested_competencies"]),
                "gaps_json": json.dumps(analysis_result["bridge_training_needed"]),
                "is_overridden": 0, "assessor_override_notes": "",
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        for w in store["workers"]:
            if w["id"] == worker_id and w["status"] in ("Registered", "Experience Submitted"):
                w["status"] = "AI Analyzed"
        _save_json_store(store)


def get_ai_mapping(worker_id):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM ai_mappings WHERE worker_id = ?", (worker_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            data = DictRow(dict(row))
            data["competency_results"] = json.loads(data["competency_results_json"])
            data["tools_identified"] = json.loads(data["tools_identified_json"] or "[]")
            data["suggested_competencies"] = json.loads(data["suggested_json"] or "[]")
            data["bridge_training_needed"] = json.loads(data["gaps_json"] or "[]")
            return data
        return None
    else:
        store = _load_json_store()
        for m in store["ai_mappings"]:
            if m["worker_id"] == worker_id:
                data = DictRow(copy.deepcopy(m))
                data["competency_results"] = json.loads(data["competency_results_json"])
                data["tools_identified"] = json.loads(data.get("tools_identified_json") or "[]")
                data["suggested_competencies"] = json.loads(data.get("suggested_json") or "[]")
                data["bridge_training_needed"] = json.loads(data.get("gaps_json") or "[]")
                return data
        return None


def update_ai_override(worker_id, override_notes):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE ai_mappings SET is_overridden = 1, assessor_override_notes = ? WHERE worker_id = ?", (override_notes, worker_id))
        conn.commit()
        conn.close()
    else:
        store = _load_json_store()
        for m in store["ai_mappings"]:
            if m["worker_id"] == worker_id:
                m["is_overridden"] = 1
                m["assessor_override_notes"] = override_notes
        _save_json_store(store)


def save_practical_assessment(worker_id, assessor_name, assessor_id, assessment_date,
                              checklist_scores, practical_score, viva_score, safety_score,
                              overall_score, assessor_comments, evidence_notes, decision, bridge_modules=""):
    new_status = "Certified" if decision == "Competent" else ("Needs Bridge Training" if decision == "Needs Bridge Training" else "Assessment Rejected")

    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM practical_assessments WHERE worker_id = ?", (worker_id,))
        existing = cursor.fetchone()
        if existing:
            cursor.execute("""
                UPDATE practical_assessments
                SET assessor_name = ?, assessor_id = ?, assessment_date = ?,
                    checklist_scores_json = ?, practical_score = ?, viva_score = ?,
                    safety_score = ?, overall_score = ?, assessor_comments = ?,
                    evidence_notes = ?, decision = ?, bridge_training_modules = ?
                WHERE worker_id = ?
            """, (
                assessor_name, assessor_id, assessment_date,
                json.dumps(checklist_scores), practical_score, viva_score,
                safety_score, overall_score, assessor_comments,
                evidence_notes, decision, bridge_modules, worker_id
            ))
        else:
            cursor.execute("""
                INSERT INTO practical_assessments (
                    worker_id, assessor_name, assessor_id, assessment_date,
                    checklist_scores_json, practical_score, viva_score,
                    safety_score, overall_score, assessor_comments,
                    evidence_notes, decision, bridge_training_modules
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                worker_id, assessor_name, assessor_id, assessment_date,
                json.dumps(checklist_scores), practical_score, viva_score,
                safety_score, overall_score, assessor_comments,
                evidence_notes, decision, bridge_modules
            ))
        cursor.execute("UPDATE workers SET status = ? WHERE id = ?", (new_status, worker_id))
        conn.commit()
        conn.close()
    else:
        store = _load_json_store()
        entry = next((p for p in store["practical_assessments"] if p["worker_id"] == worker_id), None)
        if entry:
            entry["assessor_name"] = assessor_name
            entry["assessor_id"] = assessor_id
            entry["assessment_date"] = assessment_date
            entry["checklist_scores_json"] = json.dumps(checklist_scores)
            entry["practical_score"] = practical_score
            entry["viva_score"] = viva_score
            entry["safety_score"] = safety_score
            entry["overall_score"] = overall_score
            entry["assessor_comments"] = assessor_comments
            entry["evidence_notes"] = evidence_notes
            entry["decision"] = decision
            entry["bridge_training_modules"] = bridge_modules
        else:
            new_id = max([p["id"] for p in store["practical_assessments"]], default=0) + 1
            store["practical_assessments"].append({
                "id": new_id, "worker_id": worker_id, "assessor_name": assessor_name,
                "assessor_id": assessor_id, "assessment_date": assessment_date,
                "checklist_scores_json": json.dumps(checklist_scores),
                "practical_score": practical_score, "viva_score": viva_score,
                "safety_score": safety_score, "overall_score": overall_score,
                "assessor_comments": assessor_comments, "evidence_notes": evidence_notes,
                "decision": decision, "bridge_training_modules": bridge_modules,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
        for w in store["workers"]:
            if w["id"] == worker_id:
                w["status"] = new_status
        _save_json_store(store)


def get_practical_assessment(worker_id):
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM practical_assessments WHERE worker_id = ?", (worker_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            data = DictRow(dict(row))
            data["checklist_scores"] = json.loads(data["checklist_scores_json"])
            return data
        return None
    else:
        store = _load_json_store()
        for p in store["practical_assessments"]:
            if p["worker_id"] == worker_id:
                data = DictRow(copy.deepcopy(p))
                data["checklist_scores"] = json.loads(data["checklist_scores_json"])
                return data
        return None


def get_dashboard_stats():
    if USE_SQLITE:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM workers")
        total_candidates = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM workers WHERE status = 'Certified'")
        total_certified = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM workers WHERE status IN ('AI Analyzed', 'Experience Submitted')")
        pending_assessments = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(overall_score) FROM practical_assessments WHERE decision = 'Competent'")
        avg_row = cursor.fetchone()[0]
        avg_score = round(avg_row, 1) if avg_row else 0.0
        conn.close()
        return {
            "total_candidates": total_candidates,
            "total_certified": total_certified,
            "pending_assessments": pending_assessments,
            "avg_score": avg_score
        }
    else:
        store = _load_json_store()
        total_candidates = len(store["workers"])
        total_certified = sum(1 for w in store["workers"] if w.get("status") == "Certified")
        pending_assessments = sum(1 for w in store["workers"] if w.get("status") in ("AI Analyzed", "Experience Submitted"))
        competent_scores = [p["overall_score"] for p in store["practical_assessments"] if p.get("decision") == "Competent"]
        avg_score = round(sum(competent_scores) / len(competent_scores), 1) if competent_scores else 0.0
        return {
            "total_candidates": total_candidates,
            "total_certified": total_certified,
            "pending_assessments": pending_assessments,
            "avg_score": avg_score
        }
