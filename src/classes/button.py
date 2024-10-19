import json


class Button:
    def __init__(self, **kwargs):
        self.source = kwargs.get("source")
        self.button = kwargs.get("button")
    
    def press(self):
        try:
            with open("./requests.json", "r", encoding="utf-8") as requests_json:
                requests = json.load(requests_json)
        except:
            requests = []
        if isinstance(requests, list):
            requests.append({"source": self.source, "button": self.button})
        else:
            requests=[{"source": self.source, "button": self.button}]
        with open("./requests.json", "w", encoding="utf-8") as requests_json:
            json.dump(requests, requests_json, indent=2)