from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
KV = """
MyLayout:
    padding: self.width/4, self.height/6
    Button:
        text: 'Yay'
        on_press: root.my_function()
"""

class MyLayout(BoxLayout):
    def my_function(self):
        print('yup')

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
