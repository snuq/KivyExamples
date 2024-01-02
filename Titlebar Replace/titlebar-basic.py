from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.factory import Factory
from kivy.lang.builder import Builder
Builder.load_string("""
<TitleBar@Label>:
    size_hint_y: 0.1
    text: 'My App'
""")

class Test(App):
    def build(self):
        Window.custom_titlebar = True
        titlebar = Factory.TitleBar()
        Window.set_custom_titlebar(titlebar)
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(titlebar)
        layout.add_widget(Label(text='Main Area'))
        return layout

Test().run()
