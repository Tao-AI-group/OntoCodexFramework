import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments, DataCollatorWithPadding
LABEL2ID={'PHENOTYPE':0,'MAP_rxnorm':1,'MAP_loinc':2,'MAP_snomed':3}; ID2LABEL={v:k for k,v in LABEL2ID.items()}
def _map_target(t:str)->str:
    t=t.strip();
    if t.startswith('ACTION:'): t=t.replace('ACTION:','').strip()
    if t.upper().startswith('PHENOTYPE'): return 'PHENOTYPE'
    if 'rxnorm' in t.lower(): return 'MAP_rxnorm'
    if 'loinc' in t.lower(): return 'MAP_loinc'
    if 'snomed' in t.lower(): return 'MAP_snomed'
    return 'PHENOTYPE'
def load_dataset(csv_path:str):
    df=pd.read_csv(csv_path); df['label_name']=df['target_text'].apply(_map_target); df['label']=df['label_name'].map(LABEL2ID)
    split=int(0.9*len(df)); return Dataset.from_pandas(df.iloc[:split]), Dataset.from_pandas(df.iloc[split:])
def train(csv_path:str, base_model:str='distilbert-base-uncased', out_dir:str='planner_local_ft', epochs:int=2, batch_size:int=8):
    tr,va=load_dataset(csv_path); tok=AutoTokenizer.from_pretrained(base_model); coll=DataCollatorWithPadding(tokenizer=tok)
    def tok_fn(ex): return tok(ex['input_text'], truncation=True, max_length=512)
    tr_tok=tr.map(tok_fn, batched=True); va_tok=va.map(tok_fn, batched=True)
    m=AutoModelForSequenceClassification.from_pretrained(base_model, num_labels=4, id2label=ID2LABEL, label2id=LABEL2ID)
    args=TrainingArguments(output_dir=out_dir, evaluation_strategy='epoch', save_strategy='epoch', learning_rate=2e-5, per_device_train_batch_size=batch_size, per_device_eval_batch_size=batch_size, num_train_epochs=epochs, weight_decay=0.01, logging_steps=50, load_best_model_at_end=True, metric_for_best_model='eval_loss')
    trnr=Trainer(model=m, args=args, train_dataset=tr_tok, eval_dataset=va_tok, tokenizer=tok, data_collator=coll)
    trnr.train(); trnr.save_model(out_dir); tok.save_pretrained(out_dir); return out_dir
