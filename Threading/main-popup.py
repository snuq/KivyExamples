"""Example showing how to use a popup to run a thread.
This is useful to lock the interface while something is being calculated."""
import time
import threading
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.button import Button
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
        self.popup = Popup(title='Running Thread', content=Button(text='Please Wait...'), auto_dismiss=False)
        self.popup.open()
        self.thread = threading.Thread(target=self.thread_function)
        self.thread.start()

    def thread_function(self):
        time.sleep(5)
        self.thread = None
        self.popup.dismiss()

    def build(self):
        return Builder.load_string(KV)

Test().run()
