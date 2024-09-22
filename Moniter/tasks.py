# tasks.py
from crewai import Task
from agents import create_detail_extraction_agent, create_question_generation_agent

def create_technical_term_extraction_task(llm, user_input):
    agent = create_detail_extraction_agent(llm)
    task = Task(
        description=f'Extract technical terms from the following input: "{user_input}".',
        expected_output='A list of technical terms found in the input.',
        agent=agent
    )
    # Assuming agent has a method to handle the task
    return agent.execute_task(task)

def create_question_generation_task(llm, technical_terms):
    agent = create_question_generation_agent(llm)
    terms_query = " ".join(technical_terms)
    task = Task(
        description=f'Generate follow-up questions related to the following terms: {terms_query}.',
        expected_output='A list of follow-up questions based on the technical terms.',
        agent=agent
    )
    # Assuming agent has a method to handle the task
    return agent.execute_task(task)
