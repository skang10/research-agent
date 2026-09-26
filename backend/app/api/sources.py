from typing import Annotated

from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from app.models.schema import SourcesResponse, UploadedFile
from app.retrieval.parser import UnsupportedFileTypeError

router = APIRouter()


@router.post("/api/sources", response_model=SourcesResponse)
async def upload_files(
    request: Request, files: Annotated[list[UploadFile], File()]
) -> SourcesResponse:
    uploaded_files = []

    for file in files:
        try:
            await request.app.state.ingestor.ingest(file)
        except UnsupportedFileTypeError as e:
            raise HTTPException(status_code=415, detail=str(e)) from e
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"An error occurred during ingestion: {str(e)}"
            ) from e
        file_name = file.filename
        file_size = file.size
        file_type = file.content_type

        uploaded_files.append(UploadedFile(name=file_name, size=file_size, type=file_type))
    return SourcesResponse(uploaded=uploaded_files)
