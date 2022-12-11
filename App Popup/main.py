"""
An example of how to store a popup dialog in the app class to help make popup management easier.
"""
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    Button:
        text: 'Open Popup'
        on_release: app.open_popup()
        
<PopupContent>:
    orientation: 'vertical'
    Label:
        text: 'Popup content'
    Button:
        text: 'Close Popup'
        on_release: app.dismiss_popup()
"""

class PopupContent(BoxLayout):
    pass

class Test(App):
    popup = ObjectProperty(allownone=True)

    def dismiss_popup(self, *_):
        if self.popup:
            self.popup.dismiss()
            self.popup = None
            return True
        return False

    def open_popup(self):
        self.dismiss_popup()
        content = PopupContent()
        self.popup = Popup(title="Popup", content=content, size_hint=(0.9, 0.9), auto_dismiss=False)
        self.popup.open()

    def build(self):
        return Builder.load_string(KV)

Test().run()
