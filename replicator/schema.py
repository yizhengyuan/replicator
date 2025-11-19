from typing import List, Optional
from pydantic import BaseModel, Field

class FileSpec(BaseModel):
    """Represents a single file to be generated."""
    path: str = Field(..., description="Relative path to the file (e.g., 'app/page.tsx')")
    description: str = Field(..., description="Description of what this file should contain")
    code: Optional[str] = Field(None, description="The actual code content (populated by Engineer)")

class AppSpec(BaseModel):
    """The blueprint for the application."""
    name: str = Field(..., description="Name of the application (kebab-case)")
    description: str = Field(..., description="High-level description of the app's purpose")
    pages: List[FileSpec] = Field(..., description="List of page files to generate")
    components: List[FileSpec] = Field(..., description="List of component files to generate")
    
    # Future extensibility
    theme_color: Optional[str] = Field("slate", description="Tailwind theme color")
