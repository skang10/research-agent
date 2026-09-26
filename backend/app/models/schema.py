from pydantic import BaseModel


# POST /api/research
class ResearchRequest(BaseModel):
    request: str


# POST /api/sources
class UploadedFile(BaseModel):
    name: str
    size: int
    type: str


class SourcesResponse(BaseModel):
    uploaded: list[UploadedFile]
