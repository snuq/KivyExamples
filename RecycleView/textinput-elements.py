from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty, ListProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.textinput import TextInput
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:
    on_text: self.set_text()

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

class RecycleItem(RecycleDataViewBehavior, TextInput):
    owner = ObjectProperty()
    index = NumericProperty(0)

    def set_text(self):
        if self.owner is not None:
            self.owner.data[self.index]['text'] = self.text
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{"text": "Label "+str(x), 'owner': self} for x in range(20)]
        return Builder.load_string(KV)

Test().run()