import os, pandas as pd, torch
from typing import Tuple
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from transformers import DataCollatorWithPadding

LABEL2ID = {"PHENOTYPE":0, "MAP_rxnorm":1, "MAP_loinc":2, "MAP_snomed":3}
ID2LABEL = {v:k for k,v in LABEL2ID.items()}

def _map_target(t: str) -> str:
    t = t.strip()
    if t.startswith("ACTION:"):
        # normalize
        t = t.replace("ACTION:", "").strip()
    if t.upper().startswith("PHENOTYPE"):
        return "PHENOTYPE"
    if "rxnorm" in t.lower():
        return "MAP_rxnorm"
    if "loinc" in t.lower():
        return "MAP_loinc"
    if "snomed" in t.lower():
        return "MAP_snomed"
    return "PHENOTYPE"

def load_dataset(csv_path: str) -> Tuple[Dataset, Dataset]:
    df = pd.read_csv(csv_path)
    df["label_name"] = df["target_text"].apply(_map_target)
    df["label"] = df["label_name"].map(LABEL2ID)
    # simple split
    n = len(df)
    split = int(0.9*n)
    train_df = df.iloc[:split].reset_index(drop=True)
    val_df = df.iloc[split:].reset_index(drop=True)
    return Dataset.from_pandas(train_df), Dataset.from_pandas(val_df)

def tokenize_function(examples, tokenizer):
    return tokenizer(examples["input_text"], truncation=True, max_length=512)

def train(csv_path: str, base_model: str = "distilbert-base-uncased", out_dir: str = "planner_local_ft", epochs: int = 2, batch_size: int = 8):
    train_ds, val_ds = load_dataset(csv_path)
    tok = AutoTokenizer.from_pretrained(base_model)
    train_tok = train_ds.map(lambda e: tokenize_function(e, tok), batched=True)
    val_tok = val_ds.map(lambda e: tokenize_function(e, tok), batched=True)
    collator = DataCollatorWithPadding(tokenizer=tok)

    model = AutoModelForSequenceClassification.from_pretrained(base_model, num_labels=4, id2label=ID2LABEL, label2id=LABEL2ID)

    args = TrainingArguments(
        output_dir=out_dir,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        weight_decay=0.01,
        logging_steps=50,
        load_best_model_at_end=True,
        metric_for_best_model="eval_loss"
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_tok,
        eval_dataset=val_tok,
        tokenizer=tok,
        data_collator=collator
    )

    trainer.train()
    trainer.save_model(out_dir)
    tok.save_pretrained(out_dir)
    print("Saved local planner to", out_dir)
    return out_dir

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="planner_training_data.csv")
    ap.add_argument("--base_model", default="distilbert-base-uncased")
    ap.add_argument("--out_dir", default="planner_local_ft")
    ap.add_argument("--epochs", type=int, default=2)
    ap.add_argument("--batch_size", type=int, default=8)
    args = ap.parse_args()
    train(args.csv, base_model=args.base_model, out_dir=args.out_dir, epochs=args.epochs, batch_size=args.batch_size)
