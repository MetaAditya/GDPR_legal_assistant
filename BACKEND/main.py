# backend.py

from fastapi import FastAPI

from chat_app.routes.chat_app_routes import router as chat_router
from fastapi import FastAPI, UploadFile, File, Form
import os
import shutil, time
from llm_module.utils.ingest_user_data import document_class
import asyncio
from fastapi.responses import FileResponse

app = FastAPI()



app.include_router(chat_router)


####################File Upload#######################
UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


async def ingest_document(file_name, user_id):
    doc_obj=document_class()

    await asyncio.to_thread(
        doc_obj.user_doc_ingestion_pipeline,
        file_name,
        user_id
    )

@app.post("/upload")
async def receive_file(file: UploadFile = File(...), user_id: str = Form(...)):

    file_path = os.path.join(
        UPLOAD_DIR,
        file.filename
    )

    with open(file_path, "wb") as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    

    await ingest_document(
        file.filename,
        user_id
    )
    

    print("Received file:", file.filename)
    print("Received user:", user_id)

    return {
        "message": "complete",
        "filename": file.filename
    }

###################3Downloads################3333


@app.get("/download")
async def download_pdf():

    file_path = "./downloads/download.pdf"

    if not os.path.exists(file_path):
        return {
            "error": "File not found"
        }

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="download.pdf"
    )