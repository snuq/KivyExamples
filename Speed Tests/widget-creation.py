import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
class Test(App):
    start_time = 0
    def build(self):
        Clock.schedule_once(self.fill_layout)
        return BoxLayout()
    def fill_layout(self, *_):
        start_time = time.time()
        box = self.root
        for index in range(0, 10000):
            b = Label(text='aaaaaaaaaa')
            box.add_widget(b)
        print('Creation time: '+str(time.time() - start_time))
        self.start_time = time.time()
        Clock.schedule_once(self.print_time)
    def print_time(self, *_):
        print('Draw time: '+str(time.time() - self.start_time))
        Clock.schedule_once(self.redraw_layout)
    def redraw_layout(self, *_):
        start_time = time.time()
        for widget in self.root.children:
            widget.texture_update()
        print('Refresh time: '+str(time.time() - start_time))
Test().run()
