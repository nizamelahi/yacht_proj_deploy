from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import ChatOpenAI
import openai
import os
from dotenv import load_dotenv
from vector_search.vector_search import search

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
chat = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-4", temperature=0.2
)


def augment_prompt(query: str, df, model, combined):
    results = search(df, query, model)
    source_knowledge = "\n".join(results)
    print(source_knowledge)
    if combined:
        augmented_prompt = f"""Using the contexts below, answer the query as concisely as possible.
        if information in the contexts is insufficient,use your knowledge of boats to answer the query.
        
        Contexts:
        {source_knowledge}

        Query: {query}"""
    else:
        augmented_prompt = f"""Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {query}"""
    return augmented_prompt


def req_GPT_finetune(model_name, query, concise):
    if model_name == "GPT4(untuned)":
        model = "gpt-4"
    elif model_name == "finetuned-gpt3.5(short)":
        model = "ft:gpt-3.5-turbo-0613:personal::81lwdC3E"  # split paragraph model
    else:
        model = "ft:gpt-3.5-turbo-0613:personal::825r15TO"  # combined paragraph model

    if concise:
        modifier = "give a short, concise answer to"
    else:
        modifier = "answer"

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "you are a helpful guide to boat related queries.",
            },
            {
                "role": "user",
                "content": f"please {modifier} the following query: {query}",
            },
        ],
        temperature=0.2,
    )
    return completion.choices[0].message["content"]


def req_RAG(query, df, model, combined):
    messages = [
        SystemMessage(content="you are a helpful guide to boat related queries")
    ]
    prompt = HumanMessage(content=augment_prompt(query, df, model, combined))
    messages.append(prompt)
    res = chat(messages)

    return res.content
