import streamlit as st
import re

from utils.file_utils import extract_text_from_file
from utils.llm_utils import parse_resume_llm, tailor_resume, chat_edit_resume ,generate_cover_letter
from utils.ats_utils import score_resume, extract_keywords_from_job
from utils.export_utils import export_pdf, export_docx
 


# =========================
# Helper: Clean LLM output
# =========================
def clean_llm_resume(text: str) -> str:
    text = re.sub(r"(?i)^.*?resume tailored.*?\n", "", text, flags=re.DOTALL)
    text = re.sub(r"(?i)to further refine this resume.*$", "", text, flags=re.DOTALL)
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        line = re.sub(r"^(\*+|-+|•)\s*", "", line)
        line = re.sub(r"(\*\*|__|\*)", "", line)
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

# =========================
# UI Styling
# =========================


# Inject gradient styles

st.markdown("""
    <style>
        /* App background gradient */
        .stApp {
            background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a18cd1);
            background-size: 400% 400%;
            animation: gradientShift 2s ease infinite;
            color: #222;
        }

        @keyframes gradientShift {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        h1, h2, h3, h4, h5, h6 {
            background: linear-gradient(to right, #ff6a00, #ee0979);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }


        /* Gradient button */
        div.stButton > button {
            background: linear-gradient(to right, #ff7f50, #ff1493);
            color: white;
            border: none;
            padding: 0.5em 1em;
            border-radius: 8px;
            font-weight: bold;
            transition: 0.3s ease;
        }

        div.stButton > button:hover {
            background: linear-gradient(to right, #ff1493, #ff7f50);
            transform: scale(1.05);
        }

        /* Gradient text block */
        .gradient-text {
            background: linear-gradient(to right, #00c6ff, #0072ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-size: 20px;
            font-weight: 600;
        }

        /* Card-style block */
        .gradient-card {
            background: linear-gradient(135deg, #faf0e6, #ffe4e1);
            padding: 1rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


st.set_page_config(page_title="AI Resume Assistant", layout="wide")
st.title("📄 AI Resume Assistant (LLM + ATS + CV + Chat Editing)")

# =========================
# File Upload
# =========================
uploaded_file = st.file_uploader("Upload your Resume (PDF/DOCX)", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Extracting text..."):
        resume_text = extract_text_from_file(uploaded_file)

    #st.subheader("Extracted Resume Text")
    #st.text_area("Resume Text", resume_text, height=100)

    job_desc = st.text_area("Paste Job Description here")

    if st.button("Tailor Resume"):
        if job_desc.strip():
            raw_resume = tailor_resume(parse_resume_llm(resume_text), job_desc)
            tailored_resume = clean_llm_resume(raw_resume)

            st.session_state["editable_resume"] = tailored_resume
            st.session_state["last_instruction"] = ""

            # ATS Score
            score = score_resume(tailored_resume, job_desc)
            st.metric("ATS Score", f"{score}/100")

            # Suggested keywords
            keywords = extract_keywords_from_job(job_desc)
            if keywords:
                st.markdown("**💡 Suggested Keywords for ATS:** " + ", ".join(keywords))
        else:
            st.warning("Please provide a job description.")

# =========================
# Editable Resume Preview
# =========================
if "editable_resume" in st.session_state:
    st.subheader("✏️ Editable Resume Preview")
    editable_resume = st.text_area(
        "You can directly edit your tailored resume here:",
        st.session_state["editable_resume"],
        height=400,
        key="resume_preview"
    )
    st.session_state["editable_resume"] = editable_resume

    # Update ATS Score
    if uploaded_file and job_desc.strip():
        score = score_resume(editable_resume, job_desc)
        st.metric("ATS Score", f"{score}/100")


# =========================
# Cover Letter Generation
# =========================
if "editable_resume" in st.session_state and job_desc.strip():
    st.subheader("📝 Generate Cover Letter")
    if st.button("Generate Cover Letter"):
        with st.spinner("Generating cover letter..."):
            cover_letter = generate_cover_letter(
                st.session_state["editable_resume"],
                job_desc
            )
            st.session_state["cover_letter"] = cover_letter
            st.success("✅ Cover letter generated.")

    if "cover_letter" in st.session_state:
        st.text_area(
            "Cover Letter Preview",
            st.session_state["cover_letter"],
            height=300,
            key="cover_letter_preview"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("⬇️ Download Cover Letter PDF"):
                export_pdf(st.session_state["cover_letter"], "cover_letter.pdf")
                st.success("Cover letter PDF exported successfully!")
        with col2:
            if st.button("⬇️ Download Cover Letter DOCX"):
                export_docx(st.session_state["cover_letter"], "cover_letter.docx")
                st.success("Cover letter DOCX exported successfully!")


    # =========================
    # Chat Editing
    # =========================
    st.subheader("💬 Chat Edit Instructions")
    instruction = st.text_input("Instruction (e.g., 'Highlight leadership skills')", value=st.session_state.get("last_instruction", ""), key="chat_instruction")
    if st.button("Apply Chat Edit"):
        if instruction.strip():
            edited_resume = clean_llm_resume(chat_edit_resume(st.session_state["editable_resume"], instruction))
            st.session_state["editable_resume"] = edited_resume
            st.session_state["last_instruction"] = instruction
            st.success("✅ Resume updated via chat instruction.")

            # Update ATS score after edit
            if job_desc.strip():
                score = score_resume(edited_resume, job_desc)
                st.metric("ATS Score", f"{score}/100")

    # =========================
    # Control Buttons
    # =========================
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🔄 Regenerate Resume"):
            if uploaded_file and job_desc.strip():
                raw_resume = tailor_resume(parse_resume_llm(resume_text), job_desc)
                tailored_resume = clean_llm_resume(raw_resume)
                st.session_state["editable_resume"] = tailored_resume
                st.success("✅ Resume regenerated.")
                score = score_resume(tailored_resume, job_desc)
                st.metric("ATS Score", f"{score}/100")

    with col3:
        if st.button("⬇️ Download PDF"):
            export_pdf(st.session_state["editable_resume"], "resume.pdf")
            st.success("PDF exported successfully!")

    with col4:
        if st.button("⬇️ Download DOCX"):
            export_docx(st.session_state["editable_resume"], "resume.docx")
            st.success("DOCX exported successfully!")








