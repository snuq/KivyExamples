from kivy.app import App
from kivy.uix.popup import Popup
from kivy.properties import *
from kivy.lang.builder import Builder
KV = """
<MyPopup>:
    Label:
        text: root.myprop

BoxLayout:
    Button:
        text: 'Open Popup'
        on_release: app.open_popup()
"""

class MyPopup(Popup):
    myprop = StringProperty()

class Test(App):
    def open_popup(self):
        popup = MyPopup(myprop='Testing')
        popup.open()

    def build(self):
        return Builder.load_string(KV)

Test().run()