# Replicator 🏭

**Replicator** 是一个 Web 应用流水线工厂。
输入一句话需求（如“房贷计算器”），输出一个完整的、可上线的 Next.js 应用。

## 核心角色 (Roles)

我们把系统简化为两个核心智能体：

1.  **Architect (架构师)**
    *   **职责**：**设计 (Design)**
    *   **任务**：分析用户需求，输出 `AppSpec`（应用规格书）。它决定了要做几个页面，每个页面有什么功能。

2.  **Engineer (工程师)**
    *   **职责**：**建造 (Build)**
    *   **任务**：
        *   **写代码**：根据规格书，编写 React 组件和逻辑。
        *   **组装**：利用底层工具（原 Builder），将代码写入文件系统，生成最终的项目文件夹。

3.  **Operator (运维)**
    *   **职责**：**交付 (Deliver)**
    *   **任务**：负责将生成的项目构建为静态站点，并使用 `pinme` 部署到去中心化网络 (IPFS)。

## 快速开始 (Quick Start)

### 1. 安装
```bash
pip install -r requirements.txt
npm install -g pinme
```

### 2. 配置
设置 Google Gemini API Key：
```bash
export GOOGLE_API_KEY=your_key_here
```

### 3. 生产 & 部署
```bash
# 生产一个番茄钟并自动部署
python replicator/main.py "A pomodoro timer with red theme" --deploy
```

### 4. 运行 (本地)
```bash
cd output/pomodoro-timer
npm install
npm run dev
```
