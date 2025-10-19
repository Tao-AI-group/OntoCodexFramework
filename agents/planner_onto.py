class OntologyPlanner:
    def __init__(self, llm, tools: dict):
        self.llm = llm
        self.tools = tools

    def invoke(self, goal: str):
        thought = self.llm.invoke([
            {"role":"system","content":"Decide: RETRIEVE or SPARQL. If SPARQL, emit 'SPARQL: <query>'."},
            {"role":"user","content": goal}
        ])
        content = thought.get("content","")
        if "SPARQL:" in content:
            q = content.split("SPARQL:")[-1].strip()
            return self.tools["sparql"].invoke({"query": q})
        return self.tools["retriever"].invoke(goal)
