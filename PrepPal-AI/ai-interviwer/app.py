import streamlit as st
import PyPDF2
from openai import OpenAI
import os
from dotenv import load_dotenv
import ast
from gtts import gTTS
from playsound import playsound
import json
import speech_recognition as sr
load_dotenv()
client = OpenAI()



# Import necessary libraries (if any, e.g., OpenAI client)
# from your_openai_client import client

def generate_interview_question(resume_summary, job_role):
    prompt = f"""
    Generate a list of technical interview questions tailored for a candidate applying for the '{job_role}' position. 
    Base the questions on the candidate's experience, as summarized in: '{resume_summary}', with a focus on skills relevant to the job role. 
    Provide the questions in list format, with no preamble or numbering.

    Example:
    [
    "First question",
    "Second question",
    "Third question"
    ]
    """

    response = client.chat.completions.create(
        model="gpt-4o",  # or "text-davinci-003" depending on the model
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )
    
    return {"questions": response.choices[0].message.content.strip().split("\n")}


def generate_followup_questions(answer, job_role):
    prompt = f"""
    Based on the following candidate answer: '{answer}', generate relevant follow-up questions for a '{job_role}' position. 
    The questions should seek deeper insights into the candidate's knowledge, skills, or experiences related to their answer. 
    Provide the follow-up questions in list format, with no preamble or numbering.

    Example:
    [
    "Can you elaborate on how you handled that situation?",
    "What specific tools or methods did you use?",
    "How did you measure the success of that project?"
    ]
    """
    
    response = client.chat.completions.create(
        model="gpt-4o",  # or "text-davinci-003" depending on the model
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,
    )
    
    return {"followup_questions": response.choices[0].message.content.strip().split("\n")}


def conduct_interview(resume_summary, job_role):
    # Step 1: Generate initial interview questions
    initial_questions_response = generate_interview_question(resume_summary, job_role)
    initial_questions = initial_questions_response["questions"]

    # For each question, simulate asking the candidate and receiving an answer
    for question in initial_questions:
        print("Interviewer:", question)
        
        # Capture the candidate's answer
        candidate_answer = input("Candidate's answer: ")  # Replace with actual input capture

        # Step 2: Generate follow-up questions based on the candidate's answer
        followup_questions_response = generate_followup_questions(candidate_answer, job_role)
        followup_questions = followup_questions_response["followup_questions"]
        
        # Display follow-up questions
        for followup in followup_questions:
            print("Follow-up:", followup)


# Example usage
resume_summary = "Experienced software engineer with expertise in Python, Java, and machine learning."
job_role = "Software Engineer"
conduct_interview(resume_summary, job_role)
