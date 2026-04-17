import json
from app.core.db import db


class ExportService:
    @staticmethod
    async def generate_markdown(spec_id: str) -> str | None:

        spec = await db.apispecification.find_unique(
            where={"id": spec_id}, include={"endpoints": True}
        )

        if not spec:
            return None

        md_lines = []

        title = spec.title if spec.title else "Untitled API Specification"
        md_lines.append(f"# API Documentation: {title}\n")
        md_lines.append(f"**Generated on:** {spec.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n")
        md_lines.append("---\n\n")

        if not spec.endpoints:
            md_lines.append("*No endpoints found.*")
            return "\n".join(md_lines)

        for ep in spec.endpoints:
            md_lines.append(f"## {ep.method} {ep.path}\n")

            if ep.summary:
                md_lines.append(f"**Summary:** {ep.summary}\n\n")

            if ep.request_docs:
                md_lines.append(f"### Request\n{ep.request_docs}\n\n")

            if ep.response_docs:
                md_lines.append(f"### Response\n{ep.response_docs}\n\n")

            if ep.example_payload:
                md_lines.append("### Example Payload\n")
                md_lines.append("```json\n")
                md_lines.append(json.dumps(ep.example_payload, indent=2, ensure_ascii=False) + "\n")
                md_lines.append("```\n\n")

            if ep.validation_rules:
                md_lines.append(f"### Validation Rules\n{ep.validation_rules}\n\n")

            if ep.missing_fields:
                md_lines.append("### Missing Documentation Fields\n")
                md_lines.append(f"{ep.missing_fields}\n\n")

            md_lines.append("---\n\n")

        return "".join(md_lines)
