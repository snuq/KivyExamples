"""Example showing how to use RecycleView with elements that need to change their own variables."""
from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.lang.builder import Builder
KV = """
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

class RecycleItem(RecycleDataViewBehavior, ToggleButton):
    owner = ObjectProperty()  #should be set to the location where the data list is stored for easy access
    index = NumericProperty(0)  #store the data index locally to make it easier to update original data

    def on_state(self, *_):  #Variable must be copied back to data list after being updated locally
        self.owner.data[self.index]['state'] = self.state

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{"text": "Label "+str(x), 'owner': self, 'state': 'normal'} for x in range(20)]
        return Builder.load_string(KV)

Test().run()
