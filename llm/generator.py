import json
import ollama

def generate_tailored_cv(resume_json, job_description):
    """
    Generate a tailored CV text using Gemma3.
    """
    prompt = f"""
You are a CV generator. 
Given this candidate info: {json.dumps(resume_json)}
and this job description: {job_description}

Generate an ATS-friendly, keyword-optimized CV.
Output in plain text.
"""

    response = ollama.chat(
        model="gemma3:1b",
        messages=[{"role": "user", "content": prompt}]
    )

    # Handle different possible response structures
    if isinstance(response, dict):
        if 'content' in response:
            return response['content']
        elif 'result' in response:
            return response['result']
        elif 'message' in response and 'content' in response['message']:
            return response['message']['content']
        else:
            return str(response)
    return str(response)
