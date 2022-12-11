"""Example showing how to use complex widgets as RecycleView items."""
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:
    orientation: 'horizontal'
    Label: 
        text: root.label_text
    Button:
        text: root.button_text

RecycleView:
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

class RecycleItem(BoxLayout):
    label_text = StringProperty()
    button_text = StringProperty()

class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{"label_text": "Label "+str(x), 'button_text': "Button "+str(x)} for x in range(20)]
        return Builder.load_string(KV)

Test().run()
