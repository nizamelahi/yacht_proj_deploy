import pandas as pd
from sentence_transformers import SentenceTransformer
from datetime import datetime
import pickle
import json

input_datapath = "data/yacht_training_data.json"
outfile_path = "data/stored_embeddings_text.pkl"

with open(input_datapath, "rb") as f:
    data = json.load(f)

datalst = []
for key in data:
    for text in data[key]:
        datalst.append([key, text])
df = pd.DataFrame(datalst, columns=["article_name", "text"])
df = df.dropna()

model = SentenceTransformer("thenlper/gte-large")

df["n_tokens"] = df.text.apply(lambda x: len(x)/4)
# df = df[df.n_tokens <= max_length]

starttime = datetime.now()
df["embeddings"] = df.text.apply(
    lambda x: model.encode(x, normalize_embeddings=True, show_progress_bar=True)
)

picklefile = open(outfile_path, "wb")
# pickle the dataframe
pickle.dump(df, picklefile)
# close file
picklefile.close()

print(f"{len(df)} embeddings calculated in ")
print(f"{(datetime.now()-starttime).total_seconds()} seconds")


# query_embeddings = model.encode(query)
# corpus_embeddings = model.encode(corpus)
# similarities = cosine_similarity(query_embeddings,corpus_embeddings)
# retrieved_doc_id = np.argmax(similarities)
# print(retrieved_doc_id)
