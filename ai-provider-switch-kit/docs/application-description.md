# 小米 MiMo Token Plan 申请文案

## 04 请描述你使用 Agent 或 AI 驱动构建的具体成果

我正在构建一套面向个人开发和小团队使用的 AI Coding / Agent 开发工作流，项目名称暂定为 **AI Provider Switch Kit**。它的核心目标是解决国内开发者在 Claude Code、OpenClaw、OpenCode、CC Switch 等工具中切换不同模型供应商时配置复杂、成本不可控、调试效率低的问题。

这个项目的核心痛点是：传统 AI Coding 工具通常需要手动维护 API Base URL、模型名、鉴权 Key、Anthropic Messages / OpenAI Chat Completions 协议兼容关系等配置；一旦接入多个供应商，很容易出现路径拼接错误、模型名不匹配、余额或计费异常、请求协议不兼容等问题，导致开发者把大量时间浪费在环境调试上，而不是实际编码。

目前我使用 Claude Code + CC Switch + 多模型 API 的方式搭建了一套可切换的 Agent 编程环境，并把接入、校验和排错流程整理成了一个开源项目原型。核心流程包括：

1. 使用 Agent 辅助分析不同供应商的 API 文档，提取 base_url、messages endpoint、模型名、鉴权方式和协议格式；
2. 由 AI 生成并校验对应的 Claude Code / CC Switch 配置 JSON；
3. 在终端中通过 Claude Code 执行真实开发任务，例如代码解释、配置修复、错误日志分析、接口接入验证；
4. 将运行日志、HTTP 状态码和 API 返回结果再次交给 Agent 进行长链推理，定位是路径问题、协议问题、模型问题还是账户计费问题；
5. 将这些经验沉淀为 CLI 工具和项目文档，用于快速接入和验证国内外不同 AI Coding 模型供应商。

这个项目中包含明显的长链推理过程：Agent 需要同时理解 API 文档、配置文件、终端日志、HTTP 错误码、模型协议差异，并给出可执行的修复方案。后续我计划引入多 Agent 协作：一个 Agent 负责读取供应商文档并抽取配置，一个 Agent 负责生成配置文件，一个 Agent 负责运行测试并分析日志，最后由主 Agent 汇总修复建议。

目前项目已经完成基础原型，包括供应商配置模板、Anthropic/OpenAI 协议差异说明、CC Switch 环境变量生成、常见错误码诊断等能力。我也已经完成 Claude Code 与第三方 Anthropic Messages 兼容接口的接入测试，并能通过终端实际触发模型调用；同时沉淀了常见错误排查流程，例如 401 鉴权错误、402 余额不足、404 endpoint 拼接错误、模型名不匹配等。

后续如果获得 Token Plan，我会重点用于高频 AI Coding、Agent 工作流测试、配置自动生成、接口兼容性验证和真实项目代码重构，持续验证 MiMo 在 Claude Code / OpenClaw / OpenCode 场景下的稳定性和性价比。

## 05 使用证明与影响力证明建议

建议上传或填写以下材料：

1. GitHub 项目链接：本项目仓库地址。
2. CC Switch 配置截图：展示已配置的模型供应商。
3. Claude Code 终端运行截图：展示通过 Agent 进行配置排查或代码生成的过程。
4. 运行日志或录屏：展示从输入任务到 Agent 分析、生成配置、解释错误的完整流程。
5. README 截图：展示项目背景、核心能力和后续计划。

注意：公开仓库和截图中不要暴露真实 API Key、账单信息、手机号、邮箱等隐私内容。
