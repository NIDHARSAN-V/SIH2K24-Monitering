# agents.py
from crewai import Agent
from crewai_tools import RagTool, WebsiteSearchTool

def create_detail_extraction_agent(llm):
    return Agent(
        role='Technical Term Extractor',
        backstory='This agent extracts technical terms from input text for further analysis.',
        goal='Extract technical terms from the input text.',
        tools=[],  # Add any specific tools needed for extraction if available
        verbose=True,
        llm=llm
    )

def create_context_fetching_agent(llm):
    rag_tool = RagTool()  # Assuming RagTool is for fetching related information
    website_search_tool = WebsiteSearchTool()
    
    return Agent(
        role='Context Fetcher',
        backstory='This agent fetches relevant contexts or information related to technical terms.',
        goal='Fetch relevant contexts or information related to technical terms.',
        tools=[rag_tool, website_search_tool],
        verbose=True,
        llm=llm
    )



# main.py
import os
from crewai import Crew
from dotenv import load_dotenv, find_dotenv
from langchain_groq import ChatGroq
from tasks import create_technical_term_extraction_task, create_context_fetching_task

# Load environment variables
load_dotenv(find_dotenv())
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

def main():
    user_input = input("Enter your answer: ")
    
    # Create technical term extraction task
    technical_term_task = create_technical_term_extraction_task(llm, user_input)
    technical_terms = technical_term_task  # Use returned value directly or adjust based on actual method
    
    if not technical_terms:
        print("No technical terms found.")
        return
    
    print(f"Technical terms found: {technical_terms}")
    
    # Create context fetching task
    context_fetching_task = create_context_fetching_task(llm, technical_terms)
    contexts = context_fetching_task  # Use returned value directly or adjust based on actual method
    
    print(f"Contexts for technical terms: {contexts}")

if __name__ == "__main__":
    main()




# tasks.py
from crewai import Task
from agents import create_detail_extraction_agent, create_context_fetching_agent

def create_technical_term_extraction_task(llm, user_input):
    agent = create_detail_extraction_agent(llm)
    # Define a task or function to process the input using the agent
    task = Task(
        description=f'Extract technical terms from the following input: "{user_input}".',
        expected_output='A list of technical terms found in the input.',
        agent=agent
    )
    # Assuming the agent has a method to handle the task
    return agent.execute_task(task)  # Modify this based on actual method available

def create_context_fetching_task(llm, technical_terms):
    agent = create_context_fetching_agent(llm)
    terms_query = " ".join(technical_terms)
    task = Task(
        description=f'Fetch relevant contexts for the following terms: {terms_query}.',
        expected_output='Contexts or information related to the technical terms.',
        agent=agent
    )
    # Assuming the agent has a method to handle the task
    return agent.execute_task(task)  # Modify this based on actual method available
