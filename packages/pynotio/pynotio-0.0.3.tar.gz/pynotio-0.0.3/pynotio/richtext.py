class RichText:
    def __init__(self, data=None):
        if data is not None:
            if isinstance(data, dict):
                self.data = data
                self.is_link = data['href'] is not None
                self.href = data['href']
                self.is_bold = data['annotations']['bold']
                self.is_italic = data['annotations']['italic']
                self.is_underlined = data['annotations']['underline']
                self.is_strikethrough = data['annotations']['strikethrough']
                self.is_code = data['annotations']['code']
                self.color = data['annotations']['color']
                self.text = data['plain_text']
            elif isinstance(data, str):
                self.text = data
                self.is_link = False
                self.href = None
                self.is_bold = False
                self.is_italic = False
                self.is_underlined = False
                self.is_strikethrough = False
                self.is_code = False
                self.color = 'default'

    def toggle_bold(self):
        self.is_bold = not self.is_bold
        return self
    def toggle_italic(self):
        self.is_italic = not self.is_italic
        return self
    def toggle_underlined(self):
        self.is_underlined = not self.is_underlined
        return self
    def toggle_striketrough(self):
        self.is_strikethrough = not self.is_strikethrough
        return self

    def set_link(self, href):
        self.is_link = True
        self.href = href
        return self


    def get_plaintext(self):
        return self.text

    def set_text(self, text):
        self.text = text
        return self

    def get_json(self):
        data =  {
            'type': 'text',
            'plain_text': self.text,
            'annotations': {
                'bold': self.is_bold,
                'code': self.is_code,
                'color': self.color,
                'italic': self.is_italic,
                'strikethrough': self.is_strikethrough,
                'underline': self.is_underlined,
            },
            'text': {
                'content': self.text,
            }
        }
        if self.href is not None:
            data['href'] = self.href
            data['text']['link'] = {
                'url': self.href
            }

        return data
