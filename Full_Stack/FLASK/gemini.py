

# import os
# from flask import Flask, request, jsonify
# from transformers import T5ForConditionalGeneration, T5Tokenizer, BertTokenizer, BertForQuestionAnswering
# from sentence_transformers import SentenceTransformer, util
# import torch
# import requests

# app = Flask(__name__)

# project_dir = os.path.dirname(os.path.abspath(__file__))

# t5_model_name = "allenai/t5-small-squad2-question-generation"
# t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name, cache_dir=project_dir)
# t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name, cache_dir=project_dir)

# bert_tokenizer = BertTokenizer.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2", cache_dir=project_dir)
# bert_model = BertForQuestionAnswering.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2", cache_dir=project_dir)

# embedder = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=project_dir)

# evaluation_url = 'http://localhost:5003/evaluate'  

# def run_model(input_string, **generator_args):
#     input_ids = t5_tokenizer.encode(input_string, return_tensors="pt")
#     res = t5_model.generate(input_ids, **generator_args)
#     output = t5_tokenizer.batch_decode(res, skip_special_tokens=True)
#     return output

# def filter_similar_questions(questions, similarity_threshold=0.75):
#     embeddings = embedder.encode(questions, convert_to_tensor=True)
#     unique_questions = []

#     for i, question in enumerate(questions):
#         if i == 0:
#             unique_questions.append(question)
#         else:
#             is_similar = False
#             for unique_question in unique_questions:
#                 unique_embedding = embedder.encode(unique_question, convert_to_tensor=True)
#                 similarity = util.pytorch_cos_sim(embeddings[i], unique_embedding).item()
#                 if similarity > similarity_threshold:
#                     is_similar = True
#                     break
#             if not is_similar:
#                 unique_questions.append(question)

#     return unique_questions

# def get_best_answer(answers):
#     return max(answers, key=len) if answers else ""

# def clean_answer(answer):
#     return answer.strip().replace(" .", ".").replace(" ,", ",").replace("  ", " ")

# @app.route('/api/generate', methods=['POST'])
# def generate():
#     data = request.json
#     print
#     input_string = data.get("inp", "React")

#     questions = run_model(
#         input_string,
#         num_beams=15,
#         num_return_sequences=15,
#         max_length=128,
#         early_stopping=True,
#         temperature=0.7,
#         top_p=0.85,
#         top_k=50
#     )

#     filtered_questions = filter_similar_questions(questions)

#     results = []
#     all_payload=[]
#     for question in filtered_questions:
#         context = input_string

#         inputs = bert_tokenizer(question, context, return_tensors="pt")

#         with torch.no_grad():
#             outputs = bert_model(**inputs)

#         start_logits = outputs.start_logits
#         end_logits = outputs.end_logits

#         top_n = 3
#         start_indices = torch.topk(start_logits, top_n).indices.squeeze()
#         end_indices = torch.topk(end_logits, top_n).indices.squeeze()

#         answers = []
#         for start_idx in start_indices:
#             for end_idx in end_indices:
#                 if end_idx >= start_idx:
#                     answer = bert_tokenizer.convert_tokens_to_string(
#                         bert_tokenizer.convert_ids_to_tokens(inputs.input_ids[0][start_idx:end_idx+1])
#                     )
#                     answers.append(clean_answer(answer))

#         best_answer = get_best_answer(answers)
        
#         # EVALUATION here
#         print(question)
        
#         s
#         # ///question should be sent to react////
        
#         # /////get answer from react////
#         can_answer ="NUll"
#         payload = {
#             "reference_answer": best_answer,   # model answer
#             "candidate_answer": can_answer,   # user answer
#             "question": question
#         }
        
#         print(payload)
#         print("------------------------------------------------------")
#         all_payload.append(payload)
#         # evaluation_response = requests.post(evaluation_url, json=payload)
#         # evaluation_result = evaluation_response.json()
         
