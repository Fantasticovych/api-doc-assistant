from fastapi import APIRouter, BackgroundTasks, Response, HTTPException
from app.services.documentation import DocumentationService
from app.services.export import ExportService

router = APIRouter()


@router.post("/{spec_id}/generate")
async def generate_documentation(spec_id: str, background_tasks: BackgroundTasks):

    background_tasks.add_task(DocumentationService.generate_docs_for_spec, spec_id)

    return {"message": "AI documentation generation started in the background.", "spec_id": spec_id}


@router.get("/{spec_id}/export")
async def export_documentation(spec_id: str):

    markdown_content = await ExportService.generate_markdown(spec_id)

    if not markdown_content:
        raise HTTPException(status_code=404, detail="Specification not found")

    return Response(
        content=markdown_content,
        media_type="text/markdown",
        headers={"Content-Disposition": 'attachment; filename="api_docs.md"'},
    )
