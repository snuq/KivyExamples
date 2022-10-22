import time
from kivy.app import App
from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty
import threading
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    Button:
        text: 'Run Thread' if app.thread is None else 'Cancel Thread'
        on_press: app.toggle_thread()
    Label:
        canvas.before:
            Color:
                rgba: 1, 1, 1, 0.5
            Rectangle:
                pos: self.pos
                size: self.size[0] * (app.thread_percent / 100), self.size[1]
        text: 'Thread Percent: '+str(app.thread_percent) if app.thread else 'Thread Stopped'
"""

class Test(App):
    canceling_thread = BooleanProperty(False)
    thread = ObjectProperty(allownone=True)
    thread_percent = NumericProperty(0)

    def build(self):
        return Builder.load_string(KV)

    def toggle_thread(self):
        if self.thread is not None:  #Thread is already running, cancel it
            self.canceling_thread = True
            return
        self.canceling_thread = False
        self.thread_percent = 0
        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()

    def thread_function(self):
        while not self.canceling_thread:  #This is the main loop for the thread
            self.thread_percent += 1
            time.sleep(.2)  #Placeholder, actual processing would be done here
            if self.thread_percent == 100:  #Check if processing is done
                break
        self.thread = None  #Cleanup after thread loop is done

    def on_stop(self):
        self.canceling_thread = True
        while self.thread is not None:  #Wait for thread to stop so kivy won't crash
            time.sleep(0.01)

Test().run()