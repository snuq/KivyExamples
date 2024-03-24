import time
from math import fsum
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.lang.builder import Builder

class Test(App):
    last_time = 0
    frame_intervals = []
    fps = StringProperty()

    def update_fps(self, *_):  #averages out all frame intervals taken since last call and puts that in self.fps
        average_time = fsum(self.frame_intervals) / len(self.frame_intervals)
        self.fps = str(int(round(1 / average_time)))
        self.frame_intervals = []

    def calculate_frame(self, *_):  #stores time since last call in self.frame_intervals
        current_time = time.time()
        self.frame_intervals.append(current_time - self.last_time)
        self.last_time = current_time

    def build(self):
        Clock.schedule_interval(self.calculate_frame, 0)  #records frame interval for every frame
        Clock.schedule_interval(self.update_fps, 0.5)  #updates fps variable at a more human-readable rate
        return Builder.load_string("""
Label:
    text: app.fps
""")

Test().run()
