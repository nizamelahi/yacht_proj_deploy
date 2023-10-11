from os import getenv
from dotenv import load_dotenv
from flask import Flask, request
from datetime import datetime
from vector_search.vector_search import initialise
from openAI import req_GPT_finetune,req_RAG
from BARD import req_BARD

load_dotenv()
app = Flask(__name__)
datafile = getenv("processed_data")

df, model = initialise(datafile)

print("Ready")


@app.route("/ask", methods=["GET"])
def search_page():
    print("____________________")
    print("finetune request recieved")
    time1=datetime.now()
    print(request.json.get('model'))
    result=req_GPT_finetune(request.json.get('model_name'),request.json.get('query'))
    print(f"time taken: {datetime.now()-time1}")
    return {"result":result}

@app.route("/askRAG", methods=["GET"])
def search_with_RAG():
    print("____________________")
    print("RAG request recieved")
    time1=datetime.now()
    result=req_RAG(request.json.get('query'),df,model)
    print(f"time taken: {datetime.now()-time1}")
    return {"result":result}

@app.route("/askBARD", methods=["GET"])
def search_with_BARD():
    print("____________________")
    print("BARD request recieved")
    time1=datetime.now()
    result=req_BARD(request.json.get('query'))
    print(f"time taken: {datetime.now()-time1}")
    return {"result":result}



# driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7365)
