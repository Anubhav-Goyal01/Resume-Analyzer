import os
import json
import openai
from langchain_community.document_loaders import PyPDFLoader
from utils import parseResume, getResumeDetails, rankResumes, checkParsing
from dotenv import load_dotenv
from Prompt.prompt import prompt, rankingPrompt, jobDescriptionPrompt, ParsingCheckPrompt
load_dotenv()

RESUME_DIR = os.path.join(os.path.dirname(__file__), 'Data')
resumes = os.listdir(RESUME_DIR)

parsedResumes = []


for resume in resumes:
    print(f"Processing {resume}")
    resume_path = os.path.join(RESUME_DIR, resume)
    text = parseResume(resume_path)
    details = getResumeDetails(text, prompt)

    # Check if the parsing is correct
    # check = checkParsing(details, ParsingCheckPrompt)
    # i = 0
    # while True:
    #     if "yes" in check.lower():
    #         break
    #     else:
    #         print("Parsing failed. Reparsing resume...")
    #         details = getResumeDetails(text, prompt)
    #         check = checkParsing(details, ParsingCheckPrompt)
    #         print(check)
    #         i += 1
    #         if i > 3:
    #             break

    
    if details:
        print("Parsing successful")
        print(json.dumps(details, indent=4))
        parsedResumes.append(details)
        
    else:
        print("Parsing failed")


# Assign ID to each resume
for i, resume in enumerate(parsedResumes):
    resume["ID"] = i + 1

rankedResumes = rankResumes(json.dumps(parsedResumes), rankingPrompt, jobDescriptionPrompt)
print(json.dumps(rankedResumes, indent=4))