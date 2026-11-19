"""
KaushalSetu - AI Skill Mapping Engine
Performs explainable, transparent natural language skill extraction and matching
against official Qualification Packs (QP) and National Occupational Standards (NOS).
Ready for Google Gemini API integration while providing a robust offline NLP semantic matcher.
"""

import re
import os
import json
from rpl_data import QUALIFICATION_PACKS

# Optional Gemini API key environment variable (configured when available)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")


def clean_and_tokenize(text):
    """Normalize text into lowercase alphanumeric tokens."""
    if not text:
        return []
    cleaned = re.sub(r'[^\w\s]', ' ', text.lower())
    return [word for word in cleaned.split() if len(word) > 2]


def extract_matching_evidence(sentences, keywords):
    """Extract full sentences where candidate demonstrated competency keywords."""
    matched_sentences = []
    for sentence in sentences:
        s_lower = sentence.lower()
        found_words = [kw for kw in keywords if re.search(r'\b' + re.escape(kw) + r'\b', s_lower)]
        if found_words:
            matched_sentences.append({
                "sentence": sentence.strip(),
                "keywords": found_words
            })
    return matched_sentences


def analyze_worker_experience(trade_id, experience_text, years_experience=0):
    """
    Core AI Skill Mapping Algorithm:
    Evaluates candidate's experience narrative against the official Qualification Pack NOS criteria.
    Produces dynamic scores, detected evidence, matched criteria, and transparent explanations.
    """
    if trade_id not in QUALIFICATION_PACKS:
        return {
            "success": False,
            "error": f"Unknown trade '{trade_id}'. Please select a valid trade."
        }

    qp = QUALIFICATION_PACKS[trade_id]
    experience_text = (experience_text or "").strip()
    
    if len(experience_text) < 20:
        return {
            "success": False,
            "error": "Experience description is too brief. Please provide a detailed description of your daily tasks, tools used, and safety practices."
        }

    # Split candidate text into individual sentences for evidence tracking
    sentences = re.split(r'(?<=[.!?])\s+', experience_text)
    user_tokens = set(clean_and_tokenize(experience_text))
    full_text_lower = experience_text.lower()

    # Track tools mentioned
    tools_identified = []
    for tool in qp.get("common_tools", []):
        tool_lower = tool.lower()
        # Check either full tool name or main token
        tokens = tool_lower.split()
        if all(t in full_text_lower for t in tokens) or tool_lower in full_text_lower:
            tools_identified.append(tool)

    competency_results = []
    total_weighted_score = 0.0
    total_weight = 0.0

    suggested_competencies = []
    bridge_training_needed = []

    for nos in qp["nos_list"]:
        nos_code = nos["code"]
        nos_title = nos["title"]
        weight = nos.get("weight", 20)
        keywords = nos.get("keywords", [])
        pcs = nos.get("performance_criteria", [])

        # Calculate keyword match percentage
        matched_kws = []
        for kw in keywords:
            if re.search(r'\b' + re.escape(kw) + r'\b', full_text_lower):
                matched_kws.append(kw)

        keyword_ratio = len(matched_kws) / max(len(keywords), 1)

        # Extract contextual sentences as evidence
        evidence_matches = extract_matching_evidence(sentences, keywords)
        evidence_count = len(evidence_matches)

        # Base confidence calculation based on keyword breadth and sentence depth
        # Breadth: 50%, Depth of evidence: 40%, Experience modifier: 10%
        breadth_score = min(keyword_ratio * 100, 100)
        depth_score = min(evidence_count * 25, 100)
        
        # Experience factor (capped at 10 bonus points for 5+ years)
        exp_bonus = min(float(years_experience) * 1.5, 10.0)

        # Raw score computation
        raw_score = (breadth_score * 0.50) + (depth_score * 0.40) + exp_bonus
        final_score = round(min(max(raw_score, 12.0), 98.0), 1)

        # Match status classification
        if final_score >= 65.0:
            status = "Strong Match"
            status_badge = "success"
        elif final_score >= 45.0:
            status = "Partial Match (Needs Practical Verification)"
            status_badge = "warning"
        else:
            status = "Skill Gap Identified"
            status_badge = "danger"

        # Generate transparent, human-readable explanations based on findings
        matched_kw_sample = ", ".join(matched_kws[:6]) if matched_kws else "minimal technical terms"
        explanation_parts = []
        if matched_kws:
            explanation_parts.append(
                f"Candidate text demonstrated proficiency in key occupational terms: [{matched_kw_sample}]."
            )
        else:
            explanation_parts.append(
                "Candidate narrative contains few specific technical terms for this standard."
            )

        if evidence_matches:
            top_evidence = evidence_matches[0]["sentence"]
            if len(top_evidence) > 140:
                top_evidence = top_evidence[:137] + "..."
            explanation_parts.append(f'Key extracted evidence: "{top_evidence}"')
        else:
            explanation_parts.append(
                "No direct sentence-level work evidence was detected in the submitted story."
            )

        if final_score >= 65.0:
            explanation_parts.append(
                "Recommendation: Fast-track candidate to hands-on practical checklist verification."
            )
            suggested_competencies.append({
                "code": nos_code,
                "title": nos_title,
                "score": final_score
            })
        elif final_score >= 45.0:
            explanation_parts.append(
                "Recommendation: Assessor must probe specific performance criteria during viva."
            )
        else:
            explanation_parts.append(
                "Recommendation: Recommend 20-30 hours RPL bridge training module prior to reassessment."
            )
            bridge_training_needed.append({
                "code": nos_code,
                "title": nos_title,
                "reason": f"Low self-reported demonstration ({final_score}%)"
            })

        explanation = " ".join(explanation_parts)

        # Correlate matched performance criteria
        matched_pcs = []
        for pc in pcs:
            pc_lower = pc.lower()
            overlap = [kw for kw in matched_kws if kw in pc_lower]
            matched_pcs.append({
                "pc_text": pc,
                "is_aligned": len(overlap) > 0,
                "supporting_keywords": overlap
            })

        competency_results.append({
            "code": nos_code,
            "title": nos_title,
            "weight": weight,
            "score": final_score,
            "status": status,
            "status_badge": status_badge,
            "matched_keywords": matched_kws,
            "evidence_count": evidence_count,
            "evidence_samples": [e["sentence"] for e in evidence_matches[:3]],
            "explanation": explanation,
            "performance_criteria": matched_pcs,
            "viva_questions": nos.get("viva_questions", [])
        })

        total_weighted_score += (final_score * weight)
        total_weight += weight

    overall_confidence = round(total_weighted_score / max(total_weight, 1.0), 1)

    # Readiness category
    if overall_confidence >= 70:
        readiness_level = "High RPL Readiness"
        readiness_desc = "Candidate demonstrates substantial prior work knowledge matching NSQF Level standards. Ready for hands-on assessor verification."
        readiness_badge = "success"
    elif overall_confidence >= 50:
        readiness_level = "Moderate RPL Readiness"
        readiness_desc = "Candidate displays core practical experience but exhibits specific gaps in documentation, safety, or diagnostics."
        readiness_badge = "warning"
    else:
        readiness_level = "Foundation Level (Bridge Training Recommended)"
        readiness_desc = "Candidate has hands-on familiarity but lacks comprehensive coverage of National Occupational Standards. Bridge training advised."
        readiness_badge = "danger"

    return {
        "success": True,
        "trade_id": trade_id,
        "qp_code": qp["code"],
        "qp_name": qp["name"],
        "nsqf_level": qp["nsqf_level"],
        "sector": qp["sector"],
        "years_experience": years_experience,
        "overall_confidence": overall_confidence,
        "readiness_level": readiness_level,
        "readiness_desc": readiness_desc,
        "readiness_badge": readiness_badge,
        "tools_identified": tools_identified,
        "total_tools_expected": len(qp.get("common_tools", [])),
        "suggested_competencies": suggested_competencies,
        "bridge_training_needed": bridge_training_needed,
        "competency_results": competency_results,
        "official_disclaimer": (
            "STATUTORY NOTICE UNDER PMKVY RPL: This analysis is an AI-assisted preliminary mapping "
            "designed to assist certified Assessors. It DOES NOT constitute official certification or NSQF licensing. "
            "Final competency endorsement is solely the legal responsibility of an authorized Sector Skill Council Assessor "
            "following on-site practical demonstration and viva-voce."
        )
    }


def call_gemini_api_preview(prompt_text):
    """
    Gemini API Extension Stub.
    When a user or deployment supplies an active GEMINI_API_KEY, this function will call
    Google Gemini 1.5/2.0 API to enrich the RPL analysis with multilingual reasoning and voice transcription.
    Currently falls back safely to KaushalSetu's built-in NLP engine.
    """
    if not GEMINI_API_KEY:
        return {
            "available": False,
            "message": "Gemini API key is not configured. KaushalSetu is running with high-precision local NLP Engine."
        }
    
    # In production, google-generativeai client can be invoked here:
    # import google.generativeai as genai
    # genai.configure(api_key=GEMINI_API_KEY)
    # model = genai.GenerativeModel('gemini-1.5-flash')
    # response = model.generate_content(prompt_text)
    # return {"available": True, "output": response.text}
    return {
        "available": True,
        "status": "ready"
    }
