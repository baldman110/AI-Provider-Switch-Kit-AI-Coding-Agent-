import argparse
import json
from pathlib import Path
from typing import Any, Dict, List


SUPPORTED_PROTOCOLS = {"anthropic_messages", "openai_chat_completions"}


def load_config(path: str) -> Dict[str, Any]:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_provider(provider: Dict[str, Any]) -> List[str]:
    warnings: List[str] = []

    provider_id = provider.get("id", "<missing-id>")
    protocol = provider.get("protocol")
    base_url = provider.get("base_url", "")
    api_key = provider.get("api_key", "")
    models = provider.get("models", {})

    if protocol not in SUPPORTED_PROTOCOLS:
        warnings.append(
            f"[{provider_id}] Unsupported protocol: {protocol}. "
            f"Supported: {', '.join(sorted(SUPPORTED_PROTOCOLS))}"
        )

    if not base_url:
        warnings.append(f"[{provider_id}] base_url is empty.")

    if protocol == "anthropic_messages":
        if base_url.endswith("/v1/messages"):
            warnings.append(
                f"[{provider_id}] base_url looks like a full Anthropic endpoint. "
                "Most tools expect the prefix only, not /v1/messages."
            )
        if "/chat/completions" in base_url:
            warnings.append(
                f"[{provider_id}] base_url contains /chat/completions but protocol is anthropic_messages."
            )

    if protocol == "openai_chat_completions":
        if base_url.endswith("/chat/completions"):
            warnings.append(
                f"[{provider_id}] base_url looks like a full OpenAI endpoint. "
                "Most SDKs expect the /v1 prefix only."
            )

    if not api_key or api_key == "YOUR_API_KEY_HERE":
        warnings.append(f"[{provider_id}] api_key is empty or placeholder.")
    elif api_key.lower().startswith("bearer "):
        warnings.append(
            f"[{provider_id}] api_key should usually be the raw key only, without 'Bearer '."
        )

    if not models.get("main"):
        warnings.append(f"[{provider_id}] models.main is missing.")

    return warnings


def find_provider(config: Dict[str, Any], provider_id: str) -> Dict[str, Any]:
    for provider in config.get("providers", []):
        if provider.get("id") == provider_id:
            return provider
    raise ValueError(f"Provider not found: {provider_id}")


def command_validate(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    providers = config.get("providers", [])
    if not providers:
        print("No providers found.")
        return

    has_warning = False
    for provider in providers:
        provider_id = provider.get("id", "<missing-id>")
        warnings = validate_provider(provider)
        if warnings:
            has_warning = True
            print(f"\nProvider: {provider_id}")
            for warning in warnings:
                print(f"  - {warning}")
        else:
            print(f"Provider: {provider_id} OK")

    if not has_warning:
        print("\nAll provider configs look OK.")


def command_env(args: argparse.Namespace) -> None:
    config = load_config(args.config)
    provider = find_provider(config, args.provider)

    protocol = provider.get("protocol")
    base_url = provider.get("base_url", "")
    models = provider.get("models", {})

    if protocol == "anthropic_messages":
        print(f'export ANTHROPIC_BASE_URL="{base_url}"')
        print(f'export ANTHROPIC_MODEL="{models.get("main", "")}"')
        print(f'export ANTHROPIC_DEFAULT_SONNET_MODEL="{models.get("sonnet", models.get("main", ""))}"')
        print(f'export ANTHROPIC_DEFAULT_HAIKU_MODEL="{models.get("haiku", models.get("main", ""))}"')
        print(f'export ANTHROPIC_DEFAULT_OPUS_MODEL="{models.get("opus", models.get("main", ""))}"')
    elif protocol == "openai_chat_completions":
        print(f'export OPENAI_BASE_URL="{base_url}"')
        print(f'export OPENAI_MODEL="{models.get("main", "")}"')
    else:
        raise ValueError(f"Unsupported protocol: {protocol}")


def command_explain_error(args: argparse.Namespace) -> None:
    status = str(args.status)
    mapping = {
        "400": "请求参数错误。检查 messages、model、max_tokens、stream 等字段。",
        "401": "鉴权失败。检查 API Key 是否正确，是否误填 Bearer 前缀。",
        "402": "余额不足或额度不可用。检查供应商账户余额、套餐或赠送额度。",
        "403": "权限不足。检查模型权限、Key 权限或账号状态。",
        "404": "接口不存在。常见原因是 base_url 与 endpoint 拼接错误，或协议类型选错。",
        "429": "请求过于频繁或触发限流。降低并发、稍后重试或检查限额。",
        "500": "供应商服务端错误。稍后重试，并保留 request_id 便于排查。",
    }
    print(mapping.get(status, "未知状态码。请结合响应 body、request_id 和供应商文档继续排查。"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="aiswitchkit",
        description="Validate and generate configs for AI Coding provider switching."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate provider config.")
    validate_parser.add_argument("--config", required=True, help="Path to providers JSON.")
    validate_parser.set_defaults(func=command_validate)

    env_parser = subparsers.add_parser("env", help="Generate environment variables.")
    env_parser.add_argument("--config", required=True, help="Path to providers JSON.")
    env_parser.add_argument("--provider", required=True, help="Provider id.")
    env_parser.set_defaults(func=command_env)

    error_parser = subparsers.add_parser("explain-error", help="Explain common HTTP errors.")
    error_parser.add_argument("--status", required=True, help="HTTP status code, for example 402.")
    error_parser.set_defaults(func=command_explain_error)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
