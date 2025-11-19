# Replicator 🏭

**Replicator** 

<img width="696" height="271" alt="image" src="https://github.com/user-attachments/assets/37bcabec-0bf3-422e-933a-acaacd07ec69" />


本项目致力于将软件开发的边际成本降至近乎为零，让创造应用像在星舰上点一杯热茶一样简单。

## 核心架构

系统采用三代理（Three-Agent）模式，模拟软件开发团队的工作流：

1.  **Architect (架构)**
    *   **职责**：Design (架构)
    *   **输入**：用户 Prompt
    *   **输出**：`AppSpec` (包含页面结构、组件列表、功能描述)
    *   **作用**：将模糊的需求转化为结构化的开发文档。

2.  **Engineer (开发)**
    *   **职责**：Build (开发)
    *   **输入**：`AppSpec`
    *   **工作流**：
        1.  **代码生成**：基于蓝图，并行生成所有页面与组件的源代码。
        2.  **项目组装**：基于 `base-nextjs` 模板，将生成代码注入文件系统。
    *   **输出**：完整的、可运行的项目源代码。

3.  **Operator (运维)**
    *   **职责**：Deploy (运维)
    *   **输入**：项目源代码路径
    *   **工作流**：
        1.  **构建**：执行 `npm run build` 生成静态文件。
        2.  **发布**：通过 `pinme` 将应用部署到 IPFS 去中心化网络。
    *   **输出**：可访问的公网 URL。

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
