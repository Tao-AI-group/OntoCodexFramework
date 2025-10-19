class Tracer:
    def __init__(self):
        self.spans = []
    def start(self, name: str, **meta):
        self.spans.append({"name": name, "meta": meta})
    def dump(self):
        return self.spans
