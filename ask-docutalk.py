import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

# 1. Setup ChromaDB and Gemini Client
chroma_client = chromadb.PersistentClient(path="./my_vectordb")
collection = chroma_client.get_collection(name="japan_travel_docs")
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- DocuTalk-AI is Ready! ---")
print("Type 'exit' or 'quit' to stop.")

while True:
    # 2. Get User Input
    query = input("\nAsk a question about the Japan Guide: ")
    
    # Allow user to exit the loop
    if query.lower() in ['exit', 'quit']:
        print("Goodbye!")
        break

    # 3. RETRIEVAL: Find relevant chunks
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
    retrieved_context = "\n".join(results['documents'][0])

    # 4. GENERATION: Ask Gemini
    prompt = f"""
    You are a helpful travel assistant. Answer the user's question using ONLY the context provided below.
    If the answer is not in the context, say "I'm sorry, I don't have that information in the guide."

    CONTEXT:
    {retrieved_context}

    QUESTION:
    {query}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=prompt
    )

    print("\nAI RESPONSE:")
    print(response.text)
    print("-" * 30)