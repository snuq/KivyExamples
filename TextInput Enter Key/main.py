"""Example of a custom TextInput that responds to the enter key"""
from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    padding: 100, 200
    NormalInput:
        multiline: False
        text: 'Yay'
        press_enter: app.enter_function
"""

class NormalInput(TextInput):
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[0] == 13:
            self.press_enter(self.text)
        super().keyboard_on_key_down(window, keycode, text, modifiers)

    def press_enter(self, text):
        pass

class Test(App):
    def enter_function(self, text):
        print('Enter pressed, text is: '+text)

    def build(self):
        return Builder.load_string(KV)

Test().run()
