from kivy.app import App
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    orientation: 'horizontal'
    Label:
        text: 'test'
        size_hint_max_x: self.texture_size[0] + 20
    Button:
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

Test().run()
