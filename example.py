# example.py
import os
from jedi_council.core import TheJediCouncil

# CLI argument parsing and logging config
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true", help="Show detailed logs")
args = parser.parse_args()

import logging
if not args.verbose:
    logging.getLogger().setLevel(logging.WARNING)

# Make sure you have a .env file with your API keys:
# OPENAI_API_KEY="sk-..."
# ANTHROPIC_API_KEY="sk-ant-..."
from jedi_council.utils.council_log import show_banner, log_consultation

# At the start
show_banner()


def main():
    # Query 1: OpenAI
    try:
        council_gpt = TheJediCouncil(model="gpt-4o")
        prompt = "What is the primary function of a Jedi Council?"
        response_gpt = council_gpt.get_wisdom(prompt)

        # print(f"\n[Consulting {response_gpt.model}]")
        # print(f"Wisdom: {response_gpt.text}")
        # print(f"Usage: {response_gpt.usage.input_tokens} in, {response_gpt.usage.output_tokens} out, Cost: $ {response_gpt.usage.cost}")
        # print(f"Latency: {response_gpt.latency_ms:.0f}ms")

        log_consultation(
            model_name=response_gpt.model,
            wisdom=response_gpt.text,
            usage=f"{response_gpt.usage.input_tokens} in, {response_gpt.usage.output_tokens} out",
            cost=response_gpt.usage.cost,
            latency=response_gpt.latency_ms
        )
    except Exception as e:
        print(f"\nError consulting OpenAI: {e}")

    # Query 2: Anthropic
    try:
        # New line in example.py
        council_claude = TheJediCouncil(model="claude-3-haiku-20240307")
        prompt = "Describe the planet of Coruscant in three sentences."
        response_claude = council_claude.get_wisdom(prompt)

        # print(f"\n[Consulting {response_claude.model}]")
        # print(f"Wisdom: {response_claude.text}")
        # print(f"Usage: {response_claude.usage.input_tokens} in, {response_claude.usage.output_tokens} out, Cost: $ {response_claude.usage.cost}")
        # print(f"Latency: {response_claude.latency_ms:.0f}ms")

        log_consultation(
            model_name=response_claude.model,
            wisdom=response_claude.text,
            usage=f"{getattr(response_claude.usage, 'input_tokens', 0)} in, {getattr(response_claude.usage, 'output_tokens', 0)} out",
            cost=getattr(response_claude.usage, 'cost', 0.0),
            latency=response_claude.latency_ms
        )
    except Exception as e:
        print(f"\nError consulting Anthropic: {e}")

    # Query 3: Mistral
    try:
        council_mistral = TheJediCouncil(model="mistral-large-latest")
        prompt = "Summarize the role of Yoda in the Jedi Council."
        response_mistral = council_mistral.get_wisdom(prompt)

        # print(f"\n[Consulting {response_mistral.model}]")
        # print(f"Wisdom: {response_mistral.text}")
        # print(f"Usage: {response_mistral.usage.input_tokens} in, {response_mistral.usage.output_tokens} out, Cost: $ {response_mistral.usage.cost}")
        # print(f"Latency: {response_mistral.latency_ms:.0f}ms")

        log_consultation(
            model_name=response_mistral.model,
            wisdom=response_mistral.text,
            usage=f"{response_mistral.usage.input_tokens} in, {response_mistral.usage.output_tokens} out",
            cost=response_mistral.usage.cost,
            latency=response_mistral.latency_ms
        )
    except Exception as e:
        print(f"\nError consulting Mistral: {e}")

    # Query 4: Gemini
    try:
        council_gemini = TheJediCouncil(model="gemini-1.5-pro")
        prompt = "What is the philosophy behind the Jedi Code?"
        response_gemini = council_gemini.get_wisdom(prompt)

        # print(f"\n[Consulting {response_gemini.model}]")
        # print(f"Wisdom: {response_gemini.text}")
        # print(f"Usage: {response_gemini.usage.input_tokens} in, {response_gemini.usage.output_tokens} out")
        # print(f"Latency: {response_gemini.latency_ms:.0f}ms")

        log_consultation(
            model_name=response_gemini.model,
            wisdom=response_gemini.text,
            usage=f"{response_gemini.usage.input_tokens} in, {response_gemini.usage.output_tokens} out",
            cost=getattr(response_gemini.usage, "cost", 0.0),
            latency=response_gemini.latency_ms
        )
    except Exception as e:
        print(f"\nError consulting Gemini: {e}")


if __name__ == "__main__":
    main()