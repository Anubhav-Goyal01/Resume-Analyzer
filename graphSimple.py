import os
import json
import openai
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph
from Prompt.prompt import prompt
from dotenv import load_dotenv
from typing import TypedDict, List
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
load_dotenv()




# Define the state
class State(TypedDict):
    raw_resume: dict
    file_path: str
    parsed_resume: dict

def parse_resume_node(state: State):
    file_path = state["file_path"]
    # loader = PyPDFLoader(file_path)
    loader = AzureAIDocumentIntelligenceLoader(
                api_endpoint="https://maservices-di.cognitiveservices.azure.com/",
                api_key=f"{os.environ['DOC_INTELLIGENCE_API_KEY']}",
                file_path=file_path,
                api_model="prebuilt-layout"
            )
    content = loader.load()
    print(content)
    content = content[0].page_content
    raw_resume = state["raw_resume"]
    raw_resume = {"content": content}
    return {"raw_resume": raw_resume}

def get_resume_details_node(state):
    try:
        print("Getting resume details")
        parsed_resume = state["parsed_resume"]
        text = state["raw_resume"]["content"]
        client = openai.AzureOpenAI(
            azure_endpoint=os.environ["AZURE_ENDPOINT_GPT_4"], 
            api_key=os.environ["API_KEY_GPT_4"],  
            api_version=os.environ["API_VERSION_GPT_4"],
        )

        max_retries = 3
        attempts = 0
        success = False
        response = None
        while attempts < max_retries and not success:
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
                parsed_resume = {"details": json.dumps(response)}
                success = True
            except Exception as e:
                print("Retrying" , e)
                print(f"Response: {response}")
                attempts += 1
                if attempts == max_retries:
                    parsed_resume = {"details": "Could not Parse This Resume"}

        return {"parsed_resume": parsed_resume}
    except Exception as e:
        print(f"Error: {e}")
        return {"parsed_resume": "Could not Parse This Resume"}

# Directory containing resumes
RESUME_DIR = os.path.join(os.path.dirname(__file__), 'Data', "Coffeee")
# Fetch first resume
resumes = os.listdir(RESUME_DIR)
file_path = os.path.join(RESUME_DIR, resumes[0])

# Create the graph
graph = StateGraph(State)
state = {
    "raw_resume": {},
    "file_path": file_path,
    "parsed_resume": {},

}

# Create a start node
graph.add_node("start", lambda state: state)

# Add nodes and edges for resume
graph.add_node("parse_resume", lambda state: parse_resume_node(state))
graph.add_node("get_resume_details", lambda state: get_resume_details_node(state))

graph.add_edge("start", "parse_resume")
graph.add_edge("parse_resume", "get_resume_details")

graph.set_entry_point("start")
graph.set_finish_point("get_resume_details")

# Compile and run the graph
try:
    app = graph.compile()
    state = app.invoke(state)
    parsed_resume = state["parsed_resume"]["details"]
    print("Parsed Resume: ", json.dumps(json.loads(parsed_resume), indent=4))
except Exception as e:
    print(f"Error: {e}")
    print("Could not Parse Resume")
