import json
import yaml
from app.core.db import db
from prisma.models import APISpecification


class ParserService:
    @staticmethod
    async def parse_and_store_endpoints(spec: APISpecification):
        print(f"Starting to parse specification: {spec.id}")

        if spec.format == "json":
            data = json.loads(spec.raw_content)
        elif spec.format == "yaml":
            data = yaml.safe_load(spec.raw_content)
        else:
            print("Unsupported format for parsing.")
            return

        paths = data.get("paths", {})
        if not paths:
            print("No paths found in the specification.")
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
            print(f"Successfully parsed and stored {len(endpoints_data)} endpoints.")
        else:
            print("No valid endpoints found to store.")
