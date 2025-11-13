#Example showing how to replace builtin kivy classes with a modified or custom class

#create/import the replacement class
from kivy.uix.widget import Widget
class BoxLayout(Widget):
    pass

#import the module that contains the class
import kivy.uix.boxlayout

#replace the default class with custom class
kivy.uix.boxlayout.BoxLayout = BoxLayout

#register and replace original class for use in kv language
from kivy.factory import Factory
Factory.unregister('BoxLayout')
Factory.register('BoxLayout', cls=BoxLayout)

#testing
from kivy.app import App
from kivy.lang.builder import Builder
class Test(App):
    def build(self):
        return Builder.load_string("""
BoxLayout:
    Button:
        text: 'Yay'""")

Test().run()
