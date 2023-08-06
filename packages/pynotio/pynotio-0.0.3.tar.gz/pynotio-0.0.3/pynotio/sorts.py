import json

class Sort:
    @staticmethod
    def asc(prop):
        return [
            {
                "property": prop,
                "direction": "ascending"
            }
        ]
    @staticmethod
    def desc(prop):
        return [
            {
                "property": prop,
                "direction": "descending"
            }
        ]

class CompoundSort:
    def __init__(self, sorts):
        self.update(sorts)

    def __str__(self):
        return self.get_json()
    def __repr__(self):
        return self.get_json()

    def get_json(self):
        return json.dumps(self.sorts_list, indent=4)

    def update(self, sorts):
        self.sorts_list = CompoundSort.create(sorts)
        return self.sorts_list
    
    def get(self):
        return self.sorts_list

    @staticmethod
    def create(sorts):
        sorts_list = []
        for sort in sorts:
            sorts_list.append(sort[0])
        return sorts_list