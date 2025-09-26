# AI CV/Resume Assistant (LLM-ATS_Chat-editing-CV-creation)

**Description:**  
An AI-powered resume generator and ATS optimizer using Gemma3:1B LLM.  
- Parse resumes into JSON sections  
- Generate ATS-friendly CVs  
- Highlight missing keywords and refine in real-time  
- Download final CV as DOCX or PDF

## Features
- Resume parsing via LLM
- ATS keyword extraction
- Inline missing keyword highlights
- Optional auto-insertion of keywords
- Coverletter creation

## Run Locally
install Ollama (model = gemma3:4b)
```bash
git clone https://github.com/Dsanj2/AI-Resume-Assistant-LLM-ATS-Chat-Editing-
python -m venv venv
./vevn/Scripts/activate
pip install -r requirements.txt
streamlit run app.py






