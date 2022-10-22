from kivy.app import App
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    padding: 100
    Button:
        canvas.before:
            Color:
                rgba: (1,1,1,1) if self.state == 'normal' else (.9,.9,.9,1)
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [30]
        background_color: 0,0,0,0
        color: 0,0,0,1
        text: 'Yay'
"""
class Test(App):
    def build(self):
        return Builder.load_string(KV)
Test().run()
