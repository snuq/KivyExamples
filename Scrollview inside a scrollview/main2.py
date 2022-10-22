from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
KV = """
Scroller:
    bar_width: 40
    scroll_type: ['bars', 'content']
    do_scroll_x: False
    Label:
        font_size: 500
        size_hint: None, None
        size: 1000, 1000
        text: 'test'
"""
class Scroller(ScrollView):
    def on_touch_down(self, touch):
        super().on_touch_down(touch)

class Test(App):
    def build(self):
        return Builder.load_string(KV)
Test().run()
