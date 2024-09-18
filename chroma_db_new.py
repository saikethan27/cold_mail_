# import chromadb

# # Initialize the ChromaDB client
# client = chromadb.Client()

# # Create a collection
# collection = client.create_collection("cities")

# # Add documents to the collection
# collection.add(
#     documents=[
#         "Mumbai is a great city",
#         "New York is not better than Mumbai",
#         "Hyderabad is a better city than Mumbai"
#     ],
#     ids=['id1', 'id2', 'id3']
# )

# # Access the collection
# collection = client.get_collection("cities")

# # Query the collection
# results = collection.query(
#     query_texts=["best city in the world"],
#     n_results=3
# )
# print(results)


import pandas as pd
import chromadb
import uuid


class Portfolio:
    def __init__(self, file_path="steam_lt\my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        print(len(self.data),self.collection.count())
        if len(self.data) > self.collection.count():
            for _, row in self.data.iterrows():
                print(row)
                self.collection.add(documents=row["Technical_skills"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(row["id"])])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
    
portfolio = Portfolio()
portfolio.load_portfolio()
results = portfolio.query_links(skills=["Python", "Django"])
print(results)
