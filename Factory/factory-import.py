"""Example showing how to define a custom widget in kvlang, then use it in python with kivy's Factory"""
from kivy.app import App
from kivy.factory import Factory
from kivy.lang.builder import Builder
Builder.load_string("""
<MyButton@Button>:
    text: 'Yay'
""")

class Test(App):
    def build(self):
        return Factory.MyButton()

Test().run()
