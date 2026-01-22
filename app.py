import streamlit as st
import os
import chromadb
from google import genai
from dotenv import load_dotenv

load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="DocuTalk-AI", page_icon="⛩️")
st.title("⛩️ DocuTalk-AI: Japan Guide")
st.markdown("Ask anything about your Japan travel PDF!")

# --- Initialize Clients ---
@st.cache_resource
def init_app():
    # 1. Initialize Database
    chroma_client = chromadb.PersistentClient(path="./my_vectordb")
    collection = chroma_client.get_or_create_collection(name="japan_travel_docs")
    
    # 2. Auto-Process PDF if database is empty (First time on Cloud)
    if collection.count() == 0:
        from pypdf import PdfReader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        
        pdf_path = "eat_japan_jnto_2017_unlayi.pdf"
        if os.path.exists(pdf_path):
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
            chunks = splitter.split_text(text)
            collection.add(
                documents=chunks,
                ids=[f"chunk_{i}" for i in range(len(chunks))]
            )
    
    # 3. Initialize Gemini using Streamlit Secrets
    # On Cloud, this uses the 'Advanced Settings' secrets box.
    gemini_client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])
    
    return collection, gemini_client

# Corrected function call to match the definition
collection, gemini_client = init_app()

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG Logic: Retrieve and Generate
    results = collection.query(query_texts=[prompt], n_results=3)
    context = "\n".join(results['documents'][0])
    
    full_prompt = f"Answer using ONLY this context: {context}\n\nQuestion: {prompt}"
    
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=full_prompt
    )

    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})