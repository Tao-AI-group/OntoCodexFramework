import json, pandas as pd
def build_training_dataset(log_path:str='logs/planner_log.jsonl'):
    rec=[json.loads(l) for l in open(log_path,'r',encoding='utf-8')]; df=pd.DataFrame(rec)
    if 'memory_context' not in df.columns: df['memory_context']=''
    df['input_text']=df['memory_context'].fillna('')+'\nUser: '+df['user_text']
    df['target_text']=df['parsed_action']+df['parsed_table'].apply(lambda x: f' table={x}' if isinstance(x,str) and x else '')
    return df[['input_text','target_text']]
