# Replicator

## About the name "Replicator"

<img width="1183" height="445" alt="image" src="https://github.com/user-attachments/assets/41d83d6a-4c96-414e-8467-94a5531e060d" />

## Core Architecture
Replicator is a **Multi-Agent System** modeled on the workflows of a human software development team:    

<img width="1386" height="625" alt="Replicator 架构图" src="https://github.com/user-attachments/assets/d5d8fdf5-16ad-4b9c-87be-077f0623e2df" />

## Quick Start

### 1. Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install deployment tool (Optional, for IPFS deployment)
npm install -g pinme

# Configure Environment
# For Google Gemini:
export GOOGLE_API_KEY=your_google_key
export LLM_PROVIDER=google

# For OpenAI (or compatible APIs like DeepSeek/Moonshot):
export OPENAI_API_KEY=sk-xxxx
export LLM_PROVIDER=openai
# Optional: export OPENAI_BASE_URL=https://api.deepseek.com/v1

# For Anthropic (Claude):
export ANTHROPIC_API_KEY=sk-ant-xxxx
export LLM_PROVIDER=anthropic
```

### 2. Usage

Turn your prompt into a live app with a single command:

```bash
# Generate source code only
python -m replicator.main "Create a minimalist To-Do list app"

# Generate & Deploy to IPFS
python -m replicator.main "Create a Cyberpunk style Pomodoro timer" --deploy
```

## Project Structure

- `replicator/`: Core Source Code (Architect, Engineer, Operator, LLM Client).
- `templates/`: Pre-built Next.js project templates.
- `output/`: Directory for generated project artifacts.
