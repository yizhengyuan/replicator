# Replicator


<img width="696" height="271" alt="image" src="https://github.com/user-attachments/assets/37bcabec-0bf3-422e-933a-acaacd07ec69" />


Replicator aims to reduce the marginal cost of software development to near zero, making the process of creating apps as simple as ordering a hot tea on a Starship.

## Core Architecture

Replicator is a Multi-Agent System modeled on the workflows of a human software development team:

1. **Architect**
   - **Input**: Brief description of requirements and ideas.
   - **Process**:
     1. **Requirement Analysis**: Parses natural language instructions to extract core features and page logic.
     2. **Blueprint Definition**: Generates an `AppSpec` containing page structure, component lists, and data flow.
   - **Output**: `AppSpec` (Structured development documentation).

2. **Engineer**
   - **Input**: `AppSpec`
   - **Process**:
     1. **Code Generation**: Generates source code for all pages and components in parallel based on the blueprint.
     2. **Project Assembly**: Injects the generated code into the file system based on the `base-nextjs` template.
   - **Output**: Complete, executable project source code.

3. **Operator**
   - **Input**: Project source code path.
   - **Process**:
     1. **Build**: Executes `npm run build` to generate static files.
     2. **Publish**: Deploys the application to the IPFS decentralized network via `pinme`.
   - **Output**: Accessible public URL.


## 快速开始

### 1. 安装
```bash
# 安装 Python 依赖
pip install -r requirements.txt

# 安装部署工具 (可选，仅当需要自动部署时)
npm install -g pinme
```

### 2. 配置
设置 Google Gemini API Key：
```bash
export GOOGLE_API_KEY=your_key_here
```

### 3. 运行
```bash
# 示例：生成一个房贷计算器
python -m replicator.main "做一个房贷计算器，支持等额本息和等额本金"
```

### 4. 自动部署 (可选)
如果你希望生成后直接部署到 IPFS，加上 `--deploy` 参数：
```bash
python -m replicator.main "做一个番茄钟" --deploy
```

## 项目结构

- `replicator/`: 核心 Python 源码 (Architect, Engineer, Operator, LLM Client)
- `templates/`: 预置的 Next.js 项目模板
- `output/`: 生成的项目产物目录