#         # results.append({
#         #     "question": question,
#         #     "answer": best_answer,
#         #     "evaluation": evaluation_result
#         # })

#     return jsonify({"questions_and_answers": all_payload})

# if __name__ == '__main__':
#     app.run(debug=False , port=5004)


# #





import os
from flask import Flask, request, jsonify
from transformers import T5ForConditionalGeneration, T5Tokenizer, BertTokenizer, BertForQuestionAnswering
from sentence_transformers import SentenceTransformer, util
import torch
import requests

import subprocess

app = Flask(__name__)

# project_dir = os.path.dirname(os.path.abspath(__file__))
# drive_model_path = "c:/Users/Prasanna/Downloads/t5_model"
# drive_tokenizer_path = "c:/Users/Prasanna/Downloads/t5_nmap_tokenizer"
# from transformers import T5Tokenizer, T5ForConditionalGeneration
# tokenizer = T5Tokenizer.from_pretrained(drive_tokenizer_path)
# model = T5ForConditionalGeneration.from_pretrained(drive_model_path)

# t5_model_name = "allenai/t5-small-squad2-question-generation"
# t5_tokenizer = T5Tokenizer.from_pretrained(t5_model_name, cache_dir=project_dir)
# t5_model = T5ForConditionalGeneration.from_pretrained(t5_model_name, cache_dir=project_dir)

# bert_tokenizer = BertTokenizer.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2", cache_dir=project_dir)
# bert_model = BertForQuestionAnswering.from_pretrained("deepset/bert-large-uncased-whole-word-masking-squad2", cache_dir=project_dir)

# embedder = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=project_dir)

# evaluation_url = 'http://localhost:5003/evaluate'  

# def run_model(input_string, **generator_args):
#     input_ids = t5_tokenizer.encode(input_string, return_tensors="pt")
#     res = t5_model.generate(input_ids, **generator_args)
#     output = t5_tokenizer.batch_decode(res, skip_special_tokens=True)
#     return output

# def filter_similar_questions(questions, similarity_threshold=0.75):
#     embeddings = embedder.encode(questions, convert_to_tensor=True)
#     unique_questions = []

#     for i, question in enumerate(questions):
#         if i == 0:
#             unique_questions.append(question)
#         else:
#             is_similar = False
#             for unique_question in unique_questions:
#                 unique_embedding = embedder.encode(unique_question, convert_to_tensor=True)
#                 similarity = util.pytorch_cos_sim(embeddings[i], unique_embedding).item()
#                 if similarity > similarity_threshold:
#                     is_similar = True
#                     break
#             if not is_similar:
#                 unique_questions.append(question)

#     return unique_questions

# def get_best_answer(answers):
#     return max(answers, key=len) if answers else ""

# def clean_answer(answer):
#     return answer.strip().replace(" .", ".").replace(" ,", ",").replace("  ", " ")


# def t5_llm_answer(question):
#     print("Inside LLM")
#     inputs = tokenizer.encode("question: " + question, return_tensors="pt")
#     outputs = model.generate(inputs, max_length=128, num_beams=4, early_stopping=True)
#     predicted_answer = tokenizer.decode(outputs[0], skip_special_tokens=True)
#     return predicted_answer
    


