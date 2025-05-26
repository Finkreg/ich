import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
import asyncio
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import retrieval_qa
from langchain_community.vectorstores import FAISS



async def read_pdf():
    loader = PyPDFLoader("file.pdf")
    pages = []

    async for page in pages:
        pages.append(page)

    return pages

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if 'GOOGLE_API_KEY' not in os.environ:
    os.environ["GOOGLE_API_KEY"] = api_key

print("starting reading PDF file...")
documents = asyncio.run(read_pdf())

print('Start embedding documents and building embedding vector store...')

embeddings = GoogleGenerativeAIEmbeddings(model='models/embedding-001')
vector_store = FAISS.from_documents(documents, embeddings)

print('Vector store created. Initializing LLM and QA chain...')
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True 
)

question = "Moment when sharks for the first time attack the fish"
print(f"\nQuestion: {question}")


result = qa_chain.invoke({"query": question})
print("\n--- Answer from LLM ---")
print(result["result"])

if "source_documents" in result:
    print("\n--- Source Documents (used for generating the answer) ---")
    for i, doc in enumerate(result["source_documents"]):
        page_info = f"Page {doc.metadata['page']}" if 'page' in doc.metadata else "Unknown Page"
        print(f"[{i+1}] {page_info}:\n{doc.page_content[:200]}...\n") 



question_2 = "Describe Santiago's struggle with the marlin."
print(f"\nQuestion: {question_2}")
result_2 = qa_chain.invoke({"query": question_2})
print("\n--- Answer from LLM ---")
print(result_2["result"])

if "source_documents" in result_2:
    print("\n--- Source Documents (used for generating the answer) ---")
    for i, doc in enumerate(result_2["source_documents"]):
        page_info = f"Page {doc.metadata['page']}" if 'page' in doc.metadata else "Unknown Page"
        print(f"[{i+1}] {page_info}:\n{doc.page_content[:200]}...\n")