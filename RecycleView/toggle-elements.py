from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.togglebutton import ToggleButton
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:
    on_release: self.owner.data[self.index]['state'] = self.state

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
    owner = ObjectProperty()
    index = NumericProperty(0)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{"text": "Label "+str(x), 'owner': self, 'state': 'normal'} for x in range(20)]
        return Builder.load_string(KV)

Test().run()
