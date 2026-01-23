# ⛩️ DocuTalk-AI: Japan Travel Assistant

> **Status: Work-in-Progress (On Hiatus) ⏸️** 
> This project was built during a fast-paced "Vibe Coding" session. It currently serves as a functional prototype, but I plan to revisit and refine the architecture when time permits.

---

## 🔗 Project Links
* **Live App:** [Click here to try DocuTalk-AI](https://docutalk-ai-project.streamlit.app/)
* **Progress Tracker:** [View the Feature Log & Roadmap](https://docs.google.com/spreadsheets/d/1tE6vBlYt32DRGJ5xofVxmgQE_S-F2TqvcMeimvGnoo4/edit?usp=sharing)

---

## 🚀 Project Overview
DocuTalk-AI is a RAG-based (Retrieval-Augmented Generation) assistant that allows users to chat with a Japan Travel Guide PDF. It focuses on turning static travel data into interactive, conversational answers.

### 🎨 The "Vibe Coding" Approach
This entire application was **vibe coded** in partnership with Gemini. Rather than deep-diving into manual boilerplate, I focused on high-level intent, rapid iteration, and partnering with AI to move from idea to deployment in record time.

### 🔌 Why Gemini API?
For this prototype, I chose the **Gemini 2.5 Flash API** for its speed and ease of integration. While local AI (like Ollama) offers better privacy and unlimited requests, the Cloud API allowed for an immediate "zero-setup" deployment to Streamlit Cloud for public testing.

---

## 🛠️ The Tech Stack
* **LLM:** Google Gemini 2.5 Flash (via API)
* **Vector Database:** ChromaDB
* **Frontend:** Streamlit
* **Data Processing:** PyPDF & LangChain Text Splitters
* **Development Style:** Vibe Coding + AI-Augmented Engineering

---

## 🧠 How It Works (RAG Architecture)
1. **Ingest:** Reads the local Japan Travel Guide PDF.
2. **Chunk:** Breaks text into 1,000-character segments.
3. **Embed:** ChromaDB creates mathematical representations of the text.
4. **Retrieve:** Finds the top 3 most relevant segments for your question.
5. **Generate:** Gemini generates an answer grounded *only* in that context.



---

## ⚠️ Note on API Limits
This app uses the **Gemini Free Tier**. If you encounter a `429 Resource Exhausted` error, it means the request quota has been reached. Please wait a minute and refresh the page!

---
*Created with 💡 and pure Vibe Coding via Gemini.*