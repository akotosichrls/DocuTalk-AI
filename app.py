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
@st.cache_resource # This keeps the connection fast
def init_clients():
    chroma_client = chromadb.PersistentClient(path="./my_vectordb")
    collection = chroma_client.get_collection(name="japan_travel_docs")
    gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
    return collection, gemini_client

collection, gemini_client = init_clients()

# --- Chat Interface ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # RAG Logic
    results = collection.query(query_texts=[prompt], n_results=3)
    context = "\n".join(results['documents'][0])
    
    full_prompt = f"Answer using ONLY this context: {context}\n\nQuestion: {prompt}"
    
    # Get AI Response
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=full_prompt
    )

    # Display AI Response
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})