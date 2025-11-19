from .llm import LLMClient
from .schema import AppSpec

ARCHITECT_PROMPT = """
You are an expert Software Architect for a Web App Factory.
Your goal is to design a simple, single-purpose web application based on the user's request.

The app will be built using Next.js and Tailwind CSS.
You need to define the file structure, specifically the pages and components.

Rules:
1. Keep it simple. MVP only.
2. Use standard Next.js App Router structure.
3. Use 'lucide-react' for icons.
4. Design a clean, modern UI.
5. Return a JSON object matching the AppSpec schema.
"""

class Architect:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def design(self, user_prompt: str) -> AppSpec:
        print(f"Architect: Designing app for '{user_prompt}'...")
        
        full_prompt = f"""
        {ARCHITECT_PROMPT}
        
        User Request: "{user_prompt}"
        """
        
        return self.llm.generate_json(full_prompt, AppSpec)
