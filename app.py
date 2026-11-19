"""
KaushalSetu - Main Flask Application
Smart India Hackathon 2026: AI-Assisted Skill Assessment Tool for Recognition of Prior Learning (RPL)
"""

import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from rpl_data import QUALIFICATION_PACKS, TRADE_OPTIONS, SAMPLE_EXPERIENCES
from ai_engine import analyze_worker_experience
import database as db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "kaushalsetu-sih2026-secure-key-9812")

# Initialize database schema and demonstration data on startup
with app.app_context():
    db.init_db()
    db.seed_demo_data()


# -------------------------------------------------------------
# Context Processors & Helpers
# -------------------------------------------------------------
@app.context_processor
def inject_global_data():
    """Make common trade options and year available in all templates."""
    return {
        "trades": TRADE_OPTIONS,
        "qp_dict": QUALIFICATION_PACKS,
        "current_year": 2026
    }


# -------------------------------------------------------------
# 1. HOME PAGE
# -------------------------------------------------------------
@app.route("/")
def index():
    """Home page with hero, RPL explanation, how it works, features, and impact."""
    stats = db.get_dashboard_stats()
    return render_template("index.html", stats=stats)


# -------------------------------------------------------------
# 2. WORKER REGISTRATION
# -------------------------------------------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    """Worker registration page with trade, experience, contact, and language."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        mobile = request.form.get("mobile", "").strip()
        email = request.form.get("email", "").strip()
        aadhaar = request.form.get("aadhaar", "").strip()
        state = request.form.get("state", "").strip()
        district = request.form.get("district", "").strip()
        preferred_language = request.form.get("preferred_language", "Hindi").strip()
        trade = request.form.get("trade", "").strip()
        years_experience = int(request.form.get("years_experience", 1))
        prior_education = request.form.get("prior_education", "Non-Formal").strip()

        # Input validation
        if not name or not mobile or not trade:
            flash("Please fill in all required fields (Name, Mobile, and Trade).", "danger")
            return render_template("register.html")

        # Mask Aadhaar for privacy if provided
        aadhaar_masked = ""
        if aadhaar:
            clean_aadhaar = aadhaar.replace(" ", "").replace("-", "")
            if len(clean_aadhaar) >= 4:
                aadhaar_masked = f"XXXX-XXXX-{clean_aadhaar[-4:]}"
            else:
                aadhaar_masked = "XXXX-XXXX-0000"

        worker_id = db.create_worker(
            name=name,
            mobile=mobile,
            email=email,
            state=state,
            district=district,
            preferred_language=preferred_language,
            trade=trade,
            years_experience=years_experience,
            prior_education=prior_education,
            aadhaar_masked=aadhaar_masked
        )

        flash(f"Candidate '{name}' successfully registered! Now share your hands-on work experience.", "success")
        return redirect(url_for("experience", worker_id=worker_id))

    return render_template("register.html")


# -------------------------------------------------------------
# 3. EXPERIENCE SUBMISSION
# -------------------------------------------------------------
@app.route("/experience/<int:worker_id>", methods=["GET", "POST"])
def experience(worker_id):
    """Experience narrative submission with text and browser voice input."""
    worker = db.get_worker(worker_id)
    if not worker:
        flash("Worker profile not found.", "danger")
        return redirect(url_for("register"))

    existing_exp = db.get_worker_experience(worker_id)

    if request.method == "POST":
        experience_text = request.form.get("experience_text", "").strip()
        input_method = request.form.get("input_method", "text")

        if len(experience_text) < 30:
            flash("Please provide a more detailed description of your tasks, tools, and experience (at least 30 characters).", "warning")
            return render_template("experience.html", worker=worker, existing_exp=existing_exp)

        # Save narrative to database
        exp_id = db.save_worker_experience(worker_id, experience_text, input_method)

        # Trigger AI Skill Mapping engine
        analysis = analyze_worker_experience(
            trade_id=worker["trade"],
            experience_text=experience_text,
            years_experience=worker["years_experience"]
        )

        if not analysis.get("success"):
            flash(f"Analysis Error: {analysis.get('error')}", "danger")
            return render_template("experience.html", worker=worker, existing_exp=existing_exp)

        # Store AI mapping results in SQLite
        db.save_ai_mapping(worker_id, exp_id, analysis)

        flash("AI Skill Mapping complete! Review your preliminary competency breakdown below.", "success")
        return redirect(url_for("skill_mapping", worker_id=worker_id))

    sample_text = SAMPLE_EXPERIENCES.get(worker["trade"], "")
    return render_template("experience.html", worker=worker, existing_exp=existing_exp, sample_text=sample_text)


# -------------------------------------------------------------
# 4. AI SKILL MAPPING
# -------------------------------------------------------------
@app.route("/skill-mapping/<int:worker_id>")
def skill_mapping(worker_id):
    """Display suggested competencies, matched criteria, explanations, and RPL disclaimer."""
    worker = db.get_worker(worker_id)
    if not worker:
        flash("Worker not found.", "danger")
        return redirect(url_for("index"))

    mapping = db.get_ai_mapping(worker_id)
    if not mapping:
        flash("No experience has been submitted for this worker yet.", "warning")
        return redirect(url_for("experience", worker_id=worker_id))

    experience_data = db.get_worker_experience(worker_id)
    qp_info = QUALIFICATION_PACKS.get(worker["trade"], {})

    return render_template(
        "skill_mapping.html",
        worker=worker,
        mapping=mapping,
        experience=experience_data,
        qp=qp_info
    )


