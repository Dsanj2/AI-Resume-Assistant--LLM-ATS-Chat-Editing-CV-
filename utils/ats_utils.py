import re
from collections import Counter
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

def score_resume(resume_text: str, job_desc: str) -> int:
    """
    ATS scoring based on keyword overlap with job description.
    """
    resume_text = resume_text.lower()
    job_desc = job_desc.lower()

    # Extract keywords dynamically
    jd_keywords = extract_keywords_from_job(job_desc, top_n=50)
    resume_words = set(re.findall(r"\w+", resume_text.lower()))

    # Count how many job keywords are present in the resume
    matched_keywords = [kw for kw in jd_keywords if all(w in resume_words for w in kw.split())]
    if not jd_keywords:
        return 0
    score = int(len(matched_keywords) / len(jd_keywords) * 100)
    return min(score, 100)


def extract_keywords_from_job(job_desc: str, top_n: int = 15):
    """
    Dynamically extract keywords (tools, languages, skills, requirements) from job description.
    Returns top_n keywords sorted by frequency.
    """
    job_desc = job_desc.lower()

    # Capture multi-word phrases by splitting on punctuation and conjunctions
    phrases = re.split(r'[,:;\n]', job_desc)

    # Clean phrases
    cleaned_phrases = []
    for p in phrases:
        p = p.strip()
        if not p:
            continue
        # Ignore generic stopwords
        words = [w for w in re.findall(r'\w+', p) if w not in ENGLISH_STOP_WORDS]
        if words:
            cleaned_phrases.append(" ".join(words))

    # Count frequency
    freq = Counter(cleaned_phrases)
    top_keywords = [kw for kw, _ in freq.most_common(top_n)]
    return top_keywords
