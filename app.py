import streamlit as st
import os
import chromadb
from google import genai
from google.genai import types  # Added for safety settings
from dotenv import load_dotenv

# 1. Load Local Env (For local testing only)
load_dotenv()

# --- Page Config ---
st.set_page_config(page_title="DocuTalk-AI", page_icon="⛩️")
st.title("⛩️ DocuTalk-AI: Japan Guide")
st.markdown("Ask anything about your Japan travel PDF!")

# --- Initialize Clients ---
@st.cache_resource
def init_app():
    # Initialize Database
    chroma_client = chromadb.PersistentClient(path="./my_vectordb")
    collection = chroma_client.get_or_create_collection(name="japan_travel_docs")
    
    # Auto-Process PDF if database is empty (First time on Cloud)
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
    
    # API Key Priority: 1. Streamlit Secrets (Cloud) 2. Environment Variable (Local)
    api_key = st.secrets.get("GOOGLE_API_KEY") or os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("API Key not found! Please add GOOGLE_API_KEY to Streamlit Secrets.")
        st.stop()

    gemini_client = genai.Client(api_key=api_key)
    return collection, gemini_client

# Initialize everything
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

    # 1. Retrieval
    results = collection.query(query_texts=[prompt], n_results=3)
    context = "\n".join(results['documents'][0])
    
    full_prompt = f"Answer using ONLY this context: {context}\n\nQuestion: {prompt}"
    
    # 2. Generation with Error Handling & Safety Relaxed
    try:
        response = gemini_client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=full_prompt,
            config=types.GenerateContentConfig(
                safety_settings=[
                    types.SafetySetting(
                        category="HARM_CATEGORY_HATE_SPEECH", 
                        threshold="BLOCK_NONE"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_HARASSMENT", 
                        threshold="BLOCK_NONE"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_DANGEROUS_CONTENT", 
                        threshold="BLOCK_NONE"
                    ),
                    types.SafetySetting(
                        category="HARM_CATEGORY_SEXUALLY_EXPLICIT", 
                        threshold="BLOCK_NONE"
                    ),
                ]
            )
        )

        with st.chat_message("assistant"):
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("The AI couldn't generate a response based on that context.")

    except Exception as e:
        st.error(f"⚠️ AI Error: {str(e)}")
        st.info("This can happen due to region restrictions or API limits. Try again in a moment!")