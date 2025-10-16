from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# -------------------------
# Jooble API configuration
# -------------------------
API_KEY = "96c15234-5c82-46b8-b873-38b952cda5ff"   # <- replace with your key
API_URL = f"https://jooble.org/api/{API_KEY}"

# -------------------------
# Skill extraction
# -------------------------
def extract_skills(resume_text):
    skill_keywords = ["python", "sql", "machine learning", "data", "analysis",
                      "java", "javascript", "excel", "aws", "cloud", "django", "flask"]
    text_lower = resume_text.lower()
    return [kw for kw in skill_keywords if kw in text_lower]

# -------------------------
# Match score calculation
# -------------------------
def match_score(resume_skills, job_desc):
    if not resume_skills or not job_desc:
        return 0
    job_text = job_desc.lower()
    overlap = [skill for skill in resume_skills if skill in job_text]
    return len(overlap)/len(resume_skills)

# -------------------------
# Fetch jobs from Jooble API
# -------------------------
def fetch_jobs(query, location, count=20):
    payload = {
        "keywords": query,
        "location": location
    }
    try:
        resp = requests.post(API_URL, json=payload)
        resp.raise_for_status()
        return resp.json().get("jobs", [])
    except Exception as e:
        print("Error fetching jobs:", e)
        return []

# -------------------------
# Flask routes
# -------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    skills, matches = [], []
    resume_text, location = "", ""

    if request.method == "POST":
        resume_text = request.form.get("resume", "")
        location = request.form.get("location", "")

        # Step 1: Extract skills
        skills = extract_skills(resume_text)

        if skills:
            # Use first skill as query (you can enhance to use multiple)
            query = skills[0]
            jobs = fetch_jobs(query, location)

            # Step 2: Score matches
            for job in jobs:
                desc = job.get("snippet", "")
                score = match_score(skills, desc)
                matches.append({
                    "title": job.get("title", ""),
                    "company": job.get("company", ""),
                    "location": job.get("location", ""),
                    "score": round(score*100, 1),
                    "url": job.get("link", "")
                })

            matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    return render_template("index.html", skills=skills, matches=matches,
                           resume_text=resume_text, location=location)

if __name__ == "__main__":
    app.run(debug=True)
