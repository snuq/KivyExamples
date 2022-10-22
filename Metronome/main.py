from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, NumericProperty, DictProperty
from kivy.uix.widget import Widget
from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.clock import Clock
import time
from threading import Thread

Builder.load_string("""
<MainScreen>:
    orientation: 'vertical'
    MetronomeNeedle:
        id: metronomeNeedle
    Button:
        size_hint_y: None
        height: 40
        text: 'Start Metronome' if not app.metronome_updater else 'Stop Metronome'
        on_release: app.toggle_metronome()

<MetronomeNeedle>:
    canvas.before:
        Color:
            rgba: 0,0,0,1
        Rectangle:
            size: self.size
            pos: self.pos
        Color:
            rgba: 1,1,1,1
        Rectangle:
            size: self.width * self.needle_pos, self.height
            pos: self.pos
""")

class MainScreen(BoxLayout):
    pass

class MetronomeNeedle(Widget):
    needle_pos = NumericProperty(.5)
    animation = None
    
    def animate(self, duration, forward):
        if self.animation is not None:
            self.animation.stop(self)
        self.needle_pos = 0.5
        if forward:
            self.needle_pos = 0
            self.animation = Animation(needle_pos=1, duration=duration)
        else:
            self.needle_pos = 1
            self.animation = Animation(needle_pos=0, duration=duration)
        self.animation.start(self)
    
    def reset(self):
        if self.animation is not None:
            self.animation.stop(self)
        self.animation = Animation(needle_pos=0.5, duration=0.5)
        self.animation.start(self)

class Test(App):
    screen = None
    stop_metronome = False
    metronome_updater = ObjectProperty(allownone=True)

    def toggle_metronome(self):
        if self.metronome_updater is not None:
            self.stop_metronome = True
        else:
            self.start_metronome()

    def start_metronome(self):
        self.stop_metronome = False
        self.metronome_updater = Thread(target=self.metronome_update_thread)
        self.metronome_updater.start()

    def metronome_update_thread(self):
        needle = self.screen.ids['metronomeNeedle']
        beat_length = .5
        forward = True
        while not self.stop_metronome:
            needle.animate(beat_length, forward)
            #Play audio sound here
            time.sleep(beat_length)
            forward = not forward
        needle.reset()
        self.metronome_updater = None
    
    def on_stop(self):
        self.stop_metronome = True
    
    def build(self):
        self.screen = MainScreen()
        return self.screen

if __name__ == '__main__':
    Test().run()
