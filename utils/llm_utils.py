import json
import logging
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

# Initialize Ollama model
llm = Ollama(model="gemma3:4b")

# Allowed headers in Proper Case
ALLOWED_HEADERS = [
    "Summary", "Experience", "Education", "Skills",
    "Projects", "Achievements", "Interests / Hobbies"
]

def parse_resume_llm(resume_text: str) -> dict:
    """
    Parse resume text to JSON using LLM.
    Always returns a dict with safe defaults.
    Temperature is low for precise JSON parsing.
    """
    prompt_text = """
You are an AI resume parser. Extract the following fields in strict JSON format:
- personal_info
- education
- experience
- skills
- projects
- achievements

Resume text:
\"\"\"{resume_text}\"\"\"

Return ONLY valid JSON. If some fields are missing, leave them empty.
"""
    template = PromptTemplate(template=prompt_text, input_variables=["resume_text"])
    prompt = template.format(resume_text=resume_text)

    try:
        response = llm(prompt, temperature=0.1)
        return json.loads(response)
    except json.JSONDecodeError:
        logging.warning(f"Failed to parse JSON. LLM response: {response}")
        return {
            "personal_info": {"name": "", "contact": ""},
            "Summary": [],
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "achievements": [],
            "raw_text": resume_text
        }
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return {
            "personal_info": {"name": "", "contact": ""},
            "Summary": [],
            "education": [],
            "experience": [],
            "skills": [],
            "projects": [],
            "achievements": [],
            "raw_text": resume_text
        }

def tailor_resume(resume_json: dict, job_description: str) -> str:
    """
    Tailor the resume JSON to a specific job description using LLM.
    Returns a professional plain text resume.
    Constraints:
    - Only include allowed headers if they have content.
    - Headers must be Proper Case as in ALLOWED_HEADERS.
    - Preserve personal_info (name/contact) at the top.
    """
    prompt_text = f"""
You are an AI assistant that rewrites resumes to match the given job description.

Resume JSON: {{resume_json}}
Job description: {{job_description}}

Return a plain text resume that meets the following rules:
- Only include these headers if there is content: {ALLOWED_HEADERS}
- Headers must appear exactly in Proper Case.
- Omit any section that has no content.
- Highlight relevant skills, experience, and education.
- Preserve personal_info (name and contact info) at the top.
- Do NOT add commentary or explanations.
- Format clearly and professionally.
"""
    template = PromptTemplate(template=prompt_text, input_variables=["resume_json", "job_description"])
    prompt = template.format(resume_json=json.dumps(resume_json), job_description=job_description)

    try:
        response = llm(prompt, temperature=0.5)
        return response
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return "Error: Could not generate tailored resume."

def chat_edit_resume(resume_text: str, instruction: str) -> str:
    """
    Edit a resume according to a user instruction.
    Returns the edited resume as plain text.
    Constraints:
    - Only include allowed headers if they have content.
    - Headers must be Proper Case.
    - Preserve personal_info at the top.
    """
    prompt_text = f"""
You are an AI assistant that edits resumes.
Resume text: {{resume_text}}
Instruction: {{instruction}}

Return the edited resume in plain text following these rules:
- Keep headers consistent with Proper Case: {ALLOWED_HEADERS}.
- Only include sections that have content; omit empty sections.
- Preserve personal_info (name and contact info) at the top.
- Do not include any commentary or suggestions, only the resume content.
"""
    template = PromptTemplate(template=prompt_text, input_variables=["resume_text", "instruction"])
    prompt = template.format(resume_text=resume_text, instruction=instruction)

    try:
        response = llm(prompt, temperature=0.3)
        return response
    except Exception as e:
        logging.error(f"LLM call failed: {e}")
        return "Error: Could not edit resume."

def generate_cover_letter(resume_text: str, job_description: str) -> str:
    """
    Generate a professional cover letter based on the tailored resume and job description.
    Uses the same Ollama LLM as the resume functions.
    """
    from langchain_community.llms import Ollama
    llm = Ollama(model="gemma3:4b")  # same model as in tailor_resume

    prompt_text = f"""
You are an AI assistant that writes professional cover letters.
Resume content: {resume_text}
Job description: {job_description}

Return a concise, professional cover letter that highlights relevant skills and experience.
Do NOT include explanations, just the cover letter content.
"""
    try:
        response = llm(prompt_text, temperature=0.3)
        return response.strip()
    except Exception as e:
        import logging
        logging.error(f"LLM call failed: {e}")
        return "Error: Could not generate cover letter."
