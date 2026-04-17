from fastapi import APIRouter, BackgroundTasks
from app.services.documentation import DocumentationService

router = APIRouter()


@router.post("/{spec_id}/generate")
async def generate_documentation(spec_id: str, background_tasks: BackgroundTasks):

    background_tasks.add_task(DocumentationService.generate_docs_for_spec, spec_id)

    return {"message": "AI documentation generation started in the background.", "spec_id": spec_id}
