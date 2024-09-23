import os
from dotenv import load_dotenv, find_dotenv
from flask import Flask, render_template, request
from langchain_groq import ChatGroq
import re
import random 

load_dotenv(find_dotenv())

os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize the language model
llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0)

# Prompt template to classify complexity
def prompt_template(question):
   return f"""
You are an expert in software development. Your task is to classify the complexity of the following context into one of two categories: 
"easy/medium" or "hard." Use the criteria below to guide your classification.

Context: {question}

### Classification Criteria:
1. **Easy/Medium**:
   - Refers to topics that are basic, introductory, or involve moderate complexity.
   - These topics are relatively simple to explain and understand, typically requiring some prior knowledge but not highly advanced concepts.
   - The language used is generally clear, with few technical terms, and may include some terminology that requires moderate effort to understand.

2. **Hard**:
   - Refers to topics that are technically advanced or require a deep understanding of the subject.
   - Involves intricate details or abstract concepts that may be challenging to grasp without significant experience.
   - The language may include many technical terms, and understanding the topic may involve dealing with complex scenarios or multi-step processes.

### Instructions:
Carefully review the provided context and classify it based on the complexity required to understand or implement the concept. Provide your classification in a single word: "easy/medium" or "hard."
"""



# Function to classify the React question using the model
def classify_react_question(llm, question):
    prompt = prompt_template(question)
    # Send the prompt to the model
    response = llm.invoke(prompt)  # Updated method to use `invoke`
    return response

# Get the question from the user
question = input("Enter your React-related question: ")

# Call the function to classify the question
classification = classify_react_question(llm, question)

# Output the classification result
print(f"The complexity of the context is classified as: {classification}")
