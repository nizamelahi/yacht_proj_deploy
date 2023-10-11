from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
from vector_search.vector_search import search

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4")


def augment_prompt(query: str,df, model):
    results = search(df, query, model)
    source_knowledge = "\n".join(results)
    augmented_prompt = f"""Using the contexts below, answer the query.

    Contexts:
    {source_knowledge}

    Query: {query}"""
    return augmented_prompt


def req_GPT_finetune(model_name, query):
    if model_name == "GPT3.5(untuned)":
        model = "gpt-3.5-turbo"
        print("gpt")
    elif model_name == "finetuned(short)":
        model = "ft:gpt-3.5-turbo-0613:personal::81lwdC3E"  # split paragraph model
    else:
        model = "ft:gpt-3.5-turbo-0613:personal::825r15TO"  # combined paragraph model

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "you are a helpful guide to boat related queries.",
            },
            {
                "role": "user",
                "content": f"please give a short, concise answer to the following query: {query}",
            },
        ],
        temperature=0.2,
    )
    return completion.choices[0].message["content"]


def req_RAG(query,df, model):
    messages = [
        SystemMessage(content="you are a helpful guide to boat related queries")
    ]
    prompt = HumanMessage(content=augment_prompt(query,df, model))
    messages.append(prompt)
    res = chat(messages)
    
    return res.content