# -------------------------------------------------------------
# 5. PRACTICAL ASSESSMENT (Assessor Evaluation)
# -------------------------------------------------------------
@app.route("/practical/<int:worker_id>", methods=["GET", "POST"])
def practical(worker_id):
    """Assessor practical evaluation form: NOS checklist, viva questions, tool handling & scoring."""
    worker = db.get_worker(worker_id)
    if not worker:
        flash("Worker not found.", "danger")
        return redirect(url_for("dashboard"))

    qp_info = QUALIFICATION_PACKS.get(worker["trade"], {})
    existing_assessment = db.get_practical_assessment(worker_id)
    mapping = db.get_ai_mapping(worker_id)

    if request.method == "POST":
        assessor_name = request.form.get("assessor_name", "").strip()
        assessor_id = request.form.get("assessor_id", "").strip()
        assessment_date = request.form.get("assessment_date", "").strip()
        assessor_comments = request.form.get("assessor_comments", "").strip()
        evidence_notes = request.form.get("evidence_notes", "").strip()
        decision = request.form.get("decision", "Competent").strip()
        bridge_modules = request.form.get("bridge_modules", "").strip()

        # Parse per-NOS checklist scores
        checklist_scores = {}
        total_checklist_weighted = 0.0
        total_weight = 0.0

        for nos in qp_info.get("nos_list", []):
            nos_code = nos["code"]
            weight = nos.get("weight", 20)
            score_val = float(request.form.get(f"nos_score_{nos_code}", 70))
            checklist_scores[nos_code] = score_val
            total_checklist_weighted += (score_val * weight)
            total_weight += weight

        practical_score = round(total_checklist_weighted / max(total_weight, 1.0), 1)
        viva_score = float(request.form.get("viva_score", 75))
        safety_score = float(request.form.get("safety_score", 80))

        # Overall composite score: 50% Practical + 30% Viva + 20% Safety
        overall_score = round((practical_score * 0.50) + (viva_score * 0.30) + (safety_score * 0.20), 1)

        db.save_practical_assessment(
            worker_id=worker_id,
            assessor_name=assessor_name or "Authorized Sector Assessor",
            assessor_id=assessor_id or "SSC-ASSESS-DEMO",
            assessment_date=assessment_date,
            checklist_scores=checklist_scores,
            practical_score=practical_score,
            viva_score=viva_score,
            safety_score=safety_score,
            overall_score=overall_score,
            assessor_comments=assessor_comments,
            evidence_notes=evidence_notes,
            decision=decision,
            bridge_modules=bridge_modules
        )

        flash(f"Practical Assessment recorded successfully! Result: {decision} ({overall_score}%).", "success")
        return redirect(url_for("report", worker_id=worker_id))

    return render_template(
        "practical.html",
        worker=worker,
        qp=qp_info,
        mapping=mapping,
        assessment=existing_assessment
    )


# -------------------------------------------------------------
# 6. ASSESSOR DASHBOARD
# -------------------------------------------------------------
@app.route("/dashboard")
def dashboard():
    """Assessor administration dashboard: candidates, statuses, evidence review & decision actions."""
    trade_filter = request.args.get("trade", "all")
    status_filter = request.args.get("status", "all")
    search_query = request.args.get("search", "").strip()

    workers = db.get_all_workers(
        trade_filter=trade_filter,
        status_filter=status_filter,
        search_query=search_query
    )
    stats = db.get_dashboard_stats()

    return render_template(
        "dashboard.html",
        workers=workers,
        stats=stats,
        trade_filter=trade_filter,
        status_filter=status_filter,
        search_query=search_query
    )


# -------------------------------------------------------------
# 7. FINAL REPORT
# -------------------------------------------------------------
@app.route("/report/<int:worker_id>")
def report(worker_id):
    """Final RPL Assessment Report & Skill Transcript with demonstrated competencies & decision."""
    worker = db.get_worker(worker_id)
    if not worker:
        flash("Worker not found.", "danger")
        return redirect(url_for("dashboard"))

    mapping = db.get_ai_mapping(worker_id)
    assessment = db.get_practical_assessment(worker_id)
    qp_info = QUALIFICATION_PACKS.get(worker["trade"], {})

    return render_template(
        "report.html",
        worker=worker,
        mapping=mapping,
        assessment=assessment,
        qp=qp_info
    )


# -------------------------------------------------------------
# API & Helper Endpoints
# -------------------------------------------------------------
@app.route("/api/sample-experience/<trade_id>")
def get_sample_experience(trade_id):
    """Return pre-crafted realistic experience text for 1-click loading."""
    sample = SAMPLE_EXPERIENCES.get(trade_id, "")
    return jsonify({"trade": trade_id, "sample_text": sample})


@app.route("/api/override-ai/<int:worker_id>", methods=["POST"])
def override_ai(worker_id):
    """Allow assessor to adjust or record notes regarding AI skill suggestions."""
    notes = request.form.get("override_notes", "").strip()
    db.update_ai_override(worker_id, notes)
    flash("Assessor override notes recorded successfully.", "info")
    return redirect(url_for("skill_mapping", worker_id=worker_id))


if __name__ == "__main__":
    # Support dynamic PORT and host binding for deployment platforms like Render
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "False").lower() in ("true", "1")
    app.run(host="0.0.0.0", port=port, debug=debug)
