import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.question_answering import load_qa_chain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

# Load API Key
load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Helper Functions
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")

def get_conversational_chain():
    prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
    model = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)
    return chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    # Using a spinner for generating response
    with st.spinner("Generating response..."):
        response = chain({"input_documents": docs, "question": user_question}, return_only_outputs=True)

    # Display the answer after generating it with consistent font size
    st.markdown(f'<div class="answer-text">{response["output_text"]}</div>', unsafe_allow_html=True)

# Dark Mode UI Enhancements and Animation

def main():
    # Set up Streamlit page
    st.set_page_config(page_title="Chat with PDF 💬", layout="wide")

    # Add custom styles for Dark Mode UI and animation
    st.markdown(
        """
        <style>
        body {
            background-color: #121212;  /* Dark background */
            color: white;  /* White text for contrast */
            font-family: 'Arial', sans-serif;
        }
        .header {
            background-color: #1f1f1f;  /* Dark Gray */
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .upload-btn {
            background-color: #00796b;  /* Teal Button */
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
            cursor: pointer;
        }
        .upload-btn:hover {
            background-color: #004d40;  /* Darker Teal on hover */
        }
        .question-section {
            margin-top: 30px;
            padding: 15px;
            border-radius: 10px;
            background-color: #333333;  /* Darker container */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .answer-section {
            margin-top: 20px;
            padding: 15px;
            border-radius: 10px;
            background-color: #333333;  /* Darker container */
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        .submit-btn {
            background-color: #00796b;  /* Teal Button */
            color: white;
            padding: 12px;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
        }
        .submit-btn:hover {
            background-color: #004d40;  /* Darker Teal on hover */
        }
        .spinner {
            animation: rotate 1.5s linear infinite;
        }
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .answer-text {
            font-size: 18px;  /* Ensure the text size is consistent for the entire answer */
            line-height: 1.6;  /* Line spacing for readability */
            white-space: pre-wrap;  /* Ensure the text wraps correctly */
            color: white;  /* White color text for contrast */
            font-family: 'Arial', sans-serif;
            word-wrap: break-word;  /* Ensure that long words break correctly */
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Title and Introduction
    st.markdown('<div class="header"><h1>Chat with PDF 💬</h1></div>', unsafe_allow_html=True)
    st.markdown(
        """
        Upload your PDF document and ask questions. The system will process the content and answer based on the context of the document.
        """
    )

    # Sidebar - File Upload and Process
    with st.sidebar:
        st.header("📥 Upload Your PDFs")
        pdf_docs = st.file_uploader("Upload your PDF files", accept_multiple_files=True)

        if st.button("Submit & Process", key="submit_process"):
            if pdf_docs:
                with st.spinner("Processing your PDF documents..."):
                    raw_text = get_pdf_text(pdf_docs)
                    text_chunks = get_text_chunks(raw_text)
                    get_vector_store(text_chunks)
                    st.success("PDFs processed successfully!")
            else:
                st.warning("Please upload PDF files before processing.")

    # Main Section - Ask Question
    st.markdown('<div class="question-section"><h3>📝 Ask a Question:</h3></div>', unsafe_allow_html=True)
    user_question = st.text_input("Enter your question about the PDF")

    if user_question:
        user_input(user_question)

if __name__ == "__main__":
    main()

