"""Example showing how to properly handle RecycleView items that can have edit-able data.
This more complex version also shows how to use complex widgets in a RecycleView"""
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty, ListProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:
    orientation: 'horizontal'
    Label:
        text: root.label_text
    TextInput:
        text: root.input_text
        on_text: root.set_text(self.text)

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

class RecycleItem(RecycleDataViewBehavior, BoxLayout):
    owner = ObjectProperty()
    index = NumericProperty(0)
    input_text = StringProperty()
    label_text = StringProperty()

    def set_text(self, text):
        if self.owner is not None:
            self.owner.data[self.index]['input_text'] = text
    
    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

class Test(App):
    data = ListProperty()

    def build(self):
        self.data = [{'label_text': "Label "+str(x), "input_text": "Input "+str(x), 'owner': self} for x in range(20)]
        return Builder.load_string(KV)

Test().run()