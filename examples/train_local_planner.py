# Local HuggingFace trainer example
# Prereqs: pip install "transformers>=4.43" "datasets>=2.20" "accelerate>=0.30"
# Usage: python examples/train_local_planner.py --csv planner_training_data.csv --out_dir planner_local_ft
import argparse
from ontocodex.train.hf_trainer import train

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--base_model", default="distilbert-base-uncased")
    ap.add_argument("--out_dir", default="planner_local_ft")
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch_size", type=int, default=8)
    args = ap.parse_args()
    out = train(args.csv, base_model=args.base_model, out_dir=args.out_dir, epochs=args.epochs, batch_size=args.batch_size)
    print("Saved local planner to", out)
    print("To use it: export ONTOCODEX_PLANNER_LOCAL_PATH=", out)
