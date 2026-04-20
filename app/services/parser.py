import json
import logging
import yaml
from app.core.db import db
from prisma.models import APISpecification

logger = logging.getLogger(__name__)


class ParserService:
    @staticmethod
    async def parse_and_store_endpoints(spec: APISpecification):
        logger.info(f"Starting to parse specification: {spec.id}")

        if spec.format == "json":
            data = json.loads(spec.raw_content)
        elif spec.format == "yaml":
            data = yaml.safe_load(spec.raw_content)
        else:
            logger.error("Unsupported format for parsing.")
            return

        paths = data.get("paths", {})
        if not paths:
            logger.warning("No paths found in the specification.")
            return

        endpoints_data = []
        valid_methods = {"get", "post", "put", "delete", "patch", "options", "head"}

        for path, methods in paths.items():
            if not isinstance(methods, dict):
                continue

            for method, details in methods.items():
                if method.lower() in valid_methods:
                    endpoints_data.append(
                        {"spec_id": spec.id, "method": method.upper(), "path": path}
                    )

        if endpoints_data:
            await db.endpoint.create_many(data=endpoints_data)
            logger.info(f"Successfully parsed and stored {len(endpoints_data)} endpoints.")
        else:
            logger.warning("No valid endpoints found to store.")
