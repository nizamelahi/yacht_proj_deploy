from os import getenv
from dotenv import load_dotenv
from flask import Flask, request
from datetime import datetime
from vector_search.vector_search import initialise
from openAI import req_GPT_finetune,req_RAG
from PALM import req_PALM

load_dotenv()
app = Flask(__name__)
datafile = getenv("processed_data")

df, model = initialise(datafile)

print("Ready")


@app.route("/askGPT", methods=["GET"])
def search_page():
    print("____________________")
    print("GPT request recieved")
    time1=datetime.now()
    result=req_GPT_finetune(request.json.get('model_name'),request.json.get('query'),request.json.get('concise'))
    print(f"time taken: {datetime.now()-time1}")
    return {"result":result}

@app.route("/askRAG", methods=["GET"])
def search_with_RAG():
    print("____________________")
    print("RAG request recieved")
    time1=datetime.now()
    result=req_RAG(request.json.get('query'),df,model,request.json.get("combined"))
    print(f"time taken: {datetime.now()-time1}")
    return {"result":result}

@app.route("/askPALM", methods=["GET"])
def search_with_PALM():
    print("____________________")
    print("PALM request recieved")
    time1=datetime.now()
    result=req_PALM(request.json.get('query'))
    print(f"time taken: {datetime.now()-time1}")
    return {"result":result}



# driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7365)
