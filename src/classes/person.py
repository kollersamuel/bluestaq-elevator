import numpy as np

class Person:
    def __init__(self, id: int) -> None:
        self.id: int = id
        self.weight: float = max(20, min(np.random.normal(loc=150, scale=50), 500))
        self.cargo_weight: float = max(0, min(np.random.normal(loc=25, scale=5), 100))