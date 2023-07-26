"""Example of a custom label that will 'ticker' scroll a long line of text."""
from kivy.app import App
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.lang.builder import Builder
KV = """
<-TickerLabel>:
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: 0 - self.ticker_offset, int(self.center_y - self.texture_size[1] / 2.)

BoxLayout:
    orientation: 'vertical'
    TickerLabel:
        text: 'This is a long line of text that should start scrolling automatically when the label is created'
    TickerLabel:
        text: 'This is a long line of text that should start scrolling automatically when the label is created, this one is longer and should scroll at the same speed.'

"""

class TickerLabel(Label):
    ticker_delay = NumericProperty(1)  #delay in seconds before ticker starts, also is pause before scrolling back
    ticker_amount = NumericProperty(1)  #pixels to scroll by on each tick, can be less than 1
    ticker_transition = StringProperty('in_out_sine')  #type of animation to be used, try 'linear' also
    ticker_offset = NumericProperty(0)
    ticker_animate = ObjectProperty(allownone=True)
    ticker_delayer = ObjectProperty(allownone=True)

    def on_size(self, *_):
        self.stop_animate()
        if self.ticker_delayer:
            self.ticker_delayer.cancel()
            self.ticker_delayer = None
        self.ticker_delayer = Clock.schedule_once(self.setup_animate, self.ticker_delay)

    def stop_animate(self, *_):
        if self.ticker_animate:
            self.ticker_animate.cancel(self)
            self.ticker_animate = None
        self.ticker_offset = 0

    def setup_animate(self, *_):
        if not self.texture:
            return
        if self.texture.size[0] > self.width:
            self.ticker_offset = 0
            ticker_per_tick = (self.texture_size[0] - self.width) / self.ticker_amount
            ticker_time = ticker_per_tick / 100
            self.ticker_animate = Animation(ticker_offset=self.texture.width - self.width, duration=ticker_time, t=self.ticker_transition) + Animation(duration=self.ticker_delay) + Animation(ticker_offset=0, duration=ticker_time, t=self.ticker_transition) + Animation(duration=self.ticker_delay)
            self.ticker_animate.repeat = True
            self.ticker_animate.start(self)

class Test(App):
    def build(self):
        return Builder.load_string(KV)

Test().run()
