"""
Demonstrates an unusual way to bind multiple properties to the same return function using a single alias property as a manager.
"""

from kivy.app import App
from kivy.properties import *
from kivy.uix.button import Button

class MyButton(Button):
    def refresh(self, *_):
        #This function will be called when any property bound with the property_overlord is changed
        print('properties have changed')

    property_overlord = AliasProperty(refresh, None, bind=['size', 'width', 'height'])

class Test(App):
    def build(self):
        return MyButton(text='Hello World')

Test().run()