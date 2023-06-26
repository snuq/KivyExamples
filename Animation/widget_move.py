"""
An example showing use of the animation class to move a widget around based on user inputs
"""
from kivy.app import App
from kivy.animation import Animation
from kivy.properties import *
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.lang.builder import Builder
Builder.load_string("""
<AnimatedWidget>:
    size_hint: None, None
    size: 100, 100
""")

class RootLayout(RelativeLayout):  #This class just is here as an example to show the movement of the widget
    def on_touch_up(self, touch):
        #just set the animate_pos variable of the widget and it will begin moving there
        self.children[0].animate_pos = touch.pos

class AnimatedWidget(Button):
    animate_pos = ListProperty()
    pos_animator = ObjectProperty(allownone=True)

    def cancel_animation(self, *_):
        self.pos_animator.cancel(self)
        self.pos_animator = None

    def on_animate_pos(self, *_):
        if self.pos_animator:  #previous animation is already running, need to stop it
            animation_type = 'out_quad'  #dont smooth 'in' because widget is already moving
            self.cancel_animation()
        else:  #no animation currently running
            animation_type = 'in_out_quad'
        self.pos_animator = Animation(pos=(self.animate_pos[0]-self.width/2, self.animate_pos[1]-self.height/2), t=animation_type, duration=1)
        self.pos_animator.bind(on_complete=self.cancel_animation)  #calls cancel_animation when done moving to clean up
        self.pos_animator.start(self)

class Test(App):
    def build(self):
        root = RootLayout()
        root.add_widget(AnimatedWidget())
        return root

Test().run()