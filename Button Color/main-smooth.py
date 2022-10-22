from kivy.app import App
from kivy.animation import Animation
from kivy.properties import ColorProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.lang.builder import Builder
Builder.load_string("""
<SmoothButton>:
    background_down: self.background_normal
    background_color: self.smoothcolor
""")

class SmoothButton(Button):
    smoothcolor = ColorProperty((0,1,0,1))
    smoothanimate = ObjectProperty(allownone=True)
    def on_state(self, *_):
        if self.state == 'normal':
            color = (0,1,0,1)
        else:
            color = (2,0,0,1)
        self.smoothanimate = Animation(smoothcolor=color, duration=0.25)
        self.smoothanimate.start(self)

class Test(App):
    def build(self):
        return SmoothButton(text='Press Me!')

Test().run()
