from dataclasses import dataclass
from typing import List, Dict, Any
import pandas as pd
from rapidfuzz import fuzz, process
@dataclass
class MappingTable: name:str; df:pd.DataFrame; label_col:str; code_col:str; type_priority:int
def load_mapping_csv(path:str,name:str,label_col:str,code_col:str,type_priority:int)->MappingTable:
    df=pd.read_csv(path); return MappingTable(name=name, df=df, label_col=label_col, code_col=code_col, type_priority=type_priority)
def fuzzy_map(term:str,tables:List[MappingTable],limit:int=5)->List[Dict[str,Any]]:
    c=[]
    for t in tables:
        if t.label_col not in t.df.columns: continue
        choices=t.df[t.label_col].astype(str).tolist()
        results=process.extract(term, choices, scorer=fuzz.token_set_ratio, limit=limit)
        for label,score,idx in results:
            code=t.df.iloc[idx][t.code_col] if t.code_col in t.df.columns else None
            spec=len(str(code)) if code is not None else 0
            c.append({'table':t.name,'label':label,'code':code,'score_str':float(score),'specificity':spec,'type_priority':t.type_priority})
    return sorted(c, key=lambda x:(-x['score_str'],-x['specificity'],x['type_priority']))[:limit]
