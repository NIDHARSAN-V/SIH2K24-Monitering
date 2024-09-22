from flask import Flask, request, jsonify, render_template
import os
from crewai import Crew, Process, Agent, Task
from crewai_tools import WebsiteSearchTool
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq

app = Flask(__name__)

# Load environment variables
load_dotenv(find_dotenv())
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

# Create the agent
web_rag_tool = WebsiteSearchTool()

def create_search_agent(llm):
    return Agent(
        role='Information Retrieval Specialist',
        goal='Provide relevant answers to the question using web search tools.',
        backstory='A specialist in gathering accurate information from reliable sources on the web.',
        tools=[web_rag_tool],
        verbose=True,
        llm=llm,
        max_iters=15
    )

# Create the task
def create_search_task(llm, question):
    search_agent = create_search_agent(llm)
    return Task(
        description=f'Search the web for the following query: {question}. Provide the most relevant and accurate answer based on the search results.',
        expected_output='A detailed answer to the question, synthesized from the most relevant web sources.',
        agent=search_agent
    )

@app.route('/')
def home():
    return render_template('answer.html')

@app.route('/get_answer', methods=['POST'])
def get_answer():
    question = request.form.get('question')

    if not question:
        return render_template('answer.html', answer="Please enter a question.")

    # Create the agent and task
    search_agent = create_search_agent(llm)
    search_task = create_search_task(llm, question)

    # Create the crew and kickoff the process
    crew = Crew(
        agents=[search_agent],
        tasks=[search_task],
        verbose=1,
        process=Process.sequential
    )

    # Execute the task
    result = crew.kickoff()

    # Render the result in the HTML page
    return render_template('answer.html', answer=result)

if __name__ == '__main__':
    app.run(debug=True, port=8000)
