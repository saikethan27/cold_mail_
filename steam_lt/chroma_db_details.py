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
        existing_count = self.collection.count()
        if len(self.data) > existing_count:
            for _, row in self.data.iloc[existing_count:].iterrows():  
                self.collection.add(documents=row["Technical_skills"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(row["id"])])

    def query_links(self, skills):
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])
    
