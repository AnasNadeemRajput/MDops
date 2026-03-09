from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):

    vector = model.encode(text)

    return np.array(vector).astype("float32")