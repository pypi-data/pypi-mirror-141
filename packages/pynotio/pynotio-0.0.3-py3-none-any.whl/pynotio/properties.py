import json

class Prop:
    def __init__(self, data):
        self.data = data
        self.type = data['type']

    def __str__(self):
        return self.get_json()
    def __repr__(self):
        return self.get_json()

    def get_json(self):
        return json.dumps(self.data, indent=4)
    
    def get_value(self):
        if self.type == 'title':
            return self.data['title']['plain_text']
        else:
            return self.data[type]