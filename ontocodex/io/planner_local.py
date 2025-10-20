from typing import List, Dict, Any, Optional
import os, torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

LABELS = ["PHENOTYPE", "MAP_rxnorm", "MAP_loinc", "MAP_snomed"]

class LocalPlannerModel:
    """
    Local HF classifier that predicts one of:
      - PHENOTYPE
      - MAP_rxnorm
      - MAP_loinc
      - MAP_snomed
    Provide model_path or set ONTOCODEX_PLANNER_LOCAL_PATH env var.
    """
    def __init__(self, model_path: Optional[str] = None, device: Optional[str] = None):
        self.model_path = model_path or os.environ.get("ONTOCODEX_PLANNER_LOCAL_PATH")
        if not self.model_path:
            raise RuntimeError("Local planner path not provided. Set ONTOCODEX_PLANNER_LOCAL_PATH or pass model_path.")
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path).to(self.device)
        self.model.eval()

    def invoke(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        text = " ".join([m.get("content","") for m in messages])
        enc = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            logits = self.model(**enc).logits
            pred = int(torch.argmax(logits, dim=-1).item())
        label = LABELS[pred]
        # Convert label to ACTION line for planner compatibility
        if label == "PHENOTYPE":
            content = "ACTION: PHENOTYPE"
        else:
            table = label.split("_",1)[1]
            content = f"ACTION: MAP table={table}"
        return {"role":"assistant","content": content}
