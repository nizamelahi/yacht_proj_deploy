from sentence_transformers.util import cos_sim
from sentence_transformers import SentenceTransformer
import pickle


threshold = 0.82
# read the pickle file
def initialise(filename):
    with open(filename, "rb") as f:
        df = pickle.load(f)

    return (df, SentenceTransformer("thenlper/gte-large"))


def search(df, query, model, n=1):
    product_embedding = model.encode(
        query,
        normalize_embeddings=True,
    )
    df["similarity"] = df.embeddings.apply(
        lambda x: cos_sim(product_embedding, x)
    )

    results = df[df.similarity >= threshold]
    print(f"{len(results)} relevant results")
    results = (
        results.sort_values("similarity", ascending=False)
        .head(n)
    )

    results = results.text.tolist()
    
    return results
