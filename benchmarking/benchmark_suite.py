# benchmark_suite.py
import os
import csv
import time
from datetime import datetime
from jedi_council.core import TheJediCouncil
from jedi_council.utils.council_log import show_banner
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--verbose", action="store_true", help="Show detailed logs")
args = parser.parse_args()

import logging
if not args.verbose:
    logging.getLogger().setLevel(logging.WARNING)
# Directory to save logs
LOG_DIR = "benchmark_runs"
os.makedirs(LOG_DIR, exist_ok=True)

def save_results_to_csv(results, file_path):
    with open(file_path, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

def run_benchmark():
    show_banner()
    tasks = [
        {
            "name": "Logical Reasoning",
            "prompt": "If all Wookies are strong and Chewbacca is a Wookie, is Chewbacca strong? Explain.",
        },
        {
            "name": "Summarization",
            "prompt": "Summarize the following: The Jedi Council governs the Jedi Order... (short passage)",
        },
        {
            "name": "Code Generation",
            "prompt": "Write a Python function that returns Fibonacci numbers up to N.",
        },
        {
            "name": "Ambiguity Resolution",
            "prompt": "A droid sees a man with a telescope. Who has the telescope? Justify both interpretations.",
        },
        {
            "name": "Time Zone Reasoning",
            "prompt": "If it’s 3 PM in Coruscant and Tatooine is 7 hours behind, what time is it there?",
        },
    ]

    models = [
        "gpt-4o",
        "claude-3-haiku-20240307",
        "mistral-large-latest",
        "gemini-1.5-pro"
    ]

    all_results = []
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"\nRunning benchmark suite – Experiment ID: {run_id}\n")

    for task in tasks:
        print(f"→ Task: {task['name']}")
        for model in models:
            print(f"   - {model}: running...", end=" ")
            council = TheJediCouncil(model=model)
            try:
                start_time = time.time()
                response = council.get_wisdom(task["prompt"])
                latency = time.time() - start_time
                all_results.append({
                    "timestamp": datetime.now().isoformat(),
                    "run_id": run_id,
                    "task_name": task["name"],
                    "model": model,
                    "latency_ms": f"{latency * 1000:.0f}",
                    "input_tokens": getattr(response.usage, "input_tokens", 0),
                    "output_tokens": getattr(response.usage, "output_tokens", 0),
                    "cost": getattr(response.usage, "cost", 0.0),
                    "text": response.text.replace("\n", " ")[:500],
                })
                print("✅")
            except Exception as e:
                all_results.append({
                    "timestamp": datetime.now().isoformat(),
                    "run_id": run_id,
                    "task_name": task["name"],
                    "model": model,
                    "latency_ms": -1,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "cost": 0.0,
                    "text": f"[ERROR] {str(e)}"
                })
                print("❌")

    output_path = os.path.join(LOG_DIR, f"benchmark_{run_id}.csv")
    save_results_to_csv(all_results, output_path)
    print(f"\nSaved benchmark results to: {output_path}\n")

if __name__ == "__main__":
    run_benchmark()
