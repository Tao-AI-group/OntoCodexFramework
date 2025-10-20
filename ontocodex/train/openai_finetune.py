import os, json, pandas as pd
from openai import OpenAI
def csv_to_jsonl(csv_path:str,jsonl_path:str):
    df=pd.read_csv(csv_path); rows=[]
    for _,r in df.iterrows(): rows.append({'messages':[{'role':'system','content':'Return exactly one line: ACTION: PHENOTYPE or ACTION: MAP table=<rxnorm|loinc|snomed>.'},{'role':'user','content':r['input_text']},{'role':'assistant','content':r['target_text']} ]})
    with open(jsonl_path,'w',encoding='utf-8') as f:
        for row in rows: f.write(json.dumps(row, ensure_ascii=False)+'\n')
def run(csv_path:str, model:str='gpt-4o-mini'):
    client=OpenAI(); jsonl=csv_path.replace('.csv','.jsonl'); csv_to_jsonl(csv_path,jsonl)
    with open(jsonl,'rb') as f: file=client.files.create(file=f, purpose='fine-tune')
    job=client.fine_tuning.jobs.create(training_file=file.id, model=model); return job.id
