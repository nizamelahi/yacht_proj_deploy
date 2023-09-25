from os import getenv
from dotenv import load_dotenv
from flask import Flask, request
from langchain.schema import (
    SystemMessage,
    HumanMessage,
    AIMessage
)
from langchain.chat_models import ChatOpenAI
import openai
from datetime import datetime
from vector_search.vector_search import search, initialise

load_dotenv()
# creating a Flask app
app = Flask(__name__)
datafile = getenv("processed_data")
openai.api_key = getenv('OPENAI_API_KEY')
df, model = initialise(datafile)

chat = ChatOpenAI(
    openai_api_key=getenv('OPENAI_API_KEY'),
    model='gpt-3.5-turbo'
)
messages = [
    SystemMessage(content="you are a helpful guide to boat related queries"),
    HumanMessage(content="Hi AI, how are you today?"),
    AIMessage(content="I'm great thank you. How can I help you?")
]
print("Ready")


def augment_prompt(query: str):
    results=search(df,request.json.get('query'),model)
    source_knowledge = "\n".join(results)
    augmented_prompt = f"""Using the contexts below, answer the query.

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augmented_prompt




@app.route("/ask", methods=["GET"])
def search_page():
    print("____________________")
    print("finetune request recieved")
    time1=datetime.now()
    print(request.json.get('model'))
    if  request.json.get('model') == "GPT3.5(untuned)":
        model="gpt-3.5-turbo"
        print("gpt")
    elif request.json.get('model') == "finetuned(short)":
        model="ft:gpt-3.5-turbo-0613:personal::81lwdC3E"  #split paragraph model
    else:
        model="ft:gpt-3.5-turbo-0613:personal::825r15TO"    #combined paragraph model

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "you are a helpful guide to boat related queries."}, {"role": "user", "content": f"please give a short, concise answer to the following query: {request.json.get('query')}"}],
        temperature=0.2
    )
    print(f"time taken: {datetime.now()-time1}")
    return {"result":completion.choices[0].message["content"]}

@app.route("/askRAG", methods=["GET"])
def search_with_RAG():
    print("____________________")
    print("RAG request recieved")
    time1=datetime.now()
    prompt = HumanMessage(
    content=augment_prompt(request.json.get('query'))
    )
    messages.append(prompt)

    res = chat(messages)
    print(f"time taken: {datetime.now()-time1}")
    return {"result":res.content}




# driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7365)
