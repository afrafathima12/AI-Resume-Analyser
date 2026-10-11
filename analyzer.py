import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILLS = [
    "python", "sql", "excel", "power bi", "tableau",
    "machine learning", "deep learning", "data analysis",
    "pandas", "numpy", "scikit-learn", "tensorflow",
    "nlp", "statistics", "data visualization",
    "communication", "problem solving", "git"
]


def find_skills(text):
    """Find known skills mentioned in the text."""
    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill.title())

    return found


def calculate_match(resume_text, job_description):
    """Compare a resume with a job description."""
    if not resume_text.strip() or not job_description.strip():
        return 0.0

    vectorizer = TfidfVectorizer()

    try:
        vectors = vectorizer.fit_transform(
            [resume_text, job_description]
        )
        score = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return round(float(score) * 100, 2)

    except ValueError:
        return 0.0


def analyze_resume(resume_text, job_description):
    resume_skills = find_skills(resume_text)
    required_skills = find_skills(job_description)

    matched_skills = [
        skill for skill in required_skills
        if skill in resume_skills
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in resume_skills
    ]

    return {
        "resume_skills": resume_skills,
        "required_skills": required_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_score": calculate_match(
            resume_text, job_description
        ),
                  "suggestions": [
                 f"Consider developing your {skill} skills."
                 for skill in missing_skills
             ],
        
       
    }