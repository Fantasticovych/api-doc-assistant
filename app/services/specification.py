import json
import yaml
from fastapi import HTTPException
from app.core.db import db
from prisma.models import APISpecification
from app.services.parser import ParserService


class SpecificationService:
    @staticmethod
    async def process_and_save(filename: str, content: bytes) -> APISpecification:
        content_str = content.decode("utf-8")
        file_format = "unknown"

        if filename.endswith(".json"):
            file_format = "json"
            try:
                json.loads(content_str)
            except json.JSONDecodeError:
                raise HTTPException(status_code=400, detail="Invalid JSON file format.")

        elif filename.endswith((".yaml", ".yml")):
            file_format = "yaml"
            try:
                yaml.safe_load(content_str)
            except yaml.YAMLError:
                raise HTTPException(status_code=400, detail="Invalid YAML file format.")

        else:
            raise HTTPException(
                status_code=400, detail="Unsupported file format. Use .json or .yaml"
            )

        spec = await db.apispecification.create(
            data={"title": filename, "raw_content": content_str, "format": file_format}
        )

        await ParserService.parse_and_store_endpoints(spec)

        return spec
