import time
import threading
from kivy.app import App
from kivy.uix.modalview import ModalView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.button import Button
from kivy.properties import ObjectProperty


class Test(App):
    popup = ObjectProperty(allownone=True)
    progressbar = ObjectProperty(allownone=True)

    def run_thread(self, *_):
        self.progressbar = ProgressBar(max=100)
        self.popup = ModalView(auto_dismiss=False)
        self.popup.add_widget(self.progressbar)
        self.popup.open()
        thread = threading.Thread(target=self.thread_function)
        thread.start()

    def thread_function(self):
        while True:
            self.progressbar.value += 1
            time.sleep(.1)  #Placeholder, actual processing would be done here
            if self.progressbar.value == 100:
                break
        self.popup.dismiss()

    def build(self):
        return Button(text="Run Thread", on_release=self.run_thread)

Test().run()
