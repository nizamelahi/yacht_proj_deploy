from os import getenv
from dotenv import load_dotenv
from flask import Flask, request
import openai
from datetime import datetime


load_dotenv()
# creating a Flask app
app = Flask(__name__)
datafile = getenv("processed_data")
openai.api_key = getenv('OPENAI_API_KEY')

print("Ready")


@app.route("/ask", methods=["GET"])
def searchpage():
    print("request recieved")
    time1=datetime.now()
    print(request.json.get('model'))
    if not request.json.get('model'):
        model="gpt-3.5-turbo"
    else:
        model="ft:gpt-3.5-turbo-0613:personal::81lwdC3E"

    completion = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "system", "content": "you are a helpful guide to boat related queries."}, {"role": "user", "content": f"{request.json.get('query')}"}],
        temperature=0.2
    )
    print(f"time taken: {datetime.now()-time1}")
    return {"result":completion.choices[0].message["content"]}



# driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7365)
