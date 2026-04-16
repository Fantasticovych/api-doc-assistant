from fastapi import APIRouter, UploadFile, File
from app.schemas.specification import APISpecificationResponse
from app.services.specification import SpecificationService

router = APIRouter()


@router.post("/upload", response_model=APISpecificationResponse)
async def upload_specification(file: UploadFile = File(...)):
    content = await file.read()

    spec = await SpecificationService.process_and_save(filename=file.filename, content=content)

    return spec
