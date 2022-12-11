"""Example of how to easily call another widget from RecycleView elements."""
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.uix.button import Button
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:
    on_press: self.owner.recycle_button(self.variable)

RecycleView:
    scroll_type: ['bars', 'content']
    bar_width: 20
    data: app.data
    viewclass: 'RecycleItem'
    RecycleBoxLayout:
        spacing: 10
        default_size: None, dp(80)
        default_size_hint: 1, None
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""

class RecycleItem(Button):
    owner = ObjectProperty()
    variable = NumericProperty()

class Test(App):
    data = ListProperty()

    def recycle_button(self, text):
        print(text)

    def build(self):
        self.data = [{"text": "Label "+str(x), 'owner': self, 'variable': x} for x in range(20)]
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
