import json, os, time
from typing import Dict, Any

class PlannerLogger:
    """Logs planner prompts and actions for retraining."""
    def __init__(self, log_dir: str = "logs", log_name: str = "planner_log.jsonl"):
        os.makedirs(log_dir, exist_ok=True)
        self.path = os.path.join(log_dir, log_name)

    def log(self, entry: Dict[str, Any]):
        """Append one entry as JSON line."""
        entry["timestamp"] = time.time()
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
