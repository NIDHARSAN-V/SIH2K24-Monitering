import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from langchain_groq import ChatGroq
from tasks import create_technical_term_extraction_task, create_question_generation_task
import re
import random  # Import random module

# Load environment variables
load_dotenv(find_dotenv())
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

# Create Flask app
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        user_input = request.form['answer']

        # Create technical term extraction task
        technical_terms = create_technical_term_extraction_task(llm, user_input)

        if not technical_terms:
            technical_terms = ["No technical terms found."]
            follow_up_question = "No questions generated."
        else:
            # Create follow-up question generation task
            follow_up_question = create_question_generation_task(llm, technical_terms)
        
        # Split the follow-up questions
        follow_up_questions = re.split('\d+\.\s', follow_up_question)[1:]
        
        # Select a random question
        if follow_up_questions:
            random_question = random.choice(follow_up_questions)
        else:
            random_question = "No questions available."

        return render_template('index.html', 
                               technical_terms=technical_terms, 
                               random_question=random_question,
                               follow_up_questions=follow_up_questions) 

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=7000)
