from kivy.app import App
from kivy.uix.screenmanager import Screen, SlideTransition, FadeTransition, SwapTransition
from kivy.lang import Builder
KV = """
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 40
        Button:
            text: 'Screen 1'
            on_release: app.show_screen1()
        Button:
            text: 'Screen 2'
            on_release: app.show_screen2()
        Button:
            text: 'Screen 3'
            on_release: app.show_screen3()
        Widget:
    ScreenManager:
        id: screenManager
        Screen:
            name: 'first'
            Button:
                text: 'First Screen'
        Screen:
            name: 'second'
            Button:
                text: 'Second Screen'
        Screen:
            name: 'third'
            Button:
                text: 'Third Screen'
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

    def show_screen1(self):
        sm = self.root.ids['screenManager']
        sm.transition = SlideTransition()
        sm.transition.direction = 'down'
        sm.current = 'first'

    def show_screen2(self):
        sm = self.root.ids['screenManager']
        sm.transition = FadeTransition()
        sm.current = 'second'

    def show_screen3(self):
        sm = self.root.ids['screenManager']
        sm.transition = SwapTransition()
        sm.current = 'third'

Test().run()
