from kivy.app import App
from kivy.properties import *
from kivy.lang.builder import Builder
KV = """
<ColoredButton@Button>:
    background_color: app.bg
    color: app.text

<ColoredLabel@Label>:
    color: app.text

BoxLayout:
    orientation: 'vertical'
    ColoredLabel:
        text: 'First'
    ColoredButton:
        text: 'Second'
    ColoredButton:
        text: 'Third'
"""

class Test(App):
    bg = ColorProperty([1.5, 2, 2.5])
    text = ColorProperty([0, .5, 0])

    def build(self):
        return Builder.load_string(KV)

Test().run()
