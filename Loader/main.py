import threading
import time
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.app import App
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.modalview import ModalView
from kivy.lang.builder import Builder
KV = """
<Loading>:
    Label:
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.rotation
                axis: 0,0,1
                origin: self.center
        canvas.after:
            PopMatrix
        text: 'Loading...'

Button:
    text: 'Start Loading'
    on_release: app.start_load()
"""

class Loading(ModalView):
    load_function = ObjectProperty(allownone=True)
    thread = ObjectProperty(allownone=True)
    auto_dismiss = False
    rotation = NumericProperty(0)
    animate = ObjectProperty(allownone=True)
    
    def on_load_function(self, *_):
        if self.load_function:
            self.animate = Animation(rotation=0, duration=0) + Animation(rotation=360, duration=2)
            self.animate.repeat = True
            self.animate.start(self)
            self.thread = threading.Thread(target=self.thread_function, daemon=True)
            self.thread.start()
            Clock.schedule_once(lambda x: self.open())  #needs to be delayed or it closes kivy??

    def thread_function(self):
        self.load_function()
        self.dismiss()
        self.animate.cancel(self)

class Test(App):
    def build(self):
        return Builder.load_string(KV)

    def load_test_func(self):  #this function can be anything that takes some time to complete
        time.sleep(3)

    def start_load(self):
        loadtest = Loading(load_function=self.load_test_func)

Test().run()
