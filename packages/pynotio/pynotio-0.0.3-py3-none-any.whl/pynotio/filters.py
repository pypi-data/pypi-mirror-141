import json

# TODO add People, File & Formula filters
class CompoundFilter:
    def __init__(self, filter1 = None, filter2 = None, op = None):
        self.update(filter1, filter2, op)

    def __str__(self):
        return self.get_json()
    def __repr__(self):
        return self.get_json()

    def get_json(self):
        return json.dumps(self.filter_obj, indent=4)

    def update(self, filter1 = None, filter2 = None, op = "or"):
        self.filter_obj = CompoundFilter.create(filter1, filter2, op)
        return self.filter_obj
    
    def get(self):
        return self.filter_obj

    @staticmethod
    def create(filter1 = None, filter2 = None, op = "or"):
        if not filter1 is None and not filter2 is None:
            filter_obj = {
                op: [
                    filter1, filter2
                ]
            }
            return filter_obj
        else:
            raise RuntimeError("You must provide both filters to create CompoundFilter")

class TextFilter:
    @staticmethod  
    def equals(prop, val):
        return {
            "property": prop,
            "text": {
                "equals": val
            }
        }
    @staticmethod
    def not_equals(prop, val):
        return {
            "property": prop,
            "text": {
                "does_not_equal": val
            }
        }

    @staticmethod
    def contains(prop, val):
        return {
            "property": prop,
            "text": {
                "contains": val
            }
        }
    @staticmethod
    def not_contains(prop, val):
        return {
            "property": prop,
            "text": {
                "does_not_contain": val
            }
        }

    @staticmethod
    def starts_with(prop, val):
        return {
            "property": prop,
            "text": {
                "starts_with": val
            }
        }
    @staticmethod
    def ends_with(prop, val):
        return {
            "property": prop,
            "text": {
                "ends_with": val
            }
        }

    @staticmethod
    def is_empty(prop, val):
        filter_object = {
            "property": prop
        }
        if val:
            filter_object['text']['is_empty'] = True
        else:
            filter_object['text']['is_not_empty'] = True
        return filter_object




class NumberFilter:
    @staticmethod  
    def equals(prop, val):
        return {
            "property": prop,
            "number": {
                "equals": val
            }
        }
    @staticmethod  
    def not_equals(prop, val):
        return {
            "property": prop,
            "number": {
                "does_not_equal": val
            }
        }

    @staticmethod  
    def greater(prop, val):
        return {
            "property": prop,
            "number": {
                "greater_than": val
            }
        }
    @staticmethod  
    def less(prop, val):
        return {
            "property": prop,
            "number": {
                "less_than": val
            }
        }

    # TODO: maybe I should add filters for greater_than_or_equal_to & less_than_or_equal_to

    @staticmethod
    def is_empty(prop, val):
        filter_object = {
            "property": prop
        }
        if val:
            filter_object['number']['is_empty'] = True
        else:
            filter_object['number']['is_not_empty'] = True
        return filter_object



class CheckboxFilter:
    @staticmethod  
    def checked(prop, val):
        return {
            "property": prop,
            "boolean": {
                "equals": val
            }
        }




class SelectFilter:
    @staticmethod  
    def equals(prop, val):
        return {
            "property": prop,
            "select": {
                "equals": val
            }
        }
    @staticmethod  
    def not_equals(prop, val):
        return {
            "property": prop,
            "select": {
                "equals": val
            }
        }

    @staticmethod
    def is_empty(prop, val):
        filter_object = {
            "property": prop
        }
        if val:
            filter_object['select']['is_empty'] = True
        else:
            filter_object['select']['is_not_empty'] = True
        return filter_object




class MultiSelectFilter:
    @staticmethod  
    def contains(prop, val):
        return {
            "property": prop,
            "multi_select": {
                "contains": val
            }
        }
    @staticmethod  
    def not_contains(prop, val):
        return {
            "property": prop,
            "multi_select": {
                "does_not_contain": val
            }
        }

    @staticmethod
    def is_empty(prop, val):
        filter_object = {
            "property": prop
        }
        if val:
            filter_object['multi_select']['is_empty'] = True
        else:
            filter_object['multi_select']['is_not_empty'] = True
        return filter_object




class RelationFilter:
    @staticmethod  
    def contains(prop, val):
        return {
            "property": prop,
            "relation": {
                "contains": val
            }
        }
    @staticmethod  
    def not_contains(prop, val):
        return {
            "property": prop,
            "relation": {
                "does_not_contain": val
            }
        }

    @staticmethod
    def is_empty(prop, val):
        filter_object = {
            "property": prop
        }
        if val:
            filter_object['relation']['is_empty'] = True
        else:
            filter_object['relation']['is_not_empty'] = True
        return filter_object




class DateFilter:
    @staticmethod  
    def equals(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "equals": val
            }
        }

    @staticmethod  
    def before(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "before": val
            }
        }
    @staticmethod  
    def after(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "after": val
            }
        }

    @staticmethod  
    def past_week(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "past_week": {}
            }
        }
    def next_week(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "next_week": {}
            }
        }

    @staticmethod  
    def past_month(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "past_month": {}
            }
        }
    def next_month(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "next_month": {}
            }
        }

    @staticmethod  
    def past_year(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "past_year": {}
            }
        }
    def next_year(prop, val, type="date"):
        return {
            "property": prop,
            type: {
                "next_year": {}
            }
        }

    @staticmethod
    def is_empty(prop, val, type="date"):
        filter_object = {
            "property": prop
        }
        if val:
            filter_object[type]['is_empty'] = True
        else:
            filter_object[type]['is_not_empty'] = True
        return filter_object