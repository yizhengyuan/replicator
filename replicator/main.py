import os
import sys
import argparse
from dotenv import load_dotenv
from replicator.llm import LLMClient
from replicator.architect import Architect
from replicator.engineer import Engineer
from replicator.tools import FileSystemTools

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Replicator: AI Web App Factory")
    parser.add_argument("prompt", help="The description of the app you want to build")
    parser.add_argument("--api-key", help="Google/OpenAI API Key", default=os.getenv("GOOGLE_API_KEY"))
    parser.add_argument("--template", help="Path to base template", default="templates/base-nextjs")
    parser.add_argument("--output", help="Path to output directory", default="output")
    
    args = parser.parse_args()
    
    if not args.api_key:
        print("Error: API Key is required. Set GOOGLE_API_KEY env var or pass --api-key")
        sys.exit(1)

    print(f"🚀 Replicator starting... Prompt: '{args.prompt}'")

    # Initialize Agents
    llm = LLMClient(api_key=args.api_key)
    architect = Architect(llm)
    engineer = Engineer(llm)
    tools = FileSystemTools(template_dir=args.template, output_base_dir=args.output)

    # Step 1: Architect
    print("\n🏗️  Phase 1: Architecture")
    app_spec = architect.design(args.prompt)
    print(f"    Spec generated: {app_spec.name} ({len(app_spec.pages)} pages, {len(app_spec.components)} components)")

    # Step 2: Engineering
    print("\n👨‍💻 Phase 2: Engineering")
    app_spec = engineer.build(app_spec)

    # Step 3: Assembly (using Tools)
    print("\n🏭 Phase 3: Construction")
    output_path = tools.create_project_files(app_spec)

    print(f"\n✅ Done! App deployed to: {output_path}")
    print(f"   Run: cd {output_path} && npm install && npm run dev")

if __name__ == "__main__":
    main()
