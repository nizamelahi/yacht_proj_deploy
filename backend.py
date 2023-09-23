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
    time1=datetime.now()
    completion = openai.ChatCompletion.create(
        # model="ftjob-7AAdc2Ij1jXelbewV0XT9ypu",
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "you are a helpful guide to boat related queries."}, {"role": "user", "content": f"tell me something about {request.json.get('query')}"}]

    )
    print(f"time taken: {datetime.now()-time1}")
    return {"result":completion.choices[0].message["content"]}



# driver function
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7365)
