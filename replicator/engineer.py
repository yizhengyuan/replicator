from .llm import LLMClient
from .schema import AppSpec, FileSpec
from pydantic import BaseModel, Field

class CodeResponse(BaseModel):
    code: str = Field(..., description="The generated code")

ENGINEER_PROMPT = """
You are an expert React/Next.js Developer.
Your task is to write the code for a specific file based on the App Specification.

Stack: Next.js 14 (App Router), Tailwind CSS, Lucide React.

Rules:
1. Write clean, modern, functional code.
2. Use 'export default function' for components.
3. Ensure all imports are correct (use @/components/ui/... for shadcn if available, or standard imports).
4. For this MVP, assume standard HTML/Tailwind elements if no UI library is pre-installed beyond Tailwind.
5. Return ONLY the code, no markdown fencing if possible, or wrapped in JSON as requested.
"""

class Engineer:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def build(self, spec: AppSpec) -> AppSpec:
        print(f"Engineer: Building app '{spec.name}'...")
        
        # Generate pages
        for page in spec.pages:
            print(f"  - Generating page: {page.path}")
            page.code = self._generate_file_content(page, spec)
            
        # Generate components
        for component in spec.components:
            print(f"  - Generating component: {component.path}")
            component.code = self._generate_file_content(component, spec)
            
        return spec

    def _generate_file_content(self, file_spec: FileSpec, app_spec: AppSpec) -> str:
        prompt = f"""
        {ENGINEER_PROMPT}
        
        App Name: {app_spec.name}
        App Description: {app_spec.description}
        
        File to generate: {file_spec.path}
        File Description: {file_spec.description}
        
        Context (Other files being generated):
        Pages: {[p.path for p in app_spec.pages]}
        Components: {[c.path for c in app_spec.components]}
        """
        
        response = self.llm.generate_json(prompt, CodeResponse)
        return response.code
