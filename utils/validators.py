import re


def validate_openai_key(api_key: str) -> bool:
    return bool(api_key and re.match(r"^sk-[A-Za-z0-9]{20,}$", api_key))


def validate_model_name(model: str) -> bool:
    valid = {
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-4",
        "gpt-4-turbo",
        "gpt-4-turbo-preview",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
    }
    return model in valid


def validate_temperature(temperature: float) -> bool:
    return 0.0 <= temperature <= 2.0


def validate_max_tokens(max_tokens: int) -> bool:
    return 1 <= max_tokens <= 4096
