"""Example of a customized scatterlayout that prevents the content from being scrolled out of the visible area."""
from kivy.app import App
from scatterlayout import *
KV = """
BoxLayout:
    padding: 100, 0
    orientation: 'vertical'
    Widget:
    BoxLayout:
        canvas.after:
            Color:
                rgba: 1, 1, 1, 0.25
            Rectangle:
                size: self.size
                pos: self.pos
        LimitedScatter:
            Label:
                canvas.before:
                    Color:
                        rgba: .5, .5, .5, 1
                    Rectangle:
                        size: self.size
                        pos: self.pos
                font_size: 100
                text: 'Image'
    Widget:
"""

class Test(App):
    def build(self):
        from kivy.lang.builder import Builder
        return Builder.load_string(KV)

if __name__ in ('__main__'):
    Test().run()