from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

# Access the API key
api_key = os.getenv("gemini_api_key")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

def evaluate_answer(reference_answer, candidate_answer, question):
    text_input = (f"Check the similarity between the following answers for the question '{question}':\n"
                  f"Candidate Answer: {candidate_answer}\n"
                  f"Reference Answer: {reference_answer}\n"
                  "Provide only the percentage similarity to estimate how correct the candidate answer is compared to the reference answer. Give the output only as percentage.")
    
    try:
        response = model.generate_content([text_input])
        response_text = response.text.strip()
        similarity_percentage = float(response_text.replace('%', '').strip())
    except Exception as e:
        print(f"Error generating content: {e}")
        similarity_percentage = 0.0
    
    return similarity_percentage

@app.route('/evaluate', methods=['POST'])
def evaluate():
    if request.content_type != 'application/json':
        return jsonify({"error": "Unsupported Media Type"}), 415
    
    item = request.json
    if not all(key in item for key in ['reference_answer', 'candidate_answer', 'question']):
        return jsonify({"error": "Missing input data"}), 400
    
    reference_answer = item.get('reference_answer')
    candidate_answer = item.get('candidate_answer')
    question = item.get('question')
    print(reference_answer,"-------000000---------")
    match_percentage = evaluate_answer(reference_answer, candidate_answer, question)
    print(match_percentage)
    return jsonify({"Percentage_gem": f"{match_percentage:.2f}"})

if __name__ == '__main__':
    app.run(debug=False, port=5008)
