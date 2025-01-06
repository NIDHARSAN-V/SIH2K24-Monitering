from flask import Flask, request, jsonify
import string
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
import nltk
from nltk.corpus import stopwords
from collections import Counter
import numpy as np
from functools import lru_cache

# Download NLTK stopwords
nltk.download('stopwords')

app = Flask(__name__)

# Define stop words and negation words
stop_words = set(stopwords.words('english'))
negation_words = {"not", "n't", "no", "never"}

# Load the SentenceTransformer model
model_path = 'allenai/scibert_scivocab_uncased'
model = SentenceTransformer(model_path)

# Function to preprocess text
def preprocess_text(text):
    text = text.lower().translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    processed_words = []
    original_words = []
    negate = False

    for word in words:
        if word in stop_words and word not in negation_words:
            continue
        if word in negation_words:
            negate = True
            original_words.append(word)
            continue
        if negate:
            processed_words.append("NOT_" + word)
            negate = False
        else:
            processed_words.append(word)
        original_words.append(word)

    return processed_words, original_words

# Function to check for negation words in text
def check_negation(original_words):
    return any(word in negation_words for word in original_words)

# Function to remove redundant words from a list
def remove_redundant_words(words):
    return list(dict.fromkeys(words))

# Function to remove question keywords from answer words
def remove_question_keywords(answer_words, question_words):
    return [word for word in answer_words if word not in question_words]

# Function to compute word frequency vector
def compute_word_frequency_vector(words, unique_words):
    word_freq = Counter(words)
    vector = [word_freq[word] for word in unique_words]
    return vector

# Function to classify question type
def classify_question(question):
    explanation_keywords = {"explain", "describe", "why", "how"}
    if any(keyword in question.lower() for keyword in explanation_keywords):
        return "explanation"
    print("In Sbert ")
    return "fact"

# Caching embeddings for performance
@lru_cache(maxsize=10000)
def get_embedding(text):
    return model.encode(text)


def evaluate_with_keywords(reference_answer, candidate_answer, question):
    question_processed, question_original = preprocess_text(question)
    ref_processed, ref_original = preprocess_text(reference_answer)
    cand_processed, cand_original = preprocess_text(candidate_answer)

    ref_filtered = remove_question_keywords(ref_processed, question_processed)
    cand_filtered = remove_question_keywords(cand_processed, question_processed)

    ref_filtered = remove_redundant_words(ref_filtered)
    cand_filtered = remove_redundant_words(cand_filtered)

    unique_words = list(set(ref_filtered + cand_filtered))

    ref_vector = compute_word_frequency_vector(ref_filtered, unique_words)
    cand_vector = compute_word_frequency_vector(cand_filtered, unique_words)

    ref_vector = np.array(ref_vector).reshape(1, -1)
    cand_vector = np.array(cand_vector).reshape(1, -1)

    cosine_sim = cosine_similarity(ref_vector, cand_vector)[0][0]
    match_percentage = cosine_sim * 100

    return match_percentage, ref_filtered, cand_filtered, question_processed, ref_original, cand_original, question_original

# Function to evaluate answers with SBERT embeddings
def evaluate_with_sbert(reference_answer, candidate_answer, question):
    ref_processed, ref_original = preprocess_text(reference_answer)
    cand_processed, cand_original = preprocess_text(candidate_answer)

    ref_embedding = get_embedding(" ".join(ref_processed))
    cand_embedding = get_embedding(" ".join(cand_processed))

    cosine_sim = cosine_similarity([ref_embedding], [cand_embedding])[0][0]
    match_percentage = cosine_sim * 100

    return match_percentage, ref_processed, cand_processed, preprocess_text(question)[0], ref_original, cand_original, preprocess_text(question)[1]

# Function to adjust score based on negation
def adjust_for_negation(match_percentage, question_original, ref_original, cand_original):
    question_has_negation = check_negation(question_original)
    ref_has_negation = check_negation(ref_original)
    cand_has_negation = check_negation(cand_original)

    if question_has_negation and ref_has_negation and cand_has_negation:
        return match_percentage
    elif cand_has_negation and not (question_has_negation or ref_has_negation):
        match_percentage *= 0.3
    elif (question_has_negation or ref_has_negation) and not cand_has_negation:
        match_percentage *= 0.5

    return match_percentage


def generalize_score(generalized_score, question_original, ref_original, cand_original):
    # difference_threshold = 10.0

    # if abs(sbert_score - keyword_score) <= difference_threshold:
    #     generalized_score = (sbert_score + keyword_score) / 2
    # else:
    #     generalized_score = (sbert_score * 0.7) + (keyword_score * 0.3)

    generalized_score = adjust_for_negation(generalized_score, question_original, ref_original, cand_original)

    return generalized_score

def evaluate_answer(reference_answer, candidate_answer, question):
    
    question_type = classify_question(question)
    generalized_score = 0.0
    print("Question-Type:",question_type)
    if question_type == "explanation":
        generalized_score, ref_keywords, cand_keywords, question_keywords, ref_original, cand_original, question_original = evaluate_with_sbert(reference_answer, candidate_answer, question)
        # keyword_score, _, _, _, _, _, _ = evaluate_with_keywords(reference_answer, candidate_answer, question)
    else:
        generalized_score, ref_keywords, cand_keywords, question_keywords, ref_original, cand_original, question_original = evaluate_with_keywords(reference_answer, candidate_answer, question)
        # sbert_score, _, _, _, _, _, _ = evaluate_with_sbert(reference_answer, candidate_answer, question)

    generalized_score = generalize_score(generalized_score, question_original, ref_original, cand_original)

    return generalized_score, ref_keywords, cand_keywords, question_keywords

