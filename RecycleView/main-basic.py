"""Basic example of how to use a RecycleView widget."""
from kivy.app import App
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
KV = """
RecycleView:
    data: app.data
    viewclass: 'Label'
    RecycleBoxLayout:
        default_size: None, dp(80)
        default_size_hint: 1, None
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""
class Test(App):
    data = ListProperty()
    def build(self):
        self.data = [{"text": "Label "+str(x)} for x in range(20)]
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
