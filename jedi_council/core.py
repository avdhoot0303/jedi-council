# jedi_council/core.py

import os
import time
import logging
import abc
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from jedi_council.utils import estimate_cost
# --- Use official clients ---
from openai import OpenAI
from anthropic import Anthropic
import google.generativeai as genai
from mistralai import Mistral

from dotenv import load_dotenv

load_dotenv()

# --- Basic logging configuration ---
# Users can control verbosity with the LOG_LEVEL environment variable.
logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# A more thematic error constant
ERROR_COUNCIL_RESPONSE = "[ERROR] The Council has failed to respond after multiple attempts."


# --- Structured Response Objects ---
@dataclass
class UsageInfo:
    """Stores token usage and cost information."""
    input_tokens: int
    output_tokens: int
    cost: Optional[float] = None


@dataclass
class CouncilResponse:
    """A structured object containing the full response from the LLM."""
    text: str
    model: str
    usage: UsageInfo
    latency_ms: float
    raw_response: Any  # The original response object for deep inspection


# --- Abstracted Retry Logic Decorator ---
def retry_handler(func):
    """A decorator to handle API call retries with exponential backoff."""

    def wrapper(self, *args, **kwargs):
        retries = self.max_retry
        wait = 1.0
        while retries > 0:
            try:
                return func(self, *args, **kwargs)
            except Exception as e:
                logger.warning(f"Error calling {self.__class__.__name__}: {e}. Retrying in {wait:.1f}s...")
                retries -= 1
                time.sleep(wait)
                wait *= 2

        # Return a structured error response if all retries fail
        return CouncilResponse(
            text=ERROR_COUNCIL_RESPONSE,
            model=self.model,
            usage=UsageInfo(input_tokens=0, output_tokens=0),
            latency_ms=0,
            raw_response=None
        )

    return wrapper


# --- Internal Provider Interface ---
class LlmProvider(abc.ABC):
    """Abstract interface for an LLM provider."""

    def __init__(self, model: str, max_retry: int = 3, **kwargs):
        self.model = model
        self.max_retry = max(1, min(max_retry, 5))

    @abc.abstractmethod
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> CouncilResponse:
        """The core method all providers must implement."""
        pass


# --- Internal Provider Implementations ---
class _OpenAIProvider(LlmProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    @retry_handler
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> CouncilResponse:
        logger.info(f"Consulting OpenAI model: {self.model}")
        start_time = time.time()

        params = {"temperature": 0.2, "max_tokens": 2048, **kwargs}
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **params
        )
        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"Received wisdom from {self.model} in {latency_ms:.0f}ms.")

        return CouncilResponse(
            text=response.choices[0].message.content,
            model=self.model,
            usage=UsageInfo(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                cost=estimate_cost(self.model, input_tokens=response.usage.prompt_tokens, output_tokens=response.usage.completion_tokens),
            ),
            latency_ms=latency_ms,
            raw_response=response
        )


class _AnthropicProvider(LlmProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    @retry_handler
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> CouncilResponse:
        logger.info(f"Consulting Anthropic model: {self.model}")
        start_time = time.time()

        system_prompt_content = next((m['content'] for m in messages if m['role'] == 'system'), None)
        user_messages = [m for m in messages if m['role'] != 'system']

        # Fix: system should be a plain string or None
        system_param = system_prompt_content


        params = {"temperature": 0.2, "max_tokens": 2048, **kwargs}
        if system_param is not None:
            response = self.client.messages.create(
                model=self.model,
                messages=user_messages,
                system=system_param,
                **params
            )
        else:
            response = self.client.messages.create(
                model=self.model,
                messages=user_messages,
                **params
            )
        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"Received wisdom from {self.model} in {latency_ms:.0f}ms.")

        return CouncilResponse(
            text=response.content[0].text,
            model=self.model,
            usage=UsageInfo(
                input_tokens=response.usage.input_tokens,
                output_tokens=response.usage.output_tokens,
                cost=estimate_cost(self.model, input_tokens=response.usage.prompt_tokens,
                                   output_tokens=response.usage.completion_tokens),

            ),
            latency_ms=latency_ms,
            raw_response=response
        )


class _GeminiProvider(LlmProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
        # Fix: use correct full model name
        self.model_obj = genai.GenerativeModel(
            model_name=f"models/{self.model}",
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,
                max_output_tokens=1000
            )
        )

    @retry_handler
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> CouncilResponse:
        logger.info(f"Consulting Gemini model: {self.model}")
        start_time = time.time()
        text_input = "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in messages])
        response = self.model_obj.generate_content(text_input, generation_config={"temperature": 0.2, **kwargs})
        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"Received wisdom from {self.model} in {latency_ms:.0f}ms.")
        return CouncilResponse(
            text=response.text,
            model=self.model,
            usage=UsageInfo(input_tokens=0, output_tokens=0),  # Gemini doesn't return usage yet
            latency_ms=latency_ms,
            raw_response=response
        )

class _MistralProvider(LlmProvider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.api_key = os.environ.get("MISTRAL_API_KEY")
        if not self.api_key:
            raise RuntimeError("Mistral API key not set.")
        self.client = Mistral(api_key=self.api_key)

    @retry_handler
    def generate(self, messages: List[Dict[str, str]], **kwargs) -> CouncilResponse:
        logger.info(f"Consulting Mistral model: {self.model}")
        start_time = time.time()

        # FIX: Use `.chat.complete()` instead of `.chat(...)`
        response = self.client.chat.complete(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.2),
            max_tokens=kwargs.get("max_tokens", 2048),
        )

        latency_ms = (time.time() - start_time) * 1000
        logger.info(f"Received wisdom from {self.model} in {latency_ms:.0f}ms.")

        return CouncilResponse(
            text=response.choices[0].message.content,
            model=self.model,
            usage=UsageInfo(
                input_tokens=response.usage.prompt_tokens,
                output_tokens=response.usage.completion_tokens,
                cost=estimate_cost(self.model, input_tokens=response.usage.prompt_tokens,
                                   output_tokens=response.usage.completion_tokens),

            ),
            latency_ms=latency_ms,
            raw_response=response
        )


# --- The Main User-Facing Class ---
class TheJediCouncil:
    """A unified wrapper to seek wisdom from various LLMs."""

    def __init__(self, model: str, **kwargs):
        """
        Initializes the council by selecting the correct member (provider).

        Args:
            model (str): The name of the model to consult (e.g., "gpt-4o", "claude-3-5-sonnet-20240620").
        """
        logger.info(f"Convening The Jedi Council to consult model: {model}")

        # Factory Logic: Route to the correct internal provider
        if model.startswith("gpt"):
            self._provider = _OpenAIProvider(model=model, **kwargs)
        elif "claude" in model:
            self._provider = _AnthropicProvider(model=model, **kwargs)
        elif "gemini" in model:
            self._provider = _GeminiProvider(model=model, **kwargs)
        elif "mistral" in model:
            self._provider = _MistralProvider(model=model, **kwargs)
        else:
            raise ValueError(f"No council member found for model '{model}'.")

    def get_wisdom(self, prompt: str | List[Dict[str, str]], **kwargs) -> CouncilResponse:
        """
        Presents a query to the council and returns its wisdom.

        Args:
            prompt (str or List[Dict]): A single query string or a list of message dictionaries.
            **kwargs: Additional parameters like temperature, max_tokens, etc.

        Returns:
            A CouncilResponse object containing the text, usage data, and more.
        """
        if isinstance(prompt, str):
            messages = [{"role": "user", "content": prompt}]
        else:
            messages = prompt

        return self._provider.generate(messages, **kwargs)
