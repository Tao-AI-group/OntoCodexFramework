from ontocodex.io.planner_dataset import build_training_dataset

df = build_training_dataset("logs/planner_log.jsonl")
print("Loaded", len(df), "records")
print(df.head())
df.to_csv("planner_training_data.csv", index=False)
print("Exported to planner_training_data.csv")
