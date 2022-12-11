"""Example that shows how to store multiple kivy properties in an object.
This is useful for grouping large amounts of variables such as theme-related properties into one object."""
from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.event import EventDispatcher
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
KV = """
RootLayout:
    orientation: 'vertical'
    Button:
        text: 'Set vars'
        on_release: root.set_vars()
    Label:
        text: app.data.first
    Label:
        text: 'Second Variable: '+str(app.data.second)
"""

class RootLayout(BoxLayout):
    def set_vars(self):
        app = App.get_running_app()
        app.data.first = 'first variable set'
        app.data.second = 100

class DataStorage(EventDispatcher):
    first = StringProperty('Not Set')
    second = NumericProperty(0)

class Test(App):
    def build(self):
        self.data = DataStorage()
        return Builder.load_string(KV)

Test().run()
