import os
import shutil
from pathlib import Path
from .schema import AppSpec

class FileSystemTools:
    def __init__(self, template_dir: str, output_base_dir: str):
        self.template_dir = Path(template_dir)
        self.output_base_dir = Path(output_base_dir)

    def create_project_files(self, spec: AppSpec) -> str:
        print(f"Assembler: Assembling '{spec.name}'...")
        
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
                
        print(f"Assembler: App '{spec.name}' ready at {app_dir}")
        return str(app_dir)
