from prisma import Json
from app.core.db import db
from app.services.llm import LLMService


class DocumentationService:
    @staticmethod
    async def generate_docs_for_spec(spec_id: str):
        spec = await db.apispecification.find_unique(where={"id": spec_id})
        if not spec:
            print(f"Specification {spec_id} not found.")
            return

        endpoints = await db.endpoint.find_many(where={"spec_id": spec_id})
        print(f"Found {len(endpoints)} endpoints for spec {spec_id}. Starting LLM processing...")

        for ep in endpoints:
            try:
                print(f"Processing {ep.method} {ep.path}...")
                analysis = await LLMService.analyze_endpoint(
                    method=ep.method, path=ep.path, raw_spec=spec.raw_content
                )

                missing_str = (
                    ", ".join(analysis.missing_fields) if analysis.missing_fields else None
                )

                update_data = {
                    "summary": analysis.summary,
                    "request_docs": analysis.request_docs,
                    "response_docs": analysis.response_docs,
                    "validation_rules": analysis.validation_rules,
                    "missing_fields": missing_str,
                }

                if analysis.example_payload is not None:
                    update_data["example_payload"] = Json(analysis.example_payload)

                await db.endpoint.update(where={"id": ep.id}, data=update_data)
                print(f"Successfully updated {ep.method} {ep.path}")
            except Exception as e:
                print(f"Error processing {ep.method} {ep.path}: {e}")
