import json
import pandas as pd

def build_training_dataset(log_path: str = "logs/planner_log.jsonl"):
    """Convert planner log JSONL to structured fine-tuning dataset."""
    with open(log_path, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]
    df = pd.DataFrame(records)
    if "memory_context" not in df.columns:
        df["memory_context"] = ""
    df["input_text"] = df["memory_context"].fillna("") + "\nUser: " + df["user_text"]
    df["target_text"] = df["parsed_action"] + df["parsed_table"].apply(lambda x: f" table={x}" if isinstance(x, str) and x else "")
    return df[["input_text", "target_text"]]
