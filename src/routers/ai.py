import os
import tempfile
from typing import Annotated
from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from starlette import status


from ..dto.response.base import BaseResponse
from ..dto.requests.ai_request import AIRequest
from ..ai.llm import generate_record
from ..utils.reponse_helper import response_helper
from ..ai.ingestions import ingestions as process_ingestions, retriever
from ..utils.file_converter import file_to_documents
from ..ai.chains import ai_answer

router = APIRouter()


@router.post("/generate", status_code=status.HTTP_200_OK, response_model=BaseResponse)
async def generate_data(body: AIRequest):
    try:
        result = await generate_record(body.input_type)
    except Exception as e:
        return response_helper(
            data=str(e), success=False, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    return response_helper(data={"ai": result.model_dump(mode="json")}, success=True)


@router.post("/ingestions", status_code=status.HTTP_200_OK)
async def ingestions(file: UploadFile = File(...)):
    # Check file type
    if not file.filename or not file.filename.endswith((".txt", ".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only .txt, .pdf, and .docx file types are supported",
        )

    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        documents = file_to_documents(tmp_path, file.filename)

        process_ingestions(documents)

        return response_helper(message="Ingestion successful", success=True)
    except Exception as e:
        return response_helper(
            message=str(e),
            success=False,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
    finally:
        os.remove(tmp_path)


@router.get("/ai_answer")
async def get_ai_answer(question: Annotated[str, Query(min_length=1)]):
    response = await ai_answer(question=question)
    return response
