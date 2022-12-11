"""Example showing how to remove elements from a RecycleView.  This version includes animations for element removal."""
from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.lang.builder import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
KV = """
<RecycleItem>:
    orientation: 'horizontal'
    Label:
        text: root.text
    Button:
        text: 'Remove'
        on_press: root.remove()

RecycleView:
    id: rv
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
    index = NumericProperty()
    text = StringProperty()
    remove_length = NumericProperty(.25)
    animation = ObjectProperty(allownone=True)
    o_pos = ListProperty()
    o_opacity = NumericProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

    def remove(self):
        if not self.animation:
            self.o_pos = self.pos
            self.o_opacity = self.opacity
            self.animation = Animation(opacity=0, duration=self.remove_length, pos=(self.pos[0]-self.width, self.pos[1]))
            self.animation.start(self)
            self.animation.bind(on_complete=self.remove_finish)

    def remove_finish(self, *_):
        self.owner.delete_element(self.index)
        self.animation = None
        self.opacity = self.o_opacity
        self.pos = self.o_pos

class Test(App):
    data = ListProperty()

    def delete_element(self, index):
        self.data.pop(index)

    def build(self):
        self.data = [{"text": "Label "+str(x), 'owner': self} for x in range(20)]
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
