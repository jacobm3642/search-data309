# Importing the required library
from sentence_transformers import SentenceTransformer

# Importing the chosen NLP model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Reading in the dataset
import pandas as pd
df = pd.read_csv('arxiv_49999_papers(in).csv')

# Creating an embedding function that works for any string
list_of_embeddings = []
def embed(a_string):
  embedding = model.encode(a_string)
  list_of_embeddings.append(embedding)


# Testing my code with the first 1000 rows
testing = df.head(1000)

# Extracting the cleaned abstracts for the embeddings
cleaned_cols = testing['abstract_cleaned']
print(f"First few cleaned abstracts:\n{cleaned_cols[:5]}")

# Creating the embeddings
for i in cleaned_cols:
  embed(i)
print(f"First embedding:\n{list_of_embeddings[0]}")

# Checking that the embeddings are already normalised
import numpy as np
sq_vals = 0
for i in list_of_embeddings[0]:
  sq_vals += (i ** 2)

print(f"Euclidean norm:\n{np.sqrt(sq_vals)}")

# Checking the similarities between each vector
similarities = model.similarity(list_of_embeddings, list_of_embeddings)
print(f"Similarites:\n{similarities[:3]}")


### Checking to see if similar indices are actually similar

# First check that the similarity between two abstracts is between 0.75 and 1 (excluding 1 as this when it is matched to itself)
similar_indices = []
for j in range(len(similarities)):
   for i in range(len(similarities[j])):
     if similarities[j][i] > 0.75:
       if similarities[j][i] < 0.99999:
          similar_indices.append((j, i))

# Then extracting the embeddings associated with each of the abstracts
to_print = []
for item in similar_indices:
  to_print.append((list_of_embeddings[item[0]], list_of_embeddings[item[1]]))

# Then averaging the difference between the two abstracts to ensure that they're actually similar
to_test = []
for i in to_print[:5]:
  diff = i[0] - i[1]
  to_test.append(sum(diff) / len(diff))

print(to_test)

# Also print the actual abstracts to manually verify that they're the same
for item in similar_indices[:5]:
  print(f"items:\n{cleaned_cols.iloc[item[0]]}\n\n{cleaned_cols.iloc[item[1]]}\n\n\n\n")
