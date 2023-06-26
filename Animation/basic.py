from random import random
from kivy.app import App
from kivy.animation import Animation
from kivy.properties import *
from kivy.uix.button import Button

class AnimatedButton(Button):
    animate_color = ColorProperty()  #temporary placeholder variable to enable color animation trigger when changed
    animator = ObjectProperty(allownone=True)  #store animator locally to prevent multiple animations at once and allow modification of animation when running

    def on_release(self):
        self.animate_color = [random(), random(), random()]  #set a color to automatically trigger animation

    def on_animate_color(self, *_):  #automatically called when animate_color is changed
        if self.animator:  #previous animation is already running, need to stop it
            self.animator.cancel(self)
        self.animator = Animation(background_color=self.animate_color, duration=1)
        self.animator.start(self)

class Test(App):
    def build(self):
        return AnimatedButton(text='Click to change color!')

Test().run()