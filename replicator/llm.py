import os
import json
import google.generativeai as genai
from openai import OpenAI
import anthropic
from typing import Type, TypeVar, Optional, Literal
from pydantic import BaseModel
import re

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

    def _clean_json_text(self, text: str) -> str:
        """Cleans up markdown fencing and extra whitespace."""
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        elif text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return text.strip()

    def _extract_valid_json(self, text: str) -> Optional[str]:
        """
        Attempts to extract the actual JSON object from a potentially noisy string.
        """
        text = self._clean_json_text(text)
        
        # Strategy 1: Direct parse
        try:
            # Quick check: if it looks like a schema definition (has "$defs" or "type": "object" at root), reject it
            parsed = json.loads(text)
            if isinstance(parsed, dict) and ("$defs" in parsed or ("type" in parsed and parsed.get("type") == "object")):
                 # This is likely just the schema echoed back
                 pass
            else:
                return text
        except json.JSONDecodeError:
            pass

        # Strategy 2: Handle concatenated JSONs (e.g. "{schema}{data}")
        if "}{" in text:
            parts = text.split("}{")
            last_part = "{" + parts[-1]
            try:
                json.loads(last_part)
                return last_part
            except json.JSONDecodeError:
                pass

        # Strategy 3: Regex search for the last outermost curly braces
        matches = list(re.finditer(r'\{.*\}', text, re.DOTALL))
        if matches:
            # Reverse iterate to find the last valid JSON that is NOT a schema
            for match in reversed(matches):
                candidate = match.group()
                try:
                    parsed = json.loads(candidate)
                    # Check if it's the schema again
                    if isinstance(parsed, dict) and ("$defs" in parsed or ("type" in parsed and parsed.get("type") == "object")):
                        continue # Skip schema
                    return candidate
                except json.JSONDecodeError:
                    continue
                
        return None

    def generate_json(self, prompt: str, schema: Type[T]) -> T:
        """Generates a JSON response matching the Pydantic schema."""
        
        # Construct a prompt that enforces JSON output
        full_prompt = f"""
        {prompt}
        
        You must respond with a valid JSON object that adheres to the following JSON Schema.
        
        JSON Schema:
        {schema.model_json_schema()}
        
        INSTRUCTIONS:
        1. Do NOT return the Schema itself.
        2. Return an actual INSTANCE of the data matching the Schema.
        3. Return ONLY the raw JSON string. No markdown.
        
        Response:
        """

        if self.provider == "google":
            if not self.api_key:
                 raise ValueError("API Key is required for generation.")
            
            print("  (LLM: Waiting for Google Gemini...)")
            response = self.model.generate_content(
                full_prompt,
                generation_config={"response_mime_type": "application/json"}
            )
            response_text = response.text

        elif self.provider == "openai":
            if not self.api_key:
                 raise ValueError("API Key is required for generation.")
            
            print(f"  (LLM: Waiting for OpenAI/{self.model_name}...)")
            
            kwargs = {
                "model": self.model_name,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. You output DATA in JSON format, not Schemas. Do not use markdown."},
                    {"role": "user", "content": full_prompt}
                ]
            }
            
            if "gpt-" in self.model_name or "json" in self.model_name:
                 kwargs["response_format"] = {"type": "json_object"}

            response = self.client.chat.completions.create(**kwargs)
            response_text = response.choices[0].message.content

        elif self.provider == "anthropic":
            if not self.api_key:
                raise ValueError("API Key is required for generation.")
            
            print(f"  (LLM: Waiting for Anthropic/{self.model_name}...)")
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=4096,
                messages=[
                    {"role": "user", "content": full_prompt},
                    {"role": "assistant", "content": "{"} 
                ]
            )
            response_text = "{" + response.content[0].text
        
        # Robust JSON extraction
        cleaned_json = self._extract_valid_json(response_text)
        
        if not cleaned_json:
             # If extraction failed, fall back to original text for debugging
             # But first, check if original text looks like the schema, if so, fail explicitly
             cleaned_json = response_text

        try:
            return schema.model_validate_json(cleaned_json)
        except Exception as e:
            print(f"Failed to parse JSON. Raw response:\n{response_text}")
            raise e
