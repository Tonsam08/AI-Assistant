import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from hr_assistant.classifier import classify_request


cases = json.loads((ROOT / "evaluation" / "cases.json").read_text(encoding="utf-8"))
topic_cases = [case for case in cases if case["topic"] != "unknown"]
topic_correct = sum(classify_request(case["text"]).topic == case["topic"] for case in topic_cases)
sensitivity_correct = sum(classify_request(case["text"]).sensitive == case["sensitive"] for case in cases)

print(json.dumps({
    "cases": len(cases),
    "topic_accuracy": topic_correct / len(topic_cases),
    "sensitivity_accuracy": sensitivity_correct / len(cases),
}, indent=2))
