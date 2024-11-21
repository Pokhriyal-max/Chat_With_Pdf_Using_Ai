# Chat_With_Pdf_Using_Ai

PDF Q&A Chatbot with Google Gemini and FAISS
This project creates an interactive chatbot capable of answering questions based on the contents of uploaded PDF documents. The system uses Streamlit for the user interface, Google Gemini for advanced natural language processing (NLP), and FAISS for efficient similarity search. This allows users to upload PDFs, extract and index their content, and ask questions that the chatbot will answer using the relevant information from the documents.

Features
PDF Upload & Text Extraction: Allows users to upload PDF documents, which are then processed to extract text using PyPDF2. Supports multi-page PDF extraction.
Text Chunking: Large documents are split into smaller chunks to ensure effective indexing and retrieval. Overlap is used to preserve context across chunks for more accurate query responses.
Document Indexing with FAISS: Extracted text is converted into embeddings using Google Gemini and stored in a FAISS vector store for fast, scalable similarity search.
Conversational AI: A conversational interface built with Streamlit allows users to ask questions related to the uploaded documents. The chatbot retrieves the most relevant information from the indexed documents and provides answers using Google Gemini's NLP capabilities.
Real-Time Responses: After uploading the PDF, users can interact with the system in real-time, asking questions based on the document's content, with immediate answers powered by document search and AI processing.
Technologies Used
Streamlit: For creating an interactive web interface that allows users to upload PDFs and interact with the chatbot.
PyPDF2: A library for reading and extracting text from PDF files.
Google Gemini: A generative AI model that powers the chatbot’s natural language processing, understanding, and response generation.
FAISS: A library developed by Facebook for efficient similarity search and clustering of dense vectors, used here to store and search document embeddings.
Installation
To get started with this project locally, follow these steps:

Clone the Repository Clone this repository to your local machine:

Install Dependencies Navigate to the project directory and install the required dependencies using pip:

bash
Copy code
cd repository-name
pip install -r requirements.txt
Set Up Google API Keys

Set up your Google Gemini API keys and store them in a .env file. The app uses these keys to access Google's NLP models for generating embeddings and processing text.
Run the Streamlit App Start the app using Streamlit:

bash
Copy code
streamlit run app.py
This will launch the app in your default browser. You can upload PDFs, ask questions, and get responses directly from the chatbot interface.

How It Works
PDF Text Extraction: Users upload a PDF, and the system reads each page to extract the text using PyPDF2. If the document contains images or complex layouts, text extraction is attempted for each page, and any non-extractable text is reported.

Text Chunking and Embedding: After extracting the text, the content is split into smaller chunks for efficient indexing. Google Gemini embeddings are then generated for each chunk to create vector representations. These vectors are stored in a FAISS index for fast search and retrieval.

Document Search and Question Answering: When a user submits a question, the system searches the FAISS index for the most relevant chunks of text. The best-matching chunks are passed to the Google Gemini model to generate a context-aware response.

Real-time Chat Interface: The Streamlit frontend provides an interactive interface where users can upload PDFs, submit questions, and see real-time answers based on the document contents.

Example Use Case
Uploading PDFs: A user uploads a legal document, research paper, or eBook.
Asking Questions: The user asks specific questions about the content, such as "What is the main topic of the first section?" or "What are the key findings in the conclusion?"
Getting Answers: The system processes the question, searches the document for relevant sections, and provides a detailed answer.
Usage
Once the app is running, you can use the following features:

Upload PDF: Click on the file upload widget to select and upload a PDF document.
Ask Questions: Once the document is processed, you can ask questions based on its contents using the text input box.
View Responses: The chatbot will provide answers in real-time, drawing from the document's text.
Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository and submit a pull request. Here are the steps to contribute:

Fork the Repository: Click on the "Fork" button to create your own copy of the repository.
Create a New Branch: Create a new branch for your changes (git checkout -b feature-name).
Make Changes: Implement your feature or fix the issue.
Commit Changes: Commit your changes (git commit -am 'Add new feature').
Push the Branch: Push your changes to your fork (git push origin feature-name).
Open a Pull Request: Open a pull request in the main repository to review and merge your changes.
