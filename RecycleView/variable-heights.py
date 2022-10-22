from kivy.app import App
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
KV = """
<RecycleItem@Label>:
    size_hint_y: None
    height: self.texture_size[1]
    text_size: self.width, None

RecycleView:
    data: app.data
    viewclass: 'RecycleItem'
    RecycleBoxLayout:
        default_size_hint: 1, None
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""
class Test(App):
    data = ListProperty()
    def build(self):
        self.data = [{"text": "First blahblah"}, {"text": "Second blahblahblahblah blahblahblahblahblahblah"}, {"text": "Third blahblahblahblah blahblahblahblahblahblahblahblahblahblah blahblahblahblahblahblahblahblahblahblah blahblahblahblahblahblahblahblah"}, {"text": "Fourth"}]
        return Builder.load_string(KV)

Test().run()
