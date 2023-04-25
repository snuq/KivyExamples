"""Example showing how to use the key_viewclass variable to have different widgets in a RecycleView"""
from kivy.app import App
from kivy.properties import ListProperty
from kivy.lang.builder import Builder
from random import choice
KV = """
RecycleView:
    data: app.data
    key_viewclass: 'widget'             #set this to the variable that holds the class name to use
    RecycleBoxLayout:
        default_size: self.width, dp(80)
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""
class Test(App):
    data = ListProperty()
    def build(self):
        self.data = [{"text": "Widget "+str(x), "widget": choice(['Label', 'Button'])} for x in range(30)]
        return Builder.load_string(KV)

Test().run()
