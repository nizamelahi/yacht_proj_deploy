import pandas as pd
from sentence_transformers import SentenceTransformer
from datetime import datetime
import pickle
import json

input_datapath_blogs = "data/blog_data.json"
input_datapath_listings = "data/listings_cleaned.json"

outfile_path = "data/stored_embeddings_text.pkl"

with open(input_datapath_blogs, "rb") as f:
    data_blogs = json.load(f)
with open(input_datapath_listings, "rb") as f:
    data_listings = json.load(f)

datalst = []
for key in data_blogs:
    for text in data_blogs[key]:
        datalst.append(text)
df_blog = pd.DataFrame(datalst, columns=["text"])
df_blog = df_blog.dropna()

yacht_listings = []
for name in data_listings:
    listing_str=f'{name}\n'
    for key in data_listings[name]:
        if not (data_listings[name][key] in ["","()"]):
            listing_str=listing_str+f'{key} : {",".join(data_listings[name][key])}\n'
    yacht_listings.append(listing_str)
df_listings = pd.DataFrame(yacht_listings, columns=["text"])
df_listings= df_listings.dropna()

frames = [df_blog,df_listings]
        
df = pd.concat(frames)

model = SentenceTransformer("thenlper/gte-large")

df["n_tokens"] = df.text.apply(lambda x: len(x) / 4)
# df = df[df.n_tokens <= max_length]

starttime = datetime.now()
df["embeddings"] = df.text.apply(
    lambda x: model.encode(x, normalize_embeddings=True, show_progress_bar=True)
)

with open(outfile_path, "wb") as pf:
    pickle.dump(df, pf)

print(f"{len(df)} embeddings calculated in ")
print(f"{(datetime.now()-starttime).total_seconds()} seconds")

