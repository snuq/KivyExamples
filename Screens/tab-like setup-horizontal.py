from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
KV = """
BoxLayout:
    orientation: 'horizontal'
    BoxLayout:
        orientation: 'vertical'
        size_hint_x: None
        width: 80
        Widget:
        Button:
            text: '1'
            on_release: screenManager.current='first'
        Button:
            text: '2'
            on_release: screenManager.current='second'
        Button:
            text: '3'
            on_release: screenManager.current='third'
        Widget:
    ScreenManager:
        id: screenManager
        Screen:
            name: 'first'
            Label:
                text: 'First Screen'
        Screen:
            name: 'second'
            Label:
                text: 'Second Screen'
        Screen:
            name: 'third'
            Label:
                text: 'Third Screen'
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

Test().run()
