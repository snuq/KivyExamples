from kivy.app import App
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    Button:
        text: 'Yay'
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
