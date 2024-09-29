import os
import json
import openai
import re
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader


def parseResume(file_path):
    loader = PyPDFLoader(file_path)
    # loader = AzureAIDocumentIntelligenceLoader(
    #             api_endpoint="https://maservices-di.cognitiveservices.azure.com/",
    #             api_key=f"{os.environ['DOC_INTELLIGENCE_API_KEY']}",
    #             file_path=file_path,
    #             api_model="prebuilt-layout"
    # )
    content = loader.load()
    content = content[0].page_content
    return content


def getResumeDetails(text, prompt):
    client = openai.AzureOpenAI(
        azure_endpoint = os.environ["AZURE_ENDPOINT_GPT_4"], 
        api_key=os.environ["API_KEY_GPT_4"],  
        api_version=os.environ["API_VERSION_GPT_4"],
    )

    completion = client.chat.completions.create(
        model='gpt4o',
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


def rankResumes(text, prompt, jobDescription):
    client = openai.AzureOpenAI(
        azure_endpoint = os.environ["AZURE_ENDPOINT_GPT_4"], 
        api_key=os.environ["API_KEY_GPT_4"],  
        api_version=os.environ["API_VERSION_GPT_4"],
    )

    completion = client.chat.completions.create(
        model='gpt4o',
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"""Here are the resumes:{text} and the job description: {jobDescription}"""}
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
    


def checkParsing(text, prompt):
    client = openai.AzureOpenAI(
        azure_endpoint = os.environ["AZURE_ENDPOINT_GPT_4"], 
        api_key=os.environ["API_KEY_GPT_4"],  
        api_version=os.environ["API_VERSION_GPT_4"],
    )

    completion = client.chat.completions.create(
        model='gpt4o',
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f"""Here is the Parsed Resume:{text}"""}
        ],
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    response = completion.choices[0].message.content
    return response



def fix_json(json_string):
    # Fix common JSON errors, like missing commas
    json_string = re.sub(r'(?<=\w)\s+(?=[\{\["])', ', ', json_string)  # Add missing commas before { and [
    return json_string