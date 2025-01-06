from flask import Flask, request, jsonify, send_from_directory
import fitz  # PyMuPDF
import google.generativeai as genai
import os
import re
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Access the API key
api_key = os.getenv("gemini_api_key")

app = Flask(__name__)
CORS(app)  

domain_skills = {
    'Computer Science': ["Python", "Java", "JavaScript", "SQL", "HTML", "CSS", "Django", "Flask", "React", "Node.js", "C", "C++", "Spring Boot", "Thymeleaf", "ProjectManagement", "ReactJS"],
    'Electronics': ["Circuit Design", "Signal Processing", "Embedded Systems", "Analog Electronics", "Digital Electronics", "Communication Systems"],
    'Mechanical': ["Thermodynamics", "Fluid Mechanics", "Material Science", "Manufacturing Processes", "Dynamics", "Control Systems"],
    'Electrical': ["Power Systems", "Electrical Machines", "Control Systems", "Power Electronics", "Signal Processing", "Renewable Energy Systems"]
}

def get_gemini_response(prompt, extracted_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    combined_input = f"{prompt}\n\n{extracted_text}"
    response = model.generate_content([combined_input])
    return response.text.strip()

def extract_text_from_pdf(pdf_file):
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text()
    return text

def map_domain(extracted_domain):
    # Use regex to find the relevant domain in the extracted string
    degree_domain_regex = r"(CSE|ECE|MECH|Electrical|Computer Science|Electronics|Mechanical|Electrical)"
    match = re.search(degree_domain_regex, extracted_domain, re.IGNORECASE)

    if match:
        normalized_domain = match.group(0).lower()
        domain_mapping = {
            'computer science': 'Computer Science',
            'cse': 'Computer Science',
            'electronics': 'Electronics',
            'ece': 'Electronics',
            'mechanical': 'Mechanical',
            'mech': 'Mechanical',
            'electrical': 'Electrical'
        }

        for key in domain_mapping:
            if key in normalized_domain:
                return domain_mapping[key]
    
    return "Unknown"

def calculate_skill_match(domain, resume_skills):
    skill_keywords = domain_skills.get(domain, [])
    resume_skills = [skill.strip().lower() for skill in resume_skills]
    matching_skills = set(skill for skill in resume_skills if skill in [s.lower() for s in skill_keywords])
    total_skills = len(skill_keywords)
    
    if total_skills == 0:
        return 0, matching_skills
    
    match_percentage = (len(matching_skills) / total_skills) * 100
    return match_percentage, matching_skills

def clean_skill(skill):
    return skill.replace('-', '').strip()

def extract_and_clean_skills(resume_skills_text):
    return [clean_skill(skill) for skill in resume_skills_text.split('\n') if skill.strip()]

@app.route('/uploadResume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400
    
    file = request.files['resume']
    extracted_text = extract_text_from_pdf(file)
    print("Extracted Text:",extracted_text)

    input_prompt_degree = """
    Get the domain mentioned in this resume like (BE Computer Science and Engineering or BE Electronics or BTECH IT) based on the data given. Don't add extra contents, just give me the actual degree with domain.
    """
    
    input_prompt_skills = """
    Get the skills mentioned in my resume. Don't add extra contents. Just give me the technical skills
    """

    resume_skills_text = get_gemini_response(input_prompt_skills, extracted_text)
    extracted_domain = get_gemini_response(input_prompt_degree, extracted_text)

    domain = map_domain(extracted_domain)
    resume_skills = extract_and_clean_skills(resume_skills_text)

    if domain and domain != "Unknown":
        match_percentage, matching_skills = calculate_skill_match(domain, resume_skills)
    else:
        match_percentage, matching_skills = 0, []

    return jsonify({
        "skills": resume_skills,
        "domain": extracted_domain,
        "mapped_domain": domain,
        "matched_skills": list(matching_skills),
        "match_percentage": int(match_percentage)
    })



if __name__ == '__main__':
    app.run(debug=True)
