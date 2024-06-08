import os
import json
import openai
from langchain_community.document_loaders import PyPDFLoader
from utils import parseResume, getResumeDetails, rankResumes
from dotenv import load_dotenv
from Prompt.prompt import prompt, rankingPrompt, jobDescriptionPrompt
load_dotenv()

RESUME_DIR = os.path.join(os.path.dirname(__file__), 'Data')
resumes = os.listdir(RESUME_DIR)

parsedResumes = []

for resume in resumes:
    print(f"Processing {resume}")
    resume_path = os.path.join(RESUME_DIR, resume)
    text = parseResume(resume_path)
    details = getResumeDetails(text, prompt)

    if details:
        print(json.dumps(details, indent=4))
        parsedResumes.append(details)


# Assign ID to each resume
for i, resume in enumerate(parsedResumes):
    resume["ID"] = i + 1

rankedResumes = rankResumes(json.dumps(parsedResumes), rankingPrompt, jobDescriptionPrompt)
print(json.dumps(rankedResumes, indent=4))