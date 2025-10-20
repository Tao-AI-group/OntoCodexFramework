from typing import List, Dict, Any, Optional
import os, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
LABELS=['PHENOTYPE','MAP_rxnorm','MAP_loinc','MAP_snomed']
class LocalPlannerModel:
    def __init__(self, model_path:Optional[str]=None, device:Optional[str]=None):
        self.model_path=model_path or os.environ.get('ONTOCODEX_PLANNER_LOCAL_PATH');
        if not self.model_path: raise RuntimeError('Set ONTOCODEX_PLANNER_LOCAL_PATH or pass model_path')
        self.device=device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.tok=AutoTokenizer.from_pretrained(self.model_path); self.m=AutoModelForSequenceClassification.from_pretrained(self.model_path).to(self.device); self.m.eval()
    def invoke(self, messages:List[Dict[str,Any]])->Dict[str,Any]:
        tx=' '.join([m.get('content','') for m in messages]); enc=self.tok(tx, return_tensors='pt', truncation=True, max_length=512).to(self.device)
        with torch.no_grad(): pred=int(self.m(**enc).logits.argmax(dim=-1).item())
        lab=LABELS[pred];
        return {'role':'assistant','content': 'ACTION: PHENOTYPE' if lab=='PHENOTYPE' else f'ACTION: MAP table={lab.split("_",1)[1]}'}
