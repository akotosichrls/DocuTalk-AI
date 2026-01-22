import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize ChromaDB (This creates a folder called 'my_vectordb')
chroma_client = chromadb.PersistentClient(path="./my_vectordb")

# 2. Create a 'Collection' (Like a table in a database)
collection = chroma_client.get_or_create_collection(name="japan_travel_docs")

# 3. Add a test chunk to our database
# In a real RAG, we would turn the text into an 'embedding' first.
collection.add(
    documents=["Tokyo is famous for its neon lights and sushi."],
    ids=["id1"]
)

print("Sumakses! ChromaDB is initialized and your first chunk is saved.")