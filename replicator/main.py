import os
import sys
import argparse
from dotenv import load_dotenv
from replicator.llm import LLMClient
from replicator.architect import Architect
from replicator.engineer import Engineer
from replicator.operator import Operator

# Load environment variables
load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="Replicator: AI Web App Factory")
    parser.add_argument("prompt", help="The description of the app you want to build")
    
    # LLM Configuration
    parser.add_argument("--provider", help="LLM Provider (google/openai)", default=os.getenv("LLM_PROVIDER", "google"))
    parser.add_argument("--api-key", help="API Key for the provider", default=None)
    parser.add_argument("--base-url", help="Base URL for OpenAI-compatible APIs", default=os.getenv("OPENAI_BASE_URL"))
    parser.add_argument("--model", help="Model name (e.g. gemini-1.5-flash, gpt-4o)", default=None)

    parser.add_argument("--template", help="Path to base template", default="templates/base-nextjs")
    parser.add_argument("--output", help="Path to output directory", default="output")
    parser.add_argument("--deploy", help="Deploy to IPFS after build", action="store_true")
    
    args = parser.parse_args()
    
    print(f"🚀 Replicator starting... Prompt: '{args.prompt}'")
    print(f"   Provider: {args.provider}")

    # Initialize Agents
    try:
        llm = LLMClient(
            provider=args.provider,
            api_key=args.api_key,
            base_url=args.base_url,
            model=args.model
        )
    except ValueError as e:
        print(f"Error initializing LLM: {e}")
        sys.exit(1)

    architect = Architect(llm)
    engineer = Engineer(llm, template_dir=args.template, output_base_dir=args.output)
    operator = Operator()

    # Step 1: Architect
    print("\n🏗️  Phase 1: Architecture")
    app_spec = architect.design(args.prompt)
    print(f"    Spec generated: {app_spec.name} ({len(app_spec.pages)} pages, {len(app_spec.components)} components)")

    # Step 2: Engineering (Build & Assemble)
    print("\n👨‍💻 Phase 2: Engineering")
    output_path = engineer.build(app_spec)

    print(f"\n✅ Done! App created at: {output_path}")
    
    # Step 3: Operation (Deployment)
    if args.deploy:
        print("\n🚀 Phase 3: Operation")
        deploy_url = operator.deploy(output_path)
        print(f"✅ Deployed to: {deploy_url}")
    else:
        print(f"   Run: cd {output_path} && npm install && npm run dev")
        print(f"   To deploy: pinme upload {output_path}/out")

if __name__ == "__main__":
    main()
