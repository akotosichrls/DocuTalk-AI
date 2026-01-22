from pypdf import PdfReader

# 1. Point to your PDF file
pdf_path = "eat_japan_jnto_2017_unlayi.pdf"

# 2. Initialize the PDF Reader
reader = PdfReader(pdf_path)

# 3. Extract text from all pages
full_text = ""
for page in reader.pages:
    full_text += page.extract_text() + "\n"

# 4. Print just the first 500 characters to test
print("--- PDF Content Preview ---")
print(full_text[:500]) 
print("---------------------------")
print(f"\nTotal pages extracted: {len(reader.pages)}")