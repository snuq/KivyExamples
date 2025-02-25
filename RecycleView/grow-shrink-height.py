"""
Example showing Recycleview elements that can toggle height based on a click.
"""

from kivy.app import App
from kivy.properties import *
from kivy.uix.togglebutton import ToggleButton
from kivy.lang.builder import Builder
KV = """
RecycleView:
    data: app.data
    viewclass: 'RecycleItem'
    RecycleBoxLayout:
        spacing: 10
        default_size_hint: 1, None
        key_size: 'current_size'
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""

class RecycleItem(ToggleButton):
    small_height = 40
    large_height = 200
    owner = ObjectProperty()  #stores the widget that holds the data list for easy access
    index = NumericProperty(0)  #need to keep track of thiis to be able to update proper element of data list

    def on_state(self, widget, state):  #need to update recycleview's data as well as self
        self.owner.data[self.index]['state'] = state
        if self.state == 'normal':
            target_height = self.small_height
        else:
            target_height = self.large_height
        self.height = target_height
        self.owner.data[self.index]['current_size'] = (0, target_height)


class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{"index": x, "text": "Button "+str(x), 'owner': self, 'state': 'normal', 'current_size': (0, RecycleItem.small_height)} for x in range(50)]
        return Builder.load_string(KV)

Test().run()