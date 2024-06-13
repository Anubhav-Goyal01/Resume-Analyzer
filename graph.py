import os
import json
import openai
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph
from Prompt.prompt import jobDescriptionPrompt, rankingPrompt, prompt
from dotenv import load_dotenv
from typing import TypedDict, List
from utils import fix_json
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
load_dotenv()

# Define the state
class State(TypedDict):
    raw_resumes: List[dict]
    file_paths: List[str]
    parsed_resumes: List[dict]
    scores: dict
    id: int

def parse_resume_node(state: State):
    id = state["id"]
    file_path = state["file_paths"][id]
    id += 1
    # loader = PyPDFLoader(file_path)
    loader = AzureAIDocumentIntelligenceLoader(
                api_endpoint="https://maservices-di.cognitiveservices.azure.com/",
                api_key=f"{os.environ['DOC_INTELLIGENCE_API_KEY']}",
                file_path=file_path,
                api_model="prebuilt-layout"
    )
    content = loader.load()
    content = content[0].page_content
    raw_resumes = state["raw_resumes"]
    raw_resumes += [{"content": content}]
    return {"raw_resumes": raw_resumes, "id": id}

def get_resume_details_node(state):
    print("Getting resume details")
    parsed_resumes = state["parsed_resumes"]
    text = state["raw_resumes"][-1]["content"]
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
        response = fix_json(response)
        try:
            starting_index = response.index("{")
            ending_index = response.rindex("}") + 1
            response = response[starting_index:ending_index]
            response = json.loads(response)
            parsed_resumes += [{"details": json.dumps(response)}]
            success = True
        except Exception as e:

            print("Retrying" , e)
            print(f"Response: {response}")
            attempts += 1
            if attempts == max_retries:
                parsed_resumes += [{"details": "Could not Parse This Resume"}]

    return {"parsed_resumes": parsed_resumes}

def rank_resumes_node(state):
    try:
        parsed_resumes = state["parsed_resumes"]
        resumes = []
        scores = state["scores"]
        for i, resume in enumerate(parsed_resumes):
            try:
                details = json.loads(resume["details"])
            except:
                continue
            details["ID"] = i + 1
            resumes.append({"details": details})

        client = openai.AzureOpenAI(
            azure_endpoint = os.environ["AZURE_ENDPOINT_GPT_4"], 
            api_key=os.environ["API_KEY_GPT_4"],  
            api_version=os.environ["API_VERSION_GPT_4"],
        )

        completion = client.chat.completions.create(
            model='sfslackbot',
            messages=[
                {"role": "system", "content": rankingPrompt},
                {"role": "user", "content": f"""Here is the Resume Text:{resumes} and the job description: {jobDescriptionPrompt}"""}
            ],
            temperature=0.1,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        print("Ranking resumes")
        response = completion.choices[0].message.content
        print(response)
        try:
            starting_index = response.index("{")
            ending_index = response.rindex("}") + 1
            response = response[starting_index:ending_index]
            scores = json.loads(response)
            print("Ranking successful")
        except:
            return {"scores": "Could not Rank Resumes"}
    except Exception as e:
        print(f"Error: {e}")
        return {"scores": "Could not Rank Resumes"}
    
    return {"scores": scores}

# Directory containing resumes
RESUME_DIR = os.path.join(os.path.dirname(__file__), 'Data', "Coffeee")
resumes = os.listdir(RESUME_DIR)

# Create the graph
graph = StateGraph(State)
state = {
    "raw_resumes": [],
    "file_paths": [os.path.join(RESUME_DIR, resume) for resume in resumes],
    "id": 0,
    "parsed_resumes": [],
    "scores": {}

}

# Create a start node
graph.add_node("start", lambda state: state)

# Add nodes and edges for each resume
previous_detail_node_name = "start"

for resume in resumes:
    file_path = os.path.join(RESUME_DIR, resume)
    parse_node_name = f"parse_{resume}"
    get_details_node_name = f"details_{resume}"

    graph.add_node(parse_node_name, lambda state: parse_resume_node(state))
    graph.add_node(get_details_node_name, lambda state: get_resume_details_node(state))

    # Connect the previous detail node to the current parse node
    graph.add_edge(previous_detail_node_name, parse_node_name)
    graph.add_edge(parse_node_name, get_details_node_name)
    
    # Update the previous detail node name to the current one
    previous_detail_node_name = get_details_node_name

# Connect the last details node to the ranking node
graph.add_edge(previous_detail_node_name, "rank_resumes")

# Add the ranking node
graph.add_node("rank_resumes", lambda state: rank_resumes_node(state))

# Define the entry and finish points
graph.set_entry_point("start")
graph.set_finish_point("rank_resumes")

# Compile and run the graph
try:
    app = graph.compile()
    state = app.invoke(state)
    parsed_resumes = state["parsed_resumes"]
    scores = state["scores"]

    for resume in parsed_resumes:
        try:
            details = json.loads(resume["details"])
            print("Parsed Resume: ", json.dumps(details, indent=4))
        except:
            print("Parsing Failed for this Resume")
        else:
            print("Parsing successful")
            # print(json.dumps(details, indent=4))

    print("Scores: ", scores)

except Exception as e:
    print(f"Error: {e}")
