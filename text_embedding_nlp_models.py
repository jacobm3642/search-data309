# Importing the required library
from sentence_transformers import SentenceTransformer

# Importing the chosen NLP model
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Importing pandas
import pandas as pd

# Reading in the dataset
df = pd.read_csv('arxiv_49999_papers(in).csv')

# Testing my code with the first 1000 rows
testing = df.head(1000)

# Extracting the abstracts for the embeddings

cleaned_cols = testing['abstract_cleaned']
print(cleaned_cols)

# Creating the embeddings
embeddings = model.encode(cleaned_cols)
print(f"Embeddings:\n{embeddings[:3]}")


# Checking the similarities between each vector
similarities = model.similarity(embeddings, embeddings)
print(f"Similarites:\n{similarities[:3]}")


# Checking to see if similar indices are actually similar
similar_indices = []
for j in range(len(similarities)):
  for i in range(len(similarities[j])):
    if similarities[j][i] > 0.75:
      if similarities[j][i] < 0.99999:
        similar_indices.append((j, i))

to_print = []
for item in similar_indices:
  to_print.append((embeddings[item[0]], embeddings[item[1]]))

to_test = []
for i in to_print[:5]:
  to_avg = i[0] - i[1]
  to_test.append(sum(to_avg) / len(to_avg))

print(to_test)






# # Importing the required package 
# from sentence_transformers import SentenceTransformer

# # Importing the chosen NLP model
# model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# # Testing
# sentences = ["This is an example sentence", 
#              "This is an example paragraph",
#              "Each sentence is converted", 
#              "Adding more sentences, to test timings", 
#              "Testing more and more and more", 
#              "How do you tell if sentences are similar?", 
#              "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
#              "What happens if it takes too long?",
#              "What happens if it takes too long?",
#              "It probably seemed trivial to most people, but it mattered to Tracey. She wasn't sure why it mattered so much to her, but she understood deep within her being that it mattered to her. So for the 365th day in a row, Tracey sat down to eat pancakes for breakfast.",
#              "There was only one way to do things in the Statton house. That one way was to do exactly what the father, Charlie, demanded. He made the decisions and everyone else followed without question. That was until today.",
#              "He dropped the ball. While most people would think that this was a metaphor of some type, in Joe's case it was absolutely literal. He had hopes of reaching the Major League and that dream was now it great jeopardy. All because he had dropped the ball.",
#              "There was a time when he would have embraced the change that was coming. In his youth, he sought adventure and the unknown, but that had been years ago. He wished he could go back and learn to find the excitement that came with change but it was useless. That curiosity had long left him to where he had come to loathe anything that put him out of his comfort zone."
#              ]
# embeddings = model.encode(sentences)
# # print(f"Embeddings:\n{embeddings}\n\n")

# similarities = model.similarity(embeddings, embeddings)
# # print(f"Similarites:\n{similarities}")

# similar_indices = []
# for i in range(len(similarities[7])):
#     # print(i)
#     if similarities[0][i] > 0.8:
#         if similarities[0][i] < 0.99999:
#             similar_indices.append(i)

# # print(similar_indices)

# for j in similar_indices:
#     print((embeddings[7][j], embeddings[7][0]))
