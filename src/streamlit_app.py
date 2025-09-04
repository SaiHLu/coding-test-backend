import asyncio
import streamlit as st
import tempfile
import os
from dotenv import load_dotenv


from src.ai.chains import ai_answer
from src.ai.ingestions import ingestions as process_ingestions
from src.utils.file_converter import file_to_documents

load_dotenv()

st.title("AI Document Ingestion and Q&A")

question = st.chat_input("Say something")
if question:
    st.chat_message("user").markdown(question)

    result = asyncio.run(ai_answer(question=question))
    st.chat_message("assistant").markdown(result.content)

upload_file = st.file_uploader(
    label="Upload a file(.docx, .txt, pdf)",
    type=["docx", "txt", "pdf"],
)
if upload_file:
    tmp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(
            delete=False, suffix=f".{upload_file.name.split('.')[-1]}"
        ) as tmp_file:
            tmp_file.write(upload_file.getvalue())
            tmp_file_path = tmp_file.name

        documents = file_to_documents(tmp_file_path, upload_file.name)

        # Process the documents
        process_ingestions(documents)

        # Clean up the temporary file
        os.unlink(tmp_file_path)

        st.success(
            f"Successfully processed '{upload_file.name}' and added to the knowledge base!"
        )

    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        # Clean up the temporary file if it exists
        if tmp_file_path and os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)
