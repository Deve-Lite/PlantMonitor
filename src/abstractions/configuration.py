class Configuration:
    def __init__(self, json):
        self.json = json

    def value_in_range(self, name, json=None, min_v: float=0, max_v: float=10):
        if json is None:
            json = self.json
        value = json.get(name)
        print(value)
        if value < min_v or value > max_v:
            raise ValueError(f"Invalid configuration {value} not in range ({min_v},{max_v})")
        return value


    def value_in_list(self, name, items: [], json=None):
        if json is None:
            json = self.json
        value = json.get(name)
        if value not in items:
            raise ValueError(f"Invalid configuration {value} not in list ({items})")
        return value
