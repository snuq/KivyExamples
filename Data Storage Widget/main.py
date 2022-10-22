from kivy.app import App
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.widget import Widget
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

class DataStorage(Widget):
    first = StringProperty('Not Set')
    second = NumericProperty(0)

class Test(App):
    def build(self):
        self.data = DataStorage()
        return Builder.load_string(KV)

Test().run()
