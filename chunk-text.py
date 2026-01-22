from langchain_text_splitters import RecursiveCharacterTextSplitter

# 1. Imagine this is the text we got from your Japan PDF
# (For this test, we'll use a sample, but later we'll connect them)
raw_text = """
Japan Travel Guide 2024. Tokyo is famous for its neon lights and sushi. 
Osaka is known for its street food like Takoyaki. 
Kyoto offers a glimpse into ancient Japanese history with its beautiful temples.
... (Imagine thousands of more words here) ...
"""

# 2. Initialize the Splitter
# chunk_size: How big each piece is (1000 characters)
# chunk_overlap: How many characters to repeat from the previous piece (prevents cutting sentences)
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=100,
    length_function=len,
)

# 3. Perform the split
chunks = text_splitter.create_documents([raw_text])

# 4. See the results
print(f"Sumakses! Created {len(chunks)} chunks.")
print(f"Preview of Chunk 1:\n{chunks[0].page_content}")