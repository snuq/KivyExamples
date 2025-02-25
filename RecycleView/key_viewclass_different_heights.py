"""Example showing how to use the key_viewclass variable to have different widgets in a RecycleView"""
from kivy.app import App
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
from random import choice
KV = """
<BasicLabel@Label>:

<BasicButton@Button>:

RecycleView:
    data: app.data
    key_viewclass: 'widget'  
    RecycleBoxLayout:
        key_size: 'widget_size'  #This is needed to encode the size of the widget in the data list, just setting widget size is not enough
        default_size_hint: 1, None
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""
class Test(App):
    data = ListProperty()
    def build(self):
        self.data = []
        for x in range(50):
            if choice([True, False]):
                self.data.append({"text": "Widget "+str(x), "widget": 'BasicLabel', 'widget_size': (0, 40)})
            else:
                self.data.append({"text": "Widget "+str(x), "widget": 'BasicButton', 'widget_size': (0, 80)})
        return Builder.load_string(KV)

Test().run()
