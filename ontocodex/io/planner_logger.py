import json, os, time
from typing import Dict, Any
class PlannerLogger:
    def __init__(self, log_dir:str='logs', log_name:str='planner_log.jsonl'):
        os.makedirs(log_dir, exist_ok=True); self.path=os.path.join(log_dir, log_name)
    def log(self, e:Dict[str,Any]): e['timestamp']=time.time(); open(self.path,'a',encoding='utf-8').write(json.dumps(e, ensure_ascii=False)+'\n')
