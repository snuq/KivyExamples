from kivy.app import App
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.properties import *

class Test(App):
    horizontal = BooleanProperty(True)

    def check_aspect(self, *_):
        if Window.width > Window.height:
            self.horizontal = True
        else:
            self.horizontal = False

    def build(self):
        Window.bind(on_draw=self.check_aspect)
        return Builder.load_string("""
Label:
    text: 'Horizontal App' if app.horizontal else 'Vertical App'
""")

Test().run()
