from pydantic import BaseModel
import yaml

class PipelineConfig(BaseModel):
    llm: dict
    embedding: dict
    vectorstore: dict
    kg: dict

def load_config(path: str) -> PipelineConfig:
    with open(path, "r") as f:
        data = yaml.safe_load(f)
    return PipelineConfig(**data)
