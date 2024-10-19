import json


class Button:
    def __init__(self, **kwargs):
        self.source = kwargs.get("source")
        self.button = kwargs.get("button")
    
    def press(self):
        pass