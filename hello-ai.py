import os
from google import genai
from dotenv import load_dotenv

# 1. Load your secret API key
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Ask a question using the modern syntax
response = client.models.generate_content(
    model="gemini-2.5-flash", 
    contents="Hello Giminai, what's the bes"
)

# 3. Print the answer
print("--- Giminai AI replied ---")
print(response.text)
print("-------------------")