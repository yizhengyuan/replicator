import shutil
from pathlib import Path
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
    def __init__(self, llm: LLMClient, template_dir: str, output_base_dir: str):
        self.llm = llm
        self.template_dir = Path(template_dir)
        self.output_base_dir = Path(output_base_dir)

    def build(self, spec: AppSpec) -> str:
        print(f"Engineer: Building app '{spec.name}'...")
        
        # 1. Generate Code
        self._generate_code(spec)
        
        # 2. Assemble Project
        return self._assemble_project(spec)

    def _generate_code(self, spec: AppSpec):
        # Generate pages
        for page in spec.pages:
            print(f"  - Generating page: {page.path}")
            page.code = self._generate_file_content(page, spec)
            
        # Generate components
        for component in spec.components:
            print(f"  - Generating component: {component.path}")
            component.code = self._generate_file_content(component, spec)

    def _assemble_project(self, spec: AppSpec) -> str:
        print(f"Engineer: Assembling '{spec.name}'...")
        
        # 1. Create output directory
        app_dir = self.output_base_dir / spec.name
        if app_dir.exists():
            shutil.rmtree(app_dir)
        
        # 2. Copy template
        print(f"  - Copying template from {self.template_dir} to {app_dir}")
        shutil.copytree(self.template_dir, app_dir)
        
        # 3. Write generated files
        for file_spec in spec.pages + spec.components:
            if not file_spec.code:
                print(f"  - Warning: No code generated for {file_spec.path}")
                continue
                
            file_path = app_dir / file_spec.path
            print(f"  - Writing {file_spec.path}")
            
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, "w") as f:
                f.write(file_spec.code)
                
        print(f"Engineer: App '{spec.name}' ready at {app_dir}")
        return str(app_dir)

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
