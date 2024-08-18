"""
Example showing Recycleview elements that can toggle height based on a click.
"""

from kivy.app import App
from kivy.properties import *
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:

RecycleView:
    data: app.data
    viewclass: 'RecycleItem'
    RecycleBoxLayout:
        spacing: 10
        default_size_hint: 1, None
        default_size: None, 40
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""

class RecycleItem(RecycleDataViewBehavior, ToggleButton):
    small_height = 40
    large_height = 200
    owner = ObjectProperty()
    index = NumericProperty(0)

    def on_state(self, widget, state):
        self.owner.data[self.index]['state'] = state
        self.set_height()

    def set_height(self):
        if self.state == 'normal':
            target_height = self.small_height
        else:
            target_height = self.large_height
        if self.height != target_height:
            self.height = target_height

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return_data = super(RecycleItem, self).refresh_view_attrs(rv, index, data)
        self.set_height()
        return return_data

class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{"text": "Button "+str(x), 'owner': self, 'state': 'normal'} for x in range(20)]
        return Builder.load_string(KV)

Test().run()
