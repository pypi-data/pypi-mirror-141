from .richtext import RichText
from pprint import pprint

class Block:
    def __init__(self, data = None):
        if data is not None:
            self.data = data
            self.type = data['type']
            self.has_children = data['has_children']
            self.archived = data['archived']
            self.id = data['id']

            self.parse_richtext_list()
        else:
            self.rich_text_objects = []
            self.has_children = False
            self.archived = False

    def parse_richtext_list(self):
        text_list = self.data[self.type]['text']
        self.rich_text_objects = []
        for rt_obj in text_list:
            richtextobj = RichText(rt_obj)
            self.rich_text_objects.append(richtextobj)

    def append_richtext(self, rt):
        if isinstance(rt, list):
            self.rich_text_objects.extend(rt)
        else:
            self.rich_text_objects.append(rt)
        return self

    def get_plaintext(self):
        result = ''
        for rto in self.rich_text_objects:
            result += rto.get_plaintext()
        return result

    def get_json(self):
        rt_list = []
        for rt in self.rich_text_objects:
            rt_list.append(rt.get_json())
        return {
            'object': 'block',
            'type': self.type,
            'archived': False,
            'has_children': self.has_children,
            self.type: {
                'text': rt_list
            }
        }