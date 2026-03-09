import faiss
import numpy as np
from services.embeddings import create_embedding


class PatientVectorStore:

    def __init__(self):

        self.dimension = 384
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []

    def add_document(self, text):

        vector = create_embedding(text)

        self.index.add(np.array([vector]))

        self.documents.append(text)

    def search(self, query, k=3):

        query_vector = create_embedding(query)

        distances, indices = self.index.search(np.array([query_vector]), k)

        results = []

        for idx in indices[0]:
            if idx < len(self.documents):
                results.append(self.documents[idx])

        return results