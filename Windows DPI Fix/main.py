from kivy.utils import platform
if platform == 'win':
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)

from kivy.app import App
from kivy.uix.button import Button

class Test(App):
    def build(self):
        return Button(text='Hello World')

if __name__ == '__main__':
    Test().run()
