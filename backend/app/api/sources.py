from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.models.schema import SourcesResponse, UploadedFile

router = APIRouter()


@router.post("/api/sources")
async def upload_files(files: Annotated[list[UploadFile], File()]) -> SourcesResponse:
    uploaded_files = []

    for file in files:
        file_name = file.filename
        file_size = file.size
        file_type = file.content_type

        uploaded_files.append(UploadedFile(name=file_name, size=file_size, type=file_type))
    return SourcesResponse(uploaded=uploaded_files)
