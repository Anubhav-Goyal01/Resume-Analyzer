import os
import json
import openai
from langchain_community.document_loaders import PyPDFLoader
from langgraph.graph import StateGraph
from Prompt.prompt import jobDescriptionPrompt, rankingPrompt, prompt
from dotenv import load_dotenv
from typing import TypedDict, List, Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage
load_dotenv()

# Define the state
class State(TypedDict):
    messages: Annotated[List[dict], add_messages]

def parse_resume_node(file_path):
    def node(state: State):
        loader = PyPDFLoader(file_path)
        content = loader.load()
        state["messages"].append({"role": "user", "content": content})
        return state
    return node

def get_resume_details_node():
    def node(state):
        text = state["messages"][-1].content
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
            state["messages"].append({"role": "assistant", "content": json.dumps(response)})
            print("Parsing successful")
        except:
            state["messages"].append({"role": "assistant", "content": ""})
        return state
    return node

def rank_resumes_node():
    def node(state):
        resumes = []
        for msg in state["messages"]:
            try:
                if msg.role == "assistant":
                    resumes.append(msg.content)
            except:
                continue
        print(resumes)
        resumes_json = json.dumps(resumes)
        client = openai.AzureOpenAI(
            azure_endpoint = os.environ["AZURE_ENDPOINT_GPT_4"], 
            api_key=os.environ["API_KEY_GPT_4"],  
            api_version=os.environ["API_VERSION_GPT_4"],
        )

        completion = client.chat.completions.create(
            model='sfslackbot',
            messages=[
                {"role": "system", "content": rankingPrompt},
                {"role": "user", "content": f"""Here is the Resume Text:{resumes_json} and the job description: {jobDescriptionPrompt}"""}
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
            response = json.loads(response)
            state["messages"].append({"role": "assistant", "content": json.dumps(response)})
            print("Ranking successful")
        except:
            state["messages"].append({"role": "assistant", "content": "Ranking failed"})
        return state
    return node

# Directory containing resumes
RESUME_DIR = os.path.join(os.path.dirname(__file__), 'Data', "Coffeee")
resumes = os.listdir(RESUME_DIR)

# Create the graph
graph = StateGraph(State)
global state
state = {"messages": []}

# Create a start node
graph.add_node("start", lambda state: state)

# Add nodes and edges for each resume
previous_detail_node_name = "start"

for resume in resumes:
    file_path = os.path.join(RESUME_DIR, resume)
    parse_node_name = f"parse_{resume}"
    get_details_node_name = f"details_{resume}"

    graph.add_node(parse_node_name, parse_resume_node(file_path))
    graph.add_node(get_details_node_name, get_resume_details_node())

    # Connect the previous detail node to the current parse node
    graph.add_edge(previous_detail_node_name, parse_node_name)
    graph.add_edge(parse_node_name, get_details_node_name)
    
    # Update the previous detail node name to the current one
    previous_detail_node_name = get_details_node_name

# Connect the last details node to the ranking node
graph.add_edge(previous_detail_node_name, "rank_resumes")

# Add the ranking node
graph.add_node("rank_resumes", rank_resumes_node())


# Define the entry and finish points
graph.set_entry_point("start")
graph.set_finish_point("rank_resumes")
# Compile and run the graph
try:
    app = graph.compile()
    app.invoke(state)
    # Collect results
    parsed_resumes = []
    print(f"State: {state}")
    for msg in state["messages"]:
        parsed_resumes.append(msg.content)
    # Assign ID to each resume
    for i, resume in enumerate(parsed_resumes):
        print(i)
        resume["ID"] = i + 1

    # Rank the resumes
    rank_state = {"messages": [{"role": "system", "content": json.dumps(parsed_resumes)}]}
    ranked_resumes = rank_resumes_node()(state=rank_state)
    print(json.dumps(json.loads(ranked_resumes["messages"][-1].content), indent=4))

except Exception as e:
    print(f"Error: {e}")
