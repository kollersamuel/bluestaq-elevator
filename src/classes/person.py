# import numpy as np

# class Person:
#     def __init__(self, id: int) -> None:
#         self.id: int = id
#         """ ? Normally distribute weight, constrain to between 20 (persons less than 20 pounds considered cargo) and
#             500 (arbitrary maximum) """
#         self.weight: float = max(20, min(np.random.normal(loc=150, scale=50), 500))
#         self.cargo_weight: float = max(0, min(np.random.normal(loc=25, scale=5), 100))
