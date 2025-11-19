# Replicator

## About the name "Replicator"

In Star Trek, a Replicator instantly reorganizes Energy into Matter, symbolizing the ultimate productivity of "creation from scratch, on demand."

In biology, a Replicator refers to self-replicating units (like genes or memes), representing the infinite propagation and reuse of Information and Intelligence.

Replicator aims to reduce the marginal cost of software development to near zero, making the process of creating apps as simple as ordering a hot tea on a Starship.

## Core Architecture
Replicator is a **Multi-Agent System** modeled after the workflows of a human software development team:    

**1. Architect**

Input: Requirements | Output: AppSpec

**2. Engineer**

Input: AppSpec | Output: Source Code

**3. Operator**

Input: Source Code | Output: URL

## Quick Start

### 1. Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install deployment tool (Optional, for IPFS deployment)
npm install -g pinme

# Configure API Key
export GOOGLE_API_KEY=your_api_key_here
```

### 2. Usage

Turn your prompt into a live app with a single command:

```bash
# Generate source code only
python -m replicator.main "Create a mortgage calculator with amortization schedule"

# Generate & Deploy to IPFS
python -m replicator.main "Create a Cyberpunk style Pomodoro timer" --deploy
```

## Project Structure

- `replicator/`: Core Source Code (Architect, Engineer, Operator, LLM Client).
- `templates/`: Pre-built Next.js project templates.
- `output/`: Directory for generated project artifacts.