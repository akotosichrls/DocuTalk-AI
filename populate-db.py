import os
import chromadb
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Setup ChromaDB
chroma_client = chromadb.PersistentClient(path="./my_vectordb")
collection = chroma_client.get_or_create_collection(name="japan_travel_docs")

# 2. Extract Text from your specific PDF
pdf_path = "eat_japan_jnto_2017_unlayi.pdf"
reader = PdfReader(pdf_path)
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

# 3. Chunk the Text
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_text(full_text)

# 4. Add all chunks to the Database
# We give each chunk a unique ID (chunk_0, chunk_1, etc.)
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

print(f"Sumakses! Added {len(chunks)} chunks to your Vector Database.")