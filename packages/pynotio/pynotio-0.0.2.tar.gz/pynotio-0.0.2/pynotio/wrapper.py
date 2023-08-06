import requests
from .page import Page
from .blocks import Block
from .richtext import RichText

class Notion:
    key = None
    api_version = '2021-08-16'

    def __init__(self, key):
        Notion.key = key


    def get_basic_headers(self):
        return {
            'Notion-Version': Notion.api_version,
            'Authorization': 'Bearer ' + Notion.key
        }


    def req_get(self, url, params = {}, headers = {}):
        headers.update(self.get_basic_headers())
        response = requests.get(url, json = params, headers = headers)
        return response.json()

    def req_post(self, url, params = {}, headers = {}):
        headers.update(self.get_basic_headers())
        response = requests.post(url, json = params, headers = headers)
        return response.json()

    def req_put(self, url, params = {}, headers = {}):
        headers.update(self.get_basic_headers())
        response = requests.put(url, json = params, headers = headers)
        return response.json()

    def req_delete(self, url, params = {}, headers = {}):
        headers.update(self.get_basic_headers())
        response = requests.delete(url, json = params, headers = headers)
        return response.json()

    def req_patch(self, url, params = {}, headers = {}):
        headers.update(self.get_basic_headers())
        response = requests.patch(url, json = params, headers = headers)
        return response.json()


    def get_page(self, page_id, lazy = False):
        page = Page(page_id, lazy = lazy, notion_obj = self)
        return page

    
    def db_query(self, db_id, filter = {}, sorts = []):
        data = {}
        if len(filter) != 0:
            data['filter'] = filter
        if len(sorts) != 0:
            data['sorts']

        response = self.req_post(f'https://api.notion.com/v1/databases/{db_id}/query', data)
        result = []
        for page in response['results']:
            result.append(Page(data = page, notion_obj = self))
        return result

    
    def create_rich_text(self, text):
        return RichText(text)

    def create_paragraph(self, rt = None):
        b = Block()
        b.type = 'paragraph'
        if rt is not None:
            if isinstance(rt, list):
                b.rich_text_objects += rt
            else:
                b.append_richtext(rt)
        return b
        