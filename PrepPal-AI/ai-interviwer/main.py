from fastapi import FastAPI, Form, UploadFile, File, Request, HTTPException
from fastapi.responses import HTMLResponse ,FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from PyPDF2 import PdfReader
from openai import OpenAI
import os
from dotenv import load_dotenv
from gtts import gTTS
import json
import csv
import utils


# Load environment variables
load_dotenv()
client = OpenAI()

# Initialize FastAPI app and templates
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory store to hold report data and questions
interview_report = []
questions = []

# Parse PDF Resume
def parse_pdf(uploaded_resume):
    reader = PdfReader(uploaded_resume)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

# Extract information from the resume using OpenAI
def extract_resume_info(resume_text):
    prompt = (
        "Extract the following information from the resume:\n"
        "1. Name\n"
        "2. Contact Information\n"
        "3. Education\n"
        "4. Skills\n"
        "5. Experience\n\n"
        f"Resume text:\n{resume_text}\n\n"
        "Provide the information in JSON format."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return {"response": response.choices[0].message.content}

# Generate interview questions based on resume and job role
def generate_interview_question(resume_summary, job_role):
    prompt = f"""
    Generate 5 list of technical interview questions tailored for a candidate applying for the '{job_role}' position. 
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
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=1,
    )
    return response.choices[0].message.content

# Home page route to display the form for uploading resume, name, and job role
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Process the interview flow
@app.post("/start_interview/")
async def start_interview(uploaded_resume: UploadFile = File(...), name: str = Form(...), job_role: str = Form(...)):
    global interview_report, questions
    interview_report = []  # Clear any previous reports

    # Parse PDF and extract resume info
    resume_text = parse_pdf(uploaded_resume.file)
    resume_info = extract_resume_info(resume_text)
    
    # Generate interview questions
    questions = json.loads(generate_interview_question(resume_info, job_role))

    if not questions:
        raise HTTPException(status_code=400, detail="No questions generated.")

    return {
        'status': 'success',
        "name": name, 
        "job_role": job_role, 
        "current_question": questions[0],  # Start with the first question
        "question_index": 0  # Index of the current question
    }

# Endpoint to get the next question
@app.get("/next_question/{index}")
async def next_question(index: int):
    global questions
    if index < len(questions):
        return {
            'status': 'success',
            "current_question": questions[index],
            "question_index": index
        }
    else:
        return {'status': 'completed'}  # Indicates there are no more questions

# Record answer and proceed to the next question
@app.post("/record_answer")
async def record_answer(answer_data: str = Form(...), question: str = Form(...)):
    data_report=list()
    data_report = {
        "question": question,
        "answer": answer_data
    }
    interview_report.append(data_report)  # Append the Q&A pair to the report
    # Save the updated QA pairs back to the JSON file (if needed)
    with open('qa_pairs.json', 'w') as json_file:
        json.dump(interview_report, json_file, indent=4)
    print(interview_report)

    return {"status": "success", "message": "Answer recorded."}


@app.get('/generate_report')
async def match_que(interview_report=None):
    print('==============in generate report===========')
    # just for testing purpos
    with open("/home/logicrays/Documents/ai-interviwer/qa_pairs.json", "r") as que_file:
            interview_report=json.load(que_file)
    # Convert the interview report to a formatted JSON string
    # formatted_report = json.loads(interview_report)
    formatted_report = interview_report
    
    # Prepare the prompt for OpenAI
    prompt = f"""
    Evaluate the following answer based on the given question. Consider accuracy, completeness, and relevance to the topic. Provide feedback on correctness with a score between 0 and 10, where 10 is fully correct.
    note : dont use any symbol or special character in output
    Here is the interview report in List of JSON format:
    {formatted_report}
  
    Provide the feedback and score in this below JSON format for the question and answer:
    [
        {{ 
        "question": <question>,
        "answer: <answer>,
        "score": <score>,
        "feedback": "<feedback>"
        }}  
    ]
    """

    print("---openai will match---")

    # Send the request to OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o",  # Make sure "gpt-4" or another model is correct
        messages=[
            {"role": "user", "content": prompt}
        ], 
        temperature=0.5,  # Adjust the temperature based on how creative you want the feedback
    )

    # Extract the feedback and score from the response
    result = response.choices[0].message.content


    # result = result.encode('utf-8')
    json_result=json.loads(result)
    print('➡ json_result:', json_result)
    data = {"final_report": json_result, 'status':'success'}
    print('➡ data:', data)



    csv_report = utils.convert_json_to_csv(json_result)
    print('➡ csv_report:', csv_report)
    

    return {"final_report": result, 'status': 'success'}

@app.get('/download_report')
async def download_report():
    csv_file_path = '/home/logicrays/Documents/ai-interviwer/final_report.csv'  # Update this path as needed
    return FileResponse(csv_file_path, media_type='text/csv', filename='final_report.csv')
