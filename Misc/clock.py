from datetime import datetime
from math import cos, sin, pi
from kivy.app import runTouchApp
from kivy.clock import Clock
from kivy.properties import *
from kivy.graphics import Line, Color
from kivy.uix.widget import Widget


class SimpleClock(Widget):
    mid_x = NumericProperty()
    mid_y = NumericProperty()
    max_radius = NumericProperty()
    hour = NumericProperty(0)
    minute = NumericProperty(0)
    second = NumericProperty(0)
    hour_line = None
    minute_line = None
    second_line = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hour_line = Line()
        self.minute_line = Line()
        self.second_line = Line()
        self.canvas.add(Color(1, 1, 1))
        self.canvas.add(self.hour_line)
        self.canvas.add(self.minute_line)
        self.canvas.add(self.second_line)
        Clock.schedule_interval(self.set_current_time, 0.03333)

    def on_size(self, *_):
        self.mid_x = self.width / 2
        self.mid_y = self.height / 2
        self.max_radius = min(self.mid_x, self.mid_y)
        self.redraw()

    def set_current_time(self, *_):
        now = datetime.now()
        self.hour = now.hour
        self.minute = now.minute
        self.second = now.second + (now.microsecond / 1000000)
        self.redraw()

    def hand_loc(self, time, length):
        radians = time * 2 * pi
        return length * sin(radians), length * cos(radians)

    def redraw(self, *_):
        second_per = self.second / 60
        minute_per = (self.minute + second_per) / 60
        hour_per = (self.hour + minute_per) / 12
        second_loc = self.hand_loc(second_per, self.max_radius)
        minute_loc = self.hand_loc(minute_per, self.max_radius)
        hour_loc = self.hand_loc(hour_per, self.max_radius / 2)
        self.hour_line.points = [self.mid_x, self.mid_y, self.mid_x + hour_loc[0], self.mid_y + hour_loc[1]]
        self.minute_line.points = [self.mid_x, self.mid_y, self.mid_x + minute_loc[0], self.mid_y + minute_loc[1]]
        self.second_line.points = [self.mid_x, self.mid_y, self.mid_x + second_loc[0], self.mid_y + second_loc[1]]


runTouchApp(SimpleClock())
