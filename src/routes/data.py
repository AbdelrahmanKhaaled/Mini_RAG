from fastapi import FastAPI, APIRouter, Depends, UploadFile, status
from fastapi.responses import JSONResponse
from helpers.config import get_settings, Settings
from controllers import DataController, ProcessController
from models import ResponseSignal
from routes import ProcessRequest
import os
import aiofiles
import logging

data_router = APIRouter(
        prefix="/api/v1/data",
        tags=["api_v1", "data"],
)

logger = logging.getLogger("uvicorn.error")

@data_router.post("/upload/{project_id}")

async def uploading_file(project_id: str, file: UploadFile
                        , app_settings: Settings = Depends(get_settings)):

        data_controller = DataController()

        is_valid, result = data_controller.validate_file_type(file=file)

        if not is_valid:
                return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content= {
                                "signal": result,
                        }
                )
        
        file_path, file_id = data_controller.generate_unique_filepath(file.filename, project_id=project_id) 
        try:       
                async with aiofiles.open(file_path, "wb") as f:
                        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
                                await f.write(chunk)
        except Exception as e:
                logger.error(f"Error while loading file: {e}")

                return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content= {
                                "signal": ResponseSignal.FILE_UPLOAD_FAILED.value
                        }
                )
        
        return JSONResponse(
                content= {
                        "signal": ResponseSignal.FILE_UPLOAD_SUCCESS.value,
                        "Path": file_id
                }
        )

@data_router.post("/process/{project_id}")
async def process_endpoint(project_id: str, process_request: ProcessRequest):
        
        file_id = process_request.file_id
        chunk_siza = process_request.chunk_size
        chunk_overlay = process_request.chunk_overlay

        process_controller = ProcessController(project_id=project_id)
        file_content = process_controller.get_file_content(file_id=file_id)

        file_chunks = process_controller.process_file_content(
                file_content=file_content,
                file_id=file_id,
                chunk_size=chunk_siza,
                overlap_size=chunk_overlay
                )
        
        if file_chunks is None or len(file_chunks) == 0:
                return JSONResponse(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        content={
                                "Signal": ResponseSignal.PROCESSING_FAILED.value
                        }
                )
        return file_chunks