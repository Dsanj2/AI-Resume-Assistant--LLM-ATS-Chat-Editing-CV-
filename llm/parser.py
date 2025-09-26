import json
import ollama

def parse_resume_llm(resume_text):
    """
    Robustly parse a resume into JSON. Always returns a dictionary.
    """
    prompt = f"""
You are an AI resume parser. Extract the following fields in strict JSON:
- personal_info
- education
- experience
- skills
- projects
- achievements

Resume text:
\"\"\"{resume_text}\"\"\"

Return ONLY valid JSON. If you cannot parse some fields, leave them empty.
"""

    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}]
    )

    # Get text safely
    if isinstance(response, dict):
        text = response.get('content') or response.get('result') or str(response)
    else:
        text = str(response)

    # Try parsing JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {
            "personal_info": {"name": "", "contact": ""},
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "achievements": [],
            "raw_text": resume_text
        }
