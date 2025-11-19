import os
import json
import google.generativeai as genai
from typing import Type, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            # For MVP, we might just warn or raise error later
            print("Warning: GOOGLE_API_KEY not found.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_json(self, prompt: str, schema: Type[T]) -> T:
        """Generates a JSON response matching the Pydantic schema."""
        if not self.api_key:
            raise ValueError("API Key is required for generation.")
            
        # Construct a prompt that enforces JSON output
        full_prompt = f"""
        {prompt}
        
        You must respond with a valid JSON object matching this schema:
        {schema.model_json_schema()}
        
        Response:
        """
        
        response = self.model.generate_content(
            full_prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        
        try:
            return schema.model_validate_json(response.text)
        except Exception as e:
            print(f"Failed to parse JSON: {response.text}")
            raise e
