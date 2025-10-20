# OpenAI planner fine-tune example
# Prereqs: pip install openai pandas
# Usage: python examples/train_openai_planner.py --csv planner_training_data.csv --model gpt-4o-mini
import argparse
from ontocodex.train.openai_finetune import run

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--model", default="gpt-4o-mini")
    args = ap.parse_args()
    job_id = run(args.csv, model=args.model)
    print("Submitted fine-tune job:", job_id)
