from typing import Callable, Dict

_REGISTRY: Dict[str, Callable[..., object]] = {}

def register(name: str):
    def deco(fn: Callable[..., object]):
        _REGISTRY[name] = fn
        return fn
    return deco

def create(name: str, **kwargs):
    if name not in _REGISTRY:
        raise KeyError(f"Component '{name}' not registered")
    return _REGISTRY[name](**kwargs)
