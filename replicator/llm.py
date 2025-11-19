import os
import json
import google.generativeai as genai
from openai import OpenAI
import anthropic
from typing import Type, TypeVar, Optional, Literal
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)

class LLMClient:
    def __init__(self, api_key: Optional[str] = None, provider: str = "google", base_url: Optional[str] = None, model: Optional[str] = None):
        self.provider = provider
        self.api_key = api_key
        self.base_url = base_url
        self.model_name = model

        if self.provider == "google":
            self.api_key = self.api_key or os.getenv("GOOGLE_API_KEY")
            if not self.api_key:
                print("Warning: GOOGLE_API_KEY not found.")
            else:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(self.model_name or 'gemini-1.5-flash')
        
        elif self.provider == "openai":
            self.api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            self.base_url = self.base_url or os.getenv("OPENAI_BASE_URL")
            if not self.api_key:
                 print("Warning: OPENAI_API_KEY not found.")
            else:
                self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
                self.model_name = self.model_name or "gpt-4o"

        elif self.provider == "anthropic":
            self.api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not self.api_key:
                print("Warning: ANTHROPIC_API_KEY not found.")
            else:
                self.client = anthropic.Anthropic(api_key=self.api_key)
                self.model_name = self.model_name or "claude-3-5-sonnet-20241022"
        
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def generate_json(self, prompt: str, schema: Type[T]) -> T:
        """Generates a JSON response matching the Pydantic schema."""
        
        # Construct a prompt that enforces JSON output
        full_prompt = f"""
        {prompt}
        
        You must respond with a valid JSON object matching this schema:
        {schema.model_json_schema()}
        
        Response:
        """

        if self.provider == "google":
            if not self.api_key:
                 raise ValueError("API Key is required for generation.")
            
            response = self.model.generate_content(
                full_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            response_text = response.text

        elif self.provider == "openai":
            if not self.api_key:
                 raise ValueError("API Key is required for generation.")
            
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that outputs JSON."},
                    {"role": "user", "content": full_prompt}
                ],
                response_format={"type": "json_object"}
            )
            response_text = response.choices[0].message.content

        elif self.provider == "anthropic":
            if not self.api_key:
                raise ValueError("API Key is required for generation.")
            
            # Anthropic doesn't have a forced JSON mode like OpenAI/Gemini yet (or handled differently),
            # but Claude is very good at following instructions.
            # We prefill the response with '{' to encourage JSON output.
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": full_prompt},
                    {"role": "assistant", "content": "{"} 
                ]
            )
            # Re-attach the opening brace since we prefilled it
            response_text = "{" + response.content[0].text

        try:
            return schema.model_validate_json(response_text)
        except Exception as e:
            print(f"Failed to parse JSON: {response_text}")
            raise e