# Define Flask route for evaluation
@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    data = data.get("QandA")
    print(data)
    avg = 0
    gemavg=0
    all_avg=0
    
    QandA_with_eval = []
    for item in data:
        print()
        print("Count++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        print()
        reference_answer = item.get('reference_answer')
        candidate_answer = item.get('candidate_answer')
        question = item.get('question')
        print("ANS",reference_answer)
        


        if not all([reference_answer, candidate_answer, question]):
            return jsonify({"error": "Missing input data"}), 400

        match_percentage, ref_keywords, cand_keywords, question_keywords = evaluate_answer(reference_answer, candidate_answer, question)
        
        
        
        res = requests.post("http://localhost:5008/evaluate" ,json={'reference_answer':reference_answer ,'candidate_answer':candidate_answer , 'question':question} )   
        temp = res.json()
        print(temp)
            
        percentage_gem = temp.get('Percentage_gem')
            


        percentage_gem_int = float(percentage_gem)
        
        gemavg+=percentage_gem_int
        print("From Gemini=====", percentage_gem_int)
   
        if candidate_answer=="NULL":
            match_percentage=0
        
        avg += match_percentage
                        
        QandA_with_eval.append({
            "generalized_match_percentage": f"{match_percentage:.2f}%",
            "reference_keywords": ref_keywords,
            "candidate_keywords": cand_keywords,
            "question_keywords": question_keywords,
            "reference_keywords": ref_keywords,
            "candidate_keywords": cand_keywords,
            "question_keywords": question_keywords
        })
    
    avg = avg / len(data)  # Corrected average calculation
    gemavg=gemavg/len(data)
    all_avg = (gemavg+avg)/2
    return jsonify({"Percentage_SBert": f"{avg:.2f}%" , "Percentage_Gem": f"{gemavg:.2f}%" , "All_Average":f"{all_avg:.2f}%"})


#
if __name__ == '__main__':
    app.run(debug=False, port=5003)






# from flask import Flask, request, jsonify
# import fitz  # PyMuPDF
# import google.generativeai as genai
# import os
# from flask_cors import CORS
# import requests
# # Configure Google Gemini API
# genai.configure(api_key="AIzaSyBhXmLdc5br5YQguZfVSE4qcbbS6jP7QdE")

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# domain_skills = {
#     'Computer Science': ["Python", "Java", "JavaScript", "SQL", "HTML", "CSS", "Django", "Flask", "React", "Node.js", "C", "C++", "Spring Boot", "Thymeleaf", "Project Management", "ReactJS"],
#     'Electronics': ["Circuit Design", "Signal Processing", "Embedded Systems", "Analog Electronics", "Digital Electronics", "Communication Systems"],
#     'Mechanical': ["Thermodynamics", "Fluid Mechanics", "Material Science", "Manufacturing Processes", "Dynamics", "Control Systems"],
#     'Electrical': ["Power Systems", "Electrical Machines", "Control Systems", "Power Electronics", "Signal Processing", "Renewable Energy Systems"]
# }

# matchstart = ["React"]

# def get_gemini_response(prompt, extracted_text):
#     model = genai.GenerativeModel('gemini-1.5-flash')
#     combined_input = f"{prompt}\n\n{extracted_text}"
#     response = model.generate_content([combined_input])
#     return response.text.strip()

# def extract_text_from_pdf(pdf_file):
#     pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
#     text = ""
#     for page_num in range(len(pdf_document)):
#         page = pdf_document.load_page(page_num)
#         text += page.get_text()
#     return text

# def map_domain(extracted_domain):
#     domain_mapping = {
#         'computer science': 'Computer Science',
#         'electronics': 'Electronics',
#         'mechanical': 'Mechanical',
#         'electrical': 'Electrical'
#     }

#     normalized_domain = extracted_domain.lower()
#     for key in domain_mapping:
#         if key in normalized_domain:
#             return domain_mapping[key]
#     return "Unknown"

# def calculate_skill_match(domain, resume_skills):
#     skill_keywords = domain_skills.get(domain, [])
#     resume_skills = [skill.strip().lower() for skill in resume_skills]
#     matching_skills = set(skill for skill in resume_skills if skill in [s.lower() for s in skill_keywords])
#     total_skills = len(skill_keywords)
    
#     if total_skills == 0:
#         return 0, matching_skills
    
#     match_percentage = (len(matching_skills) / total_skills) * 100
#     return match_percentage, matching_skills

# def clean_skill(skill):
#     return skill.replace('-', '').strip()

# def extract_and_clean_skills(resume_skills_text):
#     return [clean_skill(skill) for skill in resume_skills_text.split('\n') if skill.strip()]

# @app.route('/uploadResume', methods=['POST'])
# def upload_resume():
#     global matchstart  # Declare matchstart as global to modify it within this function

#     if 'resume' not in request.files:
#         return jsonify({"error": "No resume file provided"}), 400
    
#     file = request.files['resume']
#     extracted_text = extract_text_from_pdf(file)

#     input_prompt_degree = """
#     Get the degree with domain mentioned in this resume like (BE Computer Science and Engineering, BE Electronics, or BTech IT). Don't add extra contents, just give me the actual degree with domain.
#     """
    
#     input_prompt_skills = """
#     Get the skills mentioned in my resume. Don't add extra contents. Just give me the technical skills
#     """

#     resume_skills_text = get_gemini_response(input_prompt_skills, extracted_text)
#     extracted_domain = get_gemini_response(input_prompt_degree, extracted_text)

#     domain = map_domain(extracted_domain)
#     resume_skills = extract_and_clean_skills(resume_skills_text)

#     if domain and domain != "Unknown":
#         match_percentage, matching_skills = calculate_skill_match(domain, resume_skills)
#     else:
#         match_percentage, matching_skills = 0, []
    
#     matchstart = list(matching_skills)  # Update matchstart with the matched skills
#     print(matchstart)
#     return jsonify({
#         "skills": resume_skills,
#         "domain": extracted_domain,
#         "mapped_domain": domain,
#         "matched_skills": matchstart,
#         "match_percentage": int(match_percentage)
#     })

# if __name__ == '__main__':
#     app.run(debug=False,port=5003)