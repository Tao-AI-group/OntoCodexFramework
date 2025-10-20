import os, json, pandas as pd, tempfile
from typing import Optional

"""
Utility to fine-tune an OpenAI model for OntoCodex planner.
It expects a CSV with columns: input_text, target_text (from planner_dataset.py).
"""

def csv_to_jsonl(csv_path: str, jsonl_path: str):
    df = pd.read_csv(csv_path)
    records = []
    for _, row in df.iterrows():
        prompt = row["input_text"]
        completion = row["target_text"]
        records.append({"messages":[
            {"role":"system","content":"Return exactly one line: ACTION: PHENOTYPE or ACTION: MAP table=<rxnorm|loinc|snomed>."},
            {"role":"user","content": prompt},
            {"role":"assistant","content": completion}
        ]})
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def create_fine_tune_job(train_jsonl: str, model: str = "gpt-4o-mini"):
    from openai import OpenAI
    client = OpenAI()
    with open(train_jsonl, "rb") as f:
        file = client.files.create(file=f, purpose="fine-tune")
    job = client.fine_tuning.jobs.create(training_file=file.id, model=model)
    return job.id

def run(csv_path: str, model: str = "gpt-4o-mini") -> str:
    jsonl = csv_path.replace(".csv", ".jsonl")
    csv_to_jsonl(csv_path, jsonl)
    job_id = create_fine_tune_job(jsonl, model=model)
    return job_id

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="planner_training_data.csv")
    ap.add_argument("--model", default="gpt-4o-mini")
    args = ap.parse_args()
    jid = run(args.csv, model=args.model)
    print("Started fine-tune job:", jid)
