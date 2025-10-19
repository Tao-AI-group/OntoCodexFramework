class Metrics:
    @staticmethod
    def coverage(num_hits:int, total:int)->float:
        return (num_hits/total) if total else 0.0
