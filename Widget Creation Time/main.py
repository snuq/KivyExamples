import time
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
class Test(App):
    def build(self):
        Clock.schedule_once(self.fill_layout)
        return BoxLayout()
    def fill_layout(self, *_):
        start_time = time.time()
        box = self.root
        for index in range(0, 1000):
            b = Button(text='')
            box.add_widget(b)
        print(time.time() - start_time)
Test().run()
