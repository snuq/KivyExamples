"""Example showing how to fade text in using Kivy's animation."""
from kivy.app import App
from kivy.animation import Animation
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.label import Label
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    orientation: 'vertical'
    Button:
        text: 'Set Var'
        on_release: app.first = 'Test'
    Button:
        text: 'Clear Var'
        on_release: app.first = ''
    FadeLabel:
        text: app.first
"""

class FadeLabel(Label):
    anim = ObjectProperty(allownone=True)
    def cancel_anim(self):
        if self.anim:
            self.anim.stop(self)
            self.anim = None

    def on_text(self, *_):
        self.opacity = 0
        self.cancel_anim()
        if self.text:
            self.anim = Animation(opacity=1, duration=1)
            self.anim.start(self)

class Test(App):
    first = StringProperty('')
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
