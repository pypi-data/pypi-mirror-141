from Notion.properties import Prop
from Notion.blocks import Block
import json

class Page:
    def __init__(self, id = -1, lazy = False, notion_obj = None, data = None):
        self.notion_obj = None # Instance of wrapper. Used to do something with page using requests to Notion
        self.data = {} # page's data
        self.id = None # page's id
        self.content = [] # children blocks of the page
        
        if notion_obj is None:
            raise RuntimeError('Page instance can be created only using Notion object')
        else:
            self.notion_obj = notion_obj
            if data is not None:
                self.data = data
                self.id = data['id']
                self.content = []
            else:
                self.id = id
                self.data = { 
                    'id': id,
                    'raw_content': {
                        'results': []
                    },
                    'plaintext': []
                }
                self.content = []
                if not lazy:
                    self.load_data().load_content()


    def __str__(self):
        return self.get_json()
    def __repr__(self):
        return self.get_json()

    def get_json(self):
        return json.dumps(self.data, indent=4)


    def get_data(self):
        return self.data
    def get_title(self):
        return self.data['properties']['title']['plain_text']
    def get_cover(self):
        return self.data['cover']['external']['url']
    def get_created_time(self):
        return self.data['created_time']

    def get_prop(self, prop):
        return Prop(self.data['properties'][prop])
    def get_prop_value(self, prop):
        return self.get_prop(prop).get_value()
        

    def append_block(self, block):
        data = { 'children': [block.get_json()] }
        self.notion_obj.req_patch(f'https://api.notion.com/v1/blocks/{self.id}/children', data)
        self.data['raw_content']['results'].append(block.get_json())
        self.data['plaintext'].append(block.get_plaintext())
        self.content.append(block)
        return self


    def load_data(self):
        self.data = self.notion_obj.req_get(f'https://api.notion.com/v1/pages/{self.id}')
        return self

    def load_content(self):
        self.data['has_children'] = self.notion_obj.req_get(f'https://api.notion.com/v1/blocks/{self.id}')['has_children']
        if self.data['has_children']:
            self.data['raw_content'] = self.notion_obj.req_get(f'https://api.notion.com/v1/blocks/{self.id}/children')
            self.content = []
            self.data['plaintext'] = []
            for block in self.data['raw_content']['results']:
                b = Block(block)
                self.content.append(b)
                self.data['plaintext'].append(b.get_plaintext())
        return self

    # state-checkers
    def is_data_loaded(self):
        return 'properties' in self.data