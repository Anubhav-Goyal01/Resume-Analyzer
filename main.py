import os
import json
import openai
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from Prompt.prompt import prompt
load_dotenv()

RESUME_DIR = os.path.join(os.path.dirname(__file__), 'Data')
resumes = os.listdir(RESUME_DIR)


def parseResume(file_path):
    loader = PyPDFLoader(file_path)
    content = loader.load()
    return content


def getResumeDetails(text, prompt):
    client = openai.AzureOpenAI(
        azure_endpoint = os.environ["AZURE_ENDPOINT_GPT_4"], 
        api_key=os.environ["API_KEY_GPT_4"],  
        api_version=os.environ["API_VERSION_GPT_4"],
    )

    completion = client.chat.completions.create(
        model='sfslackbot',
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"""Here is the Resume Text:{text}"""}
        ],
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    response = completion.choices[0].message.content
    try:
        starting_index = response.index("{")
        ending_index = response.rindex("}") + 1
        response = response[starting_index:ending_index]
        response = json.loads(response)
        return response
    except:
        return None



for resume in resumes:
    print(f"Processing {resume}")
    resume_path = os.path.join(RESUME_DIR, resume)
    text = parseResume(resume_path)
    details = getResumeDetails(text, prompt)


    if details:
        print(json.dumps(details, indent=4))


