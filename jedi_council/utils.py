# Add model cost info per 1K tokens (sample values)
MODEL_COSTS = {
    "gpt-4o": {"prompt": 0.005, "completion": 0.015},
    "gpt-3.5-turbo": {"prompt": 0.001, "completion": 0.002},
    "claude-3-haiku-20240307": {"prompt": 0.00025, "completion": 0.00125},
    "mistral-7b": {"prompt": 0.0002, "completion": 0.0006},
    "models/gemini-1.5-pro": {"prompt": 0.000125, "completion": 0.000375},
}

def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    cost = MODEL_COSTS.get(model)
    if not cost:
        return 0.0
    return round((input_tokens / 1000) * cost["prompt"] + (output_tokens / 1000) * cost["completion"], 6)