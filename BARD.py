import google.generativeai as palm
from os import getenv
from dotenv import load_dotenv

load_dotenv()
apikey = getenv("PALM_API_KEY")

palm.configure(api_key=apikey)


def req_BARD(query):
    models = [
        m
        for m in palm.list_models()
        if "generateText" in m.supported_generation_methods
    ]
    model = models[0].name
    print(f"generating using {model}")
    prompt = f"""
    You have expert knowledge about marine craft.
    please answer the following query:

    {query}
    """

    completion = palm.generate_text(
        model=model,
        prompt=prompt,
        temperature=0.2,
        # The maximum length of the response
        max_output_tokens=800,
    )

    return completion.result
