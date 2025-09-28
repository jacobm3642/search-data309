## Importing the required libraries
import time
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np


## Importing the chosen NLP model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

## Creating an embedding function that works for any string
def embed(a_string):
  embedding = model.encode(a_string)
  return embedding

## Creating a similarity function that works for any list of strings
def similarities(embedding_list):
  similar_list = model.similarity(embedding_list, embedding_list)
  return similar_list

## Creating a main function so that my testing doesn't run automatically!
def main():
  ## Reading in the dataset
  df = pd.read_csv('arxiv_49999_papers(in).csv')
  
  # Checking how long my code takes to run
  start = time.time()

  # Testing my code with the first 10000 rows
  testing = df.head(1000)

  # Extracting the cleaned abstracts for the embeddings
  cleaned_cols = testing['abstract_cleaned']
  print(f"First few cleaned abstracts:\n{cleaned_cols[:5]}")

  # Creating the embeddings
  list_of_embeddings = []
  for i in cleaned_cols:
    list_of_embeddings.append(embed(i))
  print(f"First embedding:\n{list_of_embeddings[0]}\n\n")

  # Checking that the embeddings are already normalised
  sq_vals = 0
  for i in list_of_embeddings[0]:
    sq_vals += (i ** 2)

  print(f"Euclidean norm:\n{np.sqrt(sq_vals)}\n\n")

  # Checking the similarities between each vector
  similarity_test = similarities(list_of_embeddings)
  print(f"First three similarites:\n{similarity_test[:3]}\n\n")


  ## Checking to see if similar indices are actually similar

  # First check that the similarity between two abstracts is below 0.15, or between 0.85 and 1 (excluding 1 as this when it is matched to itself)
  similar_indices = []
  dissimilar_indices = []

  for j in range(len(similarity_test)):
    for i in range(len(similarity_test[j])):
      if len(dissimilar_indices) < 3:
        if similarity_test[j][i] < 0.15:
          dissimilar_indices.append((j, i))
      elif len(similar_indices) < 3:
        if similarity_test[j][i] > 0.85:
          if similarity_test[j][i] < 0.99999:
            similar_indices.append((j, i))

  # Print the first three similar abstracts to manually verify that they're the same
  for item in similar_indices:
    print(f"Similar items:\n{cleaned_cols.iloc[item[0]]}\n\n{cleaned_cols.iloc[item[1]]}\n\n")

  ## Dissimilarity:
  # Print the first three dissimilar abstracts to manually verify that they're dissimilar
  for item in dissimilar_indices:
    print(f"Dissimilar items:\n{cleaned_cols.iloc[item[0]]}\n\n{cleaned_cols.iloc[item[1]]}\n\n")

  # Checking how long my code takes to run 
  end = time.time()
  print(f"Length of time:\n{end - start}")

# Ensuring that the entire file doesn't compile when called
if __name__ == "__main__":
  main()
