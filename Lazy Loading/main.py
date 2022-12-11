"""
Example of 'lazy loading' of screens.
This delays the importing and creation of screen widgets until they are actually needed which saves on startup time.
"""
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

class Test(App):
    sm = None
    def build(self):
        self.sm = ScreenManager()
        return self.sm

    def on_start(self):
        self.show_screen1()

    def show_screen1(self):
        if 'first' not in self.sm.screen_names:
            from screens import Screen1
            self.sm.add_widget(Screen1(name='first'))
        self.sm.current = 'first'

    def show_screen2(self):
        if 'second' not in self.sm.screen_names:
            from screens import Screen2
            self.sm.add_widget(Screen2(name='second'))
        self.sm.current = 'second'

    def show_screen3(self):
        if 'third' not in self.sm.screen_names:
            from screens import Screen3
            self.sm.add_widget(Screen3(name='third'))
        self.sm.current = 'third'

Test().run()