@app.route('/api/generate', methods=['POST'])
def generate():
    data = request.get_json()  # Retrieve JSON data sent by the Node.js server
    print("Received data from Node.js:", data)

    # # Extract the individual skill
    # inp = data.get('inp', 'No input provided')
    # domain = data.get('Domain', 'No domain provided')
    skill = data.get('data', 'No skill provided')

    print(f"Processing skill: {skill}")

    # Generate questions and answers using LLaMA (Ollama)
    try:
        # Proper usage of ollama CLI
        llama_prompt = f"Generate 3 questions and answers from the paragraph '{skill}'. Only return the questions and answers in the following format: \n1. Question: [question] \n   Answer: [answer] \n2. Question: [question] \n   Answer: [answer] \n3. Question: [question] \n   Answer: [answer]. Do not include any introductory text or extra symbols."

        print(f"Prompt being sent to Ollama: {llama_prompt}")
        
        # Run Ollama process
        result = subprocess.run(
    [r'C:\Users\Prasanna\AppData\Local\Programs\Ollama\ollama.exe', 'run', 'llama3.1'],
    input=llama_prompt + "\n",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    encoding='utf-8',
    text=True,
    timeout=60
)


        # Check if the process completed successfully
        if result.returncode != 0:
            print(f"Error running ollama: {result.stderr}")
            raise Exception(result.stderr.strip())

        # Process the generated output
        questions_and_answers = result.stdout.strip()
        print(f"Generated Q&A for skill '{skill}': {questions_and_answers}")

        # Return the generated questions and answers
        return jsonify({"questions_and_answers": [questions_and_answers]})

    except subprocess.TimeoutExpired:
        print(f"Ollama process timed out for skill '{skill}'")
        return jsonify({"error": f"Processing timed out for skill '{skill}'"}), 500
    except Exception as e:
        print(f"Error generating Q&A for skill '{skill}': {e}")
        return jsonify({"error": str(e)}), 500

 

# @app.route('/api/generate', methods=['POST'])
# def generate():
#     data = request.get_json()  # Retrieve JSON data sent by the Node.js server
#     print("Received data from Node.js:", data)
#     payload = data.get('data', {})  # Use .get() to handle cases where 'data' might not exist
#     inp = payload.get('inp', 'No input provided')
#     domain = payload.get('Domain', 'No domain provided')
#     skills = payload.get('Skills', [])
    
#     print("Skills:", skills)
#     # return jsonify({"questions_and_answers": all_payload})

# @app.route('/api/generate', methods=['POST'])
# def generate():
#     print("HELLO")
#     data = request.json
#     input_string = data.get("inp", "React")
#     print("Data",input_string)
#     questions = run_model(
#         input_string,
#         num_beams=15,
#         num_return_sequences=15,
#         max_length=128,
#         early_stopping=True,
#         temperature=0.7,
#         top_p=0.85,
#         top_k=50
#     )

#     filtered_questions = filter_similar_questions(questions)
#     all_payload=[]
#     for question in filtered_questions:
#         context = input_string

#         inputs = bert_tokenizer(question, context, return_tensors="pt")

#         with torch.no_grad():
#             outputs = bert_model(**inputs)

#         start_logits = outputs.start_logits
#         end_logits = outputs.end_logits

#         top_n = 3
#         start_indices = torch.topk(start_logits, top_n).indices.squeeze()
#         end_indices = torch.topk(end_logits, top_n).indices.squeeze()

#         answers = []
#         for start_idx in start_indices:
#             for end_idx in end_indices:
#                 if end_idx >= start_idx:
#                     answer = bert_tokenizer.convert_tokens_to_string(
#                         bert_tokenizer.convert_ids_to_tokens(inputs.input_ids[0][start_idx:end_idx+1])
#                     )
#                     answers.append(clean_answer(answer))

#         best_answer = get_best_answer(answers)
        
#         # EVALUATION here
#         print(question)
        
#         llm_answer = t5_llm_answer(question)
#         # ///question should be sent to react////
        
#         # /////get answer from react////
#         can_answer ="NUll"
#         payload = {
#             "reference_answer": best_answer,   # model answer
#             "candidate_answer": can_answer,   # user answer
#             "question": question
#         }
        
#         print(payload)
#         print("------------------------------------------------------")
#         all_payload.append(payload)
#         # evaluation_response = requests.post(evaluation_url, json=payload)
#         # evaluation_result = evaluation_response.json()
         
#         # results.append({
#         #     "question": question,
#         #     "answer": best_answer,
#         #     "evaluation": evaluation_result
#         # })

#     return jsonify({"questions_and_answers": all_payload})

if __name__ == '__main__':
    app.run(debug=False , port=5004)




