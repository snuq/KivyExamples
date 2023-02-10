"""Example of how to easily call another widget from RecycleView elements."""
from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
KV = """
Button:
    text: 'Open Popup'
    on_release: app.open_popup()

<RecycleItem>:
    on_press: self.owner.recycle_button(self.variable)

<RecyclePopup>:
    RecycleView:
        scroll_type: ['bars', 'content']
        bar_width: 20
        data: root.data
        viewclass: 'RecycleItem'
        RecycleBoxLayout:
            spacing: 10
            default_size: None, dp(80)
            default_size_hint: 1, None
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
"""

class RecyclePopup(ModalView):
    data = ListProperty()

    def recycle_button(self, text):
        print(text)

class RecycleItem(Button):
    owner = ObjectProperty()
    variable = NumericProperty()

class Test(App):
    def build(self):
        return Builder.load_string(KV)

    def open_popup(self):
        popup = RecyclePopup()
        popup.data = [{"text": "Label "+str(x), 'owner': popup, 'variable': x} for x in range(20)]
        popup.open()

Test().run()
