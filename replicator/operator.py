import subprocess
import shutil
from pathlib import Path

class Operator:
    def __init__(self):
        pass

    def deploy(self, app_dir: str) -> str:
        app_path = Path(app_dir)
        print(f"Operator: Deploying app from {app_path}...")

        # 1. Build the app (Static Export)
        print("  - Building static export...")
        try:
            subprocess.run(["npm", "install"], cwd=app_path, check=True, capture_output=True)
            subprocess.run(["npm", "run", "build"], cwd=app_path, check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"  - Build failed: {e.stderr.decode()}")
            raise e

        # 2. Deploy using pinme
        out_dir = app_path / "out"
        if not out_dir.exists():
            raise FileNotFoundError(f"Build failed: {out_dir} not found")

        print(f"  - Uploading to IPFS via pinme...")
        try:
            # pinme upload <path>
            # We use capture_output to get the URL
            result = subprocess.run(["pinme", "upload", str(out_dir)], check=True, capture_output=True, text=True)
            output = result.stdout
            
            # Parse output for URL (This depends on pinme's output format)
            # Assuming it prints the URL at the end or we just return the whole output for now
            print(f"  - Deployment output:\n{output}")
            return output.strip()
            
        except subprocess.CalledProcessError as e:
            print(f"  - Deployment failed: {e.stderr}")
            raise e
