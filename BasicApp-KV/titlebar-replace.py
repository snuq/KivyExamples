from kivy.app import App
from kivy.properties import *
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.lang.builder import Builder
Builder.load_string("""
<TitleBar@BoxLayout>:
    size_hint_y: 0.1
    Label:
        text: 'My App'
    Button:
        draggable: False
        size_hint_x: 0.2
        text: 'Minimize'
        on_release: app.minimize()
    Button:
        draggable: False
        size_hint_x: 0.2
        text: 'Restore' if app.window_maximized else 'Maximize'
        on_release: app.maximize_toggle()
    Button:
        draggable: False
        size_hint_x: 0.2
        text: 'Close'
        on_release: app.stop()
""")

class Test(App):
    window_maximized = BooleanProperty(False)

    def build(self):
        Window.bind(on_maximize=self.set_maximized)
        Window.bind(on_restore=self.unset_maximized)
        Window.custom_titlebar = True
        titlebar = Factory.TitleBar()
        Window.set_custom_titlebar(titlebar)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(titlebar)
        layout.add_widget(Label(text='Main Area'))
        return layout

    def set_maximized(self, *_):
        self.window_maximized = True

    def unset_maximized(self, *_):
        self.window_maximized = False

    def maximize_toggle(self):
        if self.window_maximized:
            Window.restore()
        else:
            Window.maximize()

    def minimize(self):
        Window.minimize()

Test().run()
