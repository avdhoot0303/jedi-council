# The Jedi Council – Unified LLM Prompting & Benchmarking Framework
[![License](https://img.shields.io/github/license/avdhoot0303/jedi-council)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Issues](https://img.shields.io/github/issues/avdhoot0303/jedi-council)](https://github.com/avdhoot0303/jedi-council/issues)
[![Stars](https://img.shields.io/github/stars/avdhoot0303/jedi-council?style=social)](https://github.com/avdhoot0303/jedi-council/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/avdhoot0303/jedi-council)](https://github.com/avdhoot0303/jedi-council/commits/main)

**“When in doubt, consult the Council.”**

This project provides a clean, extensible framework for interacting with multiple LLMs (OpenAI, Anthropic, Mistral, Gemini) through a unified interface. It supports structured responses, token usage tracking, cost estimation, retry logic, and easy extensibility for adding more providers like LLaMA or Cohere.

---

## Features

- ✅ Unified interface for calling different LLMs (GPT, Claude, Mistral, Gemini)
- ✅ Automatic retry with exponential backoff
- ✅ Cost estimation based on provider pricing
- ✅ Structured logging + latency tracking
- ✅ Extensible to support more LLM providers
- CLI runner, streaming, parallelism (coming soon)

---

## Installation

### 1. Clone and install in editable mode

```bash
git clone https://github.com/yourusername/jedi-council.git
cd jedi-council
pip install -e .
```

This uses the `pyproject.toml` to install dependencies and allows live development.

2. Set up your API keys

Create a .env file in the root folder:

```.env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
MISTRAL_API_KEY=sk-mistral-...
GOOGLE_API_KEY=AIza...
```
Make sure you have a .env loader if you’re running scripts directly. Otherwise, export env vars before execution.

---
### Inspiration

This tool evolved from a research pipeline designed to automate UI tasks using LLMs. To benchmark multiple models across tasks with traceable cost, latency, and output format — a centralized interface was essential.



### Usage

1. **Import the wrapper**
   ```python
   from jedi_council.core import TheJediCouncil
   ```

2. **Initialize a model**
   ```python
   council = TheJediCouncil(model="gpt-4o")
   ```

   ✅ Supported models:
   - **OpenAI**: `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`
   - **Anthropic**: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, `claude-3-haiku-20240307`
   - **Mistral**: `mistral-small-latest`, `mistral-7b`, `mistral-large-latest`
   - **Gemini**: `gemini-1.5-pro-latest`, `gemini-1.0-pro`

3. **Send your first message**
   ```python
   response = council.get_wisdom("What is the capital of Naboo?")
   print(response.text) 
   ```

4. **See structured metadata and cost**
   ```python
   # See structured metadata and cost
   print("Wisdom:", response.text)
   print("Usage:", f"{response.usage.input_tokens} in, {response.usage.output_tokens} out")
   print("Cost: $", f"{response.usage.cost:.4f}")
   print("Latency:", f"{int(response.latency_ms)}ms") 
   ```

### Example Output

```
Wisdom: The philosophy behind the Jedi Code is rooted in principles of peace, self-discipline, and harmony with the Force...
Usage: 16 in, 323 out  
Cost: $ 0.0049  
Latency: 9981ms
```

---

### Example Script

Try running the following to test all configured models:

```bash
python example.py
```

---

### Benchmarking Support

To compare model performance across real tasks, you can run:

```bash
python benchmark/benchmarking_suite.py
```

This will:
- Run a suite of predefined tasks across all available LLMs
- Log model outputs, token usage, latency, and cost
- Save detailed results in `logs/benchmark_results.csv`

You can analyze the results using pandas or any visualization tool:

```python
import pandas as pd

df = pd.read_csv("logs/benchmark_results.csv")
print(df.groupby("model")["cost"].mean())
```

You can also track performance by task category or sort by latency:

```python
df.groupby(["model", "task_name"])["latency_ms"].mean().unstack().plot(kind="bar")
```

#### Sample Benchmarking Output

Here's a sample summary of average latency (in ms) for different models across task categories:

| Task                  | GPT-4o | Claude-3 | Gemini | Mistral |
|-----------------------|--------|----------|--------|---------|
| Ambiguity Resolution  | 13528  | 4175     | 4390   | 5308    |
| Code Generation       | 17870  | 4091     | 3741   | 10309   |
| Logical Reasoning     | 13463  | 1630     | 1890   | 4002    |
| Summarization         | 10132  | 814      | 608    | 799     |
| Time Zone Reasoning   | 11085  | 1019     | 777    | 1712    |

This table highlights latency performance trends across various LLMs for core reasoning and generation tasks.

---

### Roadmap

- Dry-run support (simulate requests without actual calls)
- CLI prompt runner:  
  ```bash
  python run_prompt.py --model gpt-4o --prompt "Say hello"
  ```
- Streaming & parallel inference
- LLaMA and Cohere provider integration
- Output visualizations (token bar, cost heatmap, model latency ranking) ✅ CSV logging added

---

Contributing

Feel free to fork, extend, or open PRs! New provider wrappers, better token tracking, and more benchmarks are all welcome.


License MIT — use freely, contribute kindly
