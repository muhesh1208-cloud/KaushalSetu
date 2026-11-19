# KAUSHALSETU (कौशलसेतु)
## AI-Assisted Skill Assessment Tool for Recognition of Prior Learning (RPL)
**Smart India Hackathon 2026 Project**

---

### 🌟 Project Overview
Under the Government of India's **Skill India Mission** and **PMKVY 4.0**, millions of unorganized workers (electricians, plumbers, masons, mechanics, welders, tailors) possess valuable hands-on skills acquired through informal work experience, but lack formal NSQF (National Skills Qualifications Framework) certification.

**KaushalSetu** bridges this informal-to-formal gap using:
1. **Explainable AI Skill Mapping**: Maps informal experience narratives (captured via text or voice) to genuine National Occupational Standards (NOS) and Qualification Packs (QP).
2. **Human Assessor In-The-Loop**: Complies with statutory RPL guidelines. AI outputs are strictly assistive; certified Sector Skill Council assessors conduct practical demonstrations and viva-voce before issuing certificates.
3. **Transparent Assessment Transcripts**: Generates standardized RPL Skill Transcripts and printable official reports with demonstrated competencies and targeted bridge training recommendations.

---

### 🛠️ Technology Stack
- **Frontend**: Modern HTML5, Responsive CSS3 (Navy Blue `#0f172a`, Teal `#0d9488`, White, Subtle Gradients), Vanilla JavaScript (Web Speech API voice transcription, live assessment score calculator).
- **Backend**: Python Flask 3.1.3 web framework.
- **Persistence**: SQLite / Resilient JSON store fallback.
- **AI Engine**: Local explainable NLP semantic matching engine with evidence sentence extraction and future Google Gemini API integration hooks.

---

### 📂 Project Structure
```
kaushalsetu/
├── app.py                     # Main Flask application with all 7 page routes and API endpoints
├── database.py                # Database persistence layer (SQLite with automatic JSON fallback)
├── rpl_data.py                # Authentic NSDC Qualification Packs & National Occupational Standards
├── ai_engine.py               # AI skill mapping algorithm, evidence extraction, explainability
├── static/
│   ├── css/
│   │   ├── style.css          # Design system: Navy blue & teal theme, responsive cards, gauges
│   │   └── print.css          # Print/PDF layout for Official RPL Skill Certificate & Report
│   └── js/
│       ├── main.js            # General UI, mobile menu, auto-dismissing flash alerts
│       ├── voice.js           # Web Speech API speech-to-text with microphone indicator
│       └── assessor.js        # Live practical score calculator & recommendation engine
├── templates/
│   ├── base.html              # Layout master template with header, footer, and navigation
│   ├── index.html             # 1. Home Page (Hero, What is RPL, How It Works, Features & Benefits)
│   ├── register.html          # 2. Worker Registration (Contact, trade, language, experience)
│   ├── experience.html        # 3. Experience Submission (Text + Voice input, 1-click sample loaders)
│   ├── skill_mapping.html     # 4. AI Skill Mapping (Suggested competencies, matched criteria, explanations)
│   ├── practical.html         # 5. Practical Assessment (Competency checklist, Assessor scoring & viva)
│   ├── dashboard.html         # 6. Assessor Dashboard (Pipeline, evidence review, override AI, decisions)
│   └── report.html            # 7. Final RPL Report (Competency breakdown, scores, assessor sign-off)
└── data/
    └── kaushalsetu_store.json # Persistent database with pre-seeded demo candidates
```

---

### 🚀 How to Run the Website
In PowerShell or Command Prompt, navigate to the project directory and run:

```bash
cd "C:\Users\D Krishnapriya\.gemini\antigravity\scratch\kaushalsetu"
python app.py
```

Then open your browser and navigate to:
**http://127.0.0.1:5000**
