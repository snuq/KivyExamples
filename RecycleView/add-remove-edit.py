from kivy.app import App
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.lang.builder import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
KV = """
<EditPopup>:
    orientation: 'vertical'
    TextInput:
        text: root.text
        on_text: root.text = self.text
    BoxLayout:
        Button:
            text: 'Confirm'
            on_release: root.owner.edit_element(root.index, root.text)
            on_release: root.owner.popup.dismiss()
        Button:
            text: 'Cancel'
            on_release: root.owner.popup.dismiss()

<RecycleItem>:
    orientation: 'horizontal'
    Label:
        text: root.text
    Button:
        size_hint_x: .2
        text: 'Edit'
        on_release: root.owner.start_edit_element(root)
    Button:
        size_hint_x: .2
        text: 'Remove'
        on_release: root.remove()

BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: .1
        TextInput:
            id: newItem
        Button:
            disabled: not newItem.text
            text: 'Add'
            on_press: app.add_element(newItem.text)
    Widget:
        size_hint_y: .05
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

class EditPopup(BoxLayout):
    text = StringProperty()
    index = NumericProperty()
    owner = ObjectProperty()


class RecycleItem(RecycleDataViewBehavior, BoxLayout):
    owner = ObjectProperty()
    index = NumericProperty()
    text = StringProperty()
    add = BooleanProperty(False)
    animate_length = NumericProperty(.25)
    animation = ObjectProperty(allownone=True)
    o_pos = ListProperty()
    o_opacity = NumericProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        if data['add']:
            self.o_opacity = self.opacity
            self.opacity = 0
            self.animation = Animation(opacity=self.o_opacity, duration=self.animate_length)
            self.animation.start(self)
            self.animation.bind(on_complete=self.animate_finish)
            self.owner.data[self.index]['add'] = False
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

    def remove(self):
        if not self.animation:
            self.o_pos = self.pos
            self.o_opacity = self.opacity
            self.animation = Animation(opacity=0, duration=self.animate_length, pos=(self.pos[0]-self.width, self.pos[1]))
            self.animation.start(self)
            self.animation.bind(on_complete=self.remove_finish)

    def remove_finish(self, *_):
        self.owner.delete_element(self.index)
        self.opacity = self.o_opacity
        self.pos = self.o_pos
        self.animate_finish()

    def animate_finish(self, *_):
        self.animation = None

class Test(App):
    data = ListProperty()
    popup = ObjectProperty(allownone=True)

    def start_edit_element(self, item):
        self.popup = Popup(title='Edit Element', content=EditPopup(text=item.text, index=item.index, owner=self), size_hint=(.5, .3))
        self.popup.open()

    def edit_element(self, index, text):
        self.data[index]['text'] = text
        self.data[index]['add'] = True
        self.root.ids.rv.refresh_from_data()

    def add_element(self, text):
        self.data.insert(0, {"text": text, "owner": self, "add": True})

    def delete_element(self, index):
        self.data.pop(index)

    def build(self):
        self.data = [{"text": "Label "+str(x+1), "owner": self, "add": False} for x in range(10)]
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
