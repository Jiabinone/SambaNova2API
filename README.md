# SambaNova API 适配器

## 免责声明

**重要提示：请在使用本项目之前仔细阅读以下声明**

1. **使用限制**：本项目及其所有相关内容仅供学习和研究目的使用。严禁将本项目用于任何商业目的或违法活动。

2. **时间限制**：使用者必须在获取本项目后的24小时内完全删除本项目的所有内容,包括但不限于源代码、文档和任何衍生作品。

3. **责任声明**：使用者应当遵守所有适用的法律法规,并对使用本项目所产生的任何后果承担全部责任。项目作者和贡献者不对因使用本项目而导致的任何直接或间接损失承担责任。

4. **遵守协议**：使用本项目即表示您同意遵守本免责声明的所有条款。如果您不同意这些条款,请立即停止使用并删除本项目。

---

## 项目简介

这个项目是一个FastAPI应用程序,旨在将SambaNova AI模型的API适配为OpenAI兼容的接口。它允许用户使用与OpenAI API相似的方式来访问和使用SambaNova的强大AI模型,特别是Meta-Llama-3.1系列。

## 功能特点

- 支持多个SambaNova模型,包括:
  - Meta-Llama-3.1-8B-Instruct
  - Meta-Llama-3.1-70B-Instruct
  - Meta-Llama-3.1-405B-Instruct
- 完全兼容OpenAI的chat completions API格式
- 支持流式和非流式响应模式
- 自动模型环境类型映射
- Docker化部署,便于快速设置和扩展
- 使用FastAPI框架,提供高性能的异步处理能力

## 系统要求

- Docker 和 Docker Compose
- Python 3.9+（如果不使用Docker）

## 快速开始

1. 克隆仓库:
   ```bash
   git clone https://github.com/Jiabinone/SambaNova2API.git
   cd SambaNova2API
   ```

2. （可选）设置自定义端口:
   ```bash
   export PORT=your_custom_port
   ```
   如果不设置,默认端口为3335。

3. 使用Docker Compose启动服务:
   ```bash
   docker compose up --build -d && docker compose logs -f
   ```

4. 服务将在 `http://localhost:3335` 上运行 (或您设置的自定义端口)

## API 使用详解

### 端点

- POST `/v1/chat/completions`

### 运行开发服务器

1. 确保您在项目根目录下,并且虚拟环境已激活。

2. 运行开发服务器:
   ```bash
   python app.py
   ```

3. 服务器将在 `http://localhost:3335` 上运行。您可以使用工具如 curl 或 Postman 来测试 API。

## 环境变量

- `PORT`: 设置应用程序运行的端口。默认值为3335。
