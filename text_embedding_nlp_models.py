# Importing the required package 
from sentence_transformers import SentenceTransformer

# Importing the chosen NLP model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Testing
sentences = ["This is an example sentence", "Each sentence is converted"]
embeddings = model.encode(sentences)
print(embeddings)