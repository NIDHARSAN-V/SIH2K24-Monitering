# agents.py
from crewai import Agent
from crewai_tools import RagTool, WebsiteSearchTool

def create_detail_extraction_agent(llm):
    return Agent(
        role='Technical Term Extractor',
        backstory='Extract technical terms from user input for further analysis.',
        goal='Identify and extract technical terms from the provided text.',
        tools=[],
        verbose=True,
        llm=llm
    )

def create_question_generation_agent(llm):
    return Agent(
        role='Follow-up Question Generator',
        backstory='Generate logical and challenging follow-up questions based on the user input and extracted terms.',
        goal='Create thoughtful follow-up questions related to the technical terms and context.',
        tools=[],
        verbose=True,
        llm=llm
    )
