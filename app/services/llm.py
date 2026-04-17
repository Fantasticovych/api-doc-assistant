import json
from openai import OpenAI
from app.core.config import settings
from app.schemas.llm import EndpointAnalysisResponse

client = OpenAI(api_key=settings.OPENAI_API_KEY)


class LLMService:
    @staticmethod
    async def analyze_endpoint(method: str, path: str, raw_spec: str) -> EndpointAnalysisResponse:
        system_prompt = """
        You are a Senior Technical Writer. Your task is to analyze a specific API endpoint
        from a provided OpenAPI specification.

        CRITICAL RULES:
        - NEVER return null for example_payload. Always infer and generate a realistic JSON
          example based on the path (e.g., /users -> return id, name, email).
        - If request_docs, response_docs, or validation_rules are missing, infer standard
          REST practices.
        - FORMATTING STRICT RULE: The fields 'request_docs', 'response_docs', and
          'validation_rules' MUST be plain text or Markdown strings. Do NOT use nested
          JSON objects for these fields.
        - Always populate missing_fields with a list of things the developer forgot to
          include (e.g., 'missing 400 response').

        Return ONLY a valid JSON object matching the requested structure.
        """

        user_prompt = f"""
        Analyze the following endpoint:
        Method: {method}
        Path: {path}

        Full Specification context:
        {raw_spec}

        Provide:
        1. Short summary of what this endpoint does.
        2. Description of request parameters/body.
        3. Description of possible responses.
        4. A realistic JSON example payload for a successful request.
        5. Potential validation rules.
        6. List of missing documentation fields in the spec.
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        return EndpointAnalysisResponse(**json.loads(content))
