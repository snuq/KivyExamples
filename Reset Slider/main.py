"""Example showing a custom Slider widget that can be reset to default with a double-click."""
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.slider import Slider
from kivy.properties import NumericProperty
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    orientation: 'vertical'
    Label:
        text: 'Double-click to reset slider:'
    ResetSlider:
        min: 0
        max: 1
        value: app.value
        on_value: app.value = self.value
        reset_value: app.reset_slider
"""

class ResetSlider(Slider):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.is_double_tap:
            Clock.schedule_once(self.reset_value, 0.15)  #Delay reset to allow this to work inside scrollviews
            return
        super(ResetSlider, self).on_touch_down(touch)

    def reset_value(self, *_):
        pass

class Test(App):
    value = NumericProperty(0.5)

    def reset_slider(self, *_):
        self.value = 0.5

    def build(self):
        return Builder.load_string(KV)

Test().run()
