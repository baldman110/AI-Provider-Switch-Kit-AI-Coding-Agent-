# AI Provider Switch Kit

面向个人开发者和小团队的 AI Coding / Agent 多模型供应商接入工具原型。

本项目用于解决在 Claude Code、OpenClaw、OpenCode、CC Switch 等 AI Coding 工具中接入不同模型供应商时遇到的配置复杂、协议差异大、调试效率低、成本不可控等问题。项目重点关注 Anthropic Messages 与 OpenAI Chat Completions 两类接口的配置抽取、配置生成、连通性测试和错误定位。

> 当前版本是一个可运行的工具原型，适合用于整理供应商配置、生成 CC Switch 环境变量、校验 base_url / endpoint / model / auth 等常见问题，并沉淀 AI Agent Coding 工作流。

## 项目背景

国内开发者在使用 AI Coding 工具时，经常需要在多个模型供应商之间切换，例如 Claude、DeepSeek、MiniMax、Qwen、Kimi、MiMo 或其他兼容 OpenAI / Anthropic 协议的平台。常见问题包括：

- API Base URL 和完整 endpoint 混淆，导致 404 或路径重复。
- 模型名填写错误，导致模型不可用。
- API Key 格式错误，例如误把 `Bearer` 一起填入。
- Anthropic Messages 与 OpenAI Chat Completions 协议不兼容。
- 余额不足、额度限制、限流等错误难以快速判断。
- Claude Code / OpenClaw / OpenCode 等工具之间的配置格式不统一。

AI Provider Switch Kit 希望把这些排查过程工具化，并作为 Agent Coding 工作流的一部分持续迭代。

## 核心能力

- 从结构化 JSON 中读取模型供应商配置。
- 检查常见配置错误：
  - base_url 是否误填完整 endpoint。
  - API Key 是否为空或疑似包含 `Bearer` 前缀。
  - 模型名是否缺失。
  - 协议类型是否为支持值。
- 生成 CC Switch / Claude Code 常用环境变量片段。
- 按 HTTP 状态码解释常见错误：
  - `401`：鉴权失败。
  - `402`：余额不足或额度不可用。
  - `404`：endpoint 拼接错误或接口不存在。
  - `429`：限流。
- 为多模型供应商接入流程提供可复用模板。

## 目录结构

```text
ai-provider-switch-kit/
├── README.md
├── requirements.txt
├── config/
│   └── providers.example.json
├── docs/
│   ├── application-description.md
│   └── evidence-guide.md
└── src/
    └── aiswitchkit/
        ├── __init__.py
        └── cli.py
```

## 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-name/ai-provider-switch-kit.git
cd ai-provider-switch-kit
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 复制配置文件

```bash
cp config/providers.example.json config/providers.local.json
```

然后把 `api_key` 替换为自己的 Key。不要把真实 Key 提交到 GitHub。

### 4. 检查配置

```bash
python -m aiswitchkit.cli validate --config config/providers.example.json
```

### 5. 生成环境变量

```bash
python -m aiswitchkit.cli env --config config/providers.example.json --provider scnet-minimax
```

输出示例：

```bash
export ANTHROPIC_BASE_URL="https://api.scnet.cn/api/llm/anthropic"
export ANTHROPIC_MODEL="MiniMax-M2.5"
export ANTHROPIC_DEFAULT_SONNET_MODEL="MiniMax-M2.5"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="MiniMax-M2.5"
export ANTHROPIC_DEFAULT_OPUS_MODEL="MiniMax-M2.5"
```

## 配置示例

```json
{
  "providers": [
    {
      "id": "scnet-minimax",
      "name": "SCNet MiniMax",
      "protocol": "anthropic_messages",
      "base_url": "https://api.scnet.cn/api/llm/anthropic",
      "models": {
        "main": "MiniMax-M2.5",
        "sonnet": "MiniMax-M2.5",
        "haiku": "MiniMax-M2.5",
        "opus": "MiniMax-M2.5"
      },
      "api_key": "YOUR_API_KEY_HERE"
    }
  ]
}
```

## Agent 工作流设计

本项目计划与 AI Coding Agent 结合，形成以下流程：

1. **文档读取 Agent**  
   读取供应商 API 文档，抽取 base_url、endpoint、鉴权方式、协议格式和模型名。

2. **配置生成 Agent**  
   根据文档生成供应商配置 JSON，以及 CC Switch / Claude Code 所需环境变量。

3. **运行测试 Agent**  
   执行连通性测试，收集终端日志、HTTP 状态码和接口返回。

4. **错误诊断 Agent**  
   分析 401、402、404、429 等错误，判断是鉴权、余额、endpoint、模型名还是协议问题。

5. **主控 Agent**  
   汇总各步骤结果，给出可执行的修复建议，并更新项目文档。

## 可验证成果

- 已形成多供应商配置模板。
- 已沉淀 Anthropic Messages / OpenAI Chat Completions 的配置差异。
- 已整理 Claude Code / CC Switch 接入过程中的典型错误。
- 已实现基础配置校验和环境变量生成。
- 后续将加入真实请求测试、日志解析、配置自动修复和多 Agent 编排。

## 后续计划

- 支持 OpenAI Chat Completions 配置生成。
- 增加真实 API ping 测试。
- 增加终端日志解析器。
- 增加 Claude Code / OpenClaw / OpenCode 配置模板。
- 增加 Web UI，用于管理不同供应商和模型。
- 引入多 Agent 协作流程，自动完成文档抽取、配置生成、测试与修复。

## 安全说明

请勿把真实 API Key、账单截图、个人隐私信息提交到公开仓库。建议使用 `.env` 或本地配置文件保存密钥，并把相关文件加入 `.gitignore`。

## License

MIT
