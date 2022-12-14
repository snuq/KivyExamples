"""Very basic threading example."""
import time
import threading
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    Button:
        text: 'Thread Running' if app.thread else 'Run Thread'
        on_press: app.run_thread()
"""

class Test(App):
    thread = ObjectProperty(allownone=True)

    def run_thread(self):
        if self.thread is not None:
            return
        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()

    def thread_function(self):
        time.sleep(5)
        self.thread = None

    def build(self):
        return Builder.load_string(KV)

Test().run()
