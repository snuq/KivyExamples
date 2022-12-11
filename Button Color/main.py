"""
Simple example showing changing a button's background color based on click state.
"""
from kivy.app import App
from kivy.lang.builder import Builder
KV = """
Button:
    background_color: (0,1,0,1) if self.state == 'down' else (2,0,0,1)
    text: 'Press Me' if self.state == 'normal' else 'Thanks!'
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
