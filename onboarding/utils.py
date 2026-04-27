import pdfplumber
import json
import re
def extract_text_from_pdf(pdf_path):
    """Extract raw text from PDF using pdfplumber."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()
def extract_resume_data_basic(pdf_text):
    """Use basic Regex to extract structured data from resume text without an LLM."""
    
    # Extract Email
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', pdf_text)
    email = email_match.group(0) if email_match else ""
    
    # Extract Phone
    phone_match = re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', pdf_text)
    phone = phone_match.group(0) if phone_match else ""
    
    # Extract Name (Approximation: usually the first non-empty line)
    lines = [line.strip() for line in pdf_text.split('\n') if line.strip()]
    full_name = lines[0][:100] if lines else "Unknown Candidate"
    
    # Basic logic to extract Skills and Education
    skills = "Not extracted"
    education = "Not extracted"
    
    keywords = ["skills", "education", "experience", "employment", "summary", "projects", "certifications"]
    current_section = None
    section_data = {k: [] for k in keywords}
    
    for line in lines:
        cleaned_line = line.strip()
        lower_line = cleaned_line.lower().replace(":", "")
        
        matched_section = None
        for kw in keywords:
            if kw in lower_line and len(lower_line.split()) <= 4:
                matched_section = kw
                break
                
        if matched_section:
            current_section = matched_section
        elif current_section and cleaned_line:
            section_data[current_section].append(cleaned_line)
            
    if section_data["skills"]:
        skills = ", ".join(section_data["skills"][:10])
        if len(skills) > 500: skills = skills[:500] + "..."
            
    if section_data["education"]:
        education = " | ".join(section_data["education"][:10])
        if len(education) > 500: education = education[:500] + "..."
    
    return {
        "full_name": full_name,
        "email": email,
        "phone": phone,
        "location": "Not extracted (Local processing)",
        "current_role": "Not extracted",
        "years_of_experience": "0",
        "skills": skills,
        "education": education,
        "work_experience": "Not extracted",
        "summary": "Not extracted",
        "linkedin": "",
        "github": ""
    }


def process_resume(pdf_path):
    """Full pipeline: PDF -> text -> Regex extraction -> dict."""
    try:
        pdf_text = extract_text_from_pdf(pdf_path)
        if not pdf_text:
            return None, "Could not extract text from PDF."

        data = extract_resume_data_basic(pdf_text)
        data['raw_text'] = pdf_text
        return data, None
    except Exception as e:
        return None, str(e)
