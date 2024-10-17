class Button:
    def __init__(self, name: str) -> None:
        self.name = name
        self.status = False

    def press(self) -> None:
        self.status = True
