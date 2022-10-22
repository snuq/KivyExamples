from kivy.app import App
from kivy.animation import Animation
from kivy.uix.button import Button
from kivy.properties import ColorProperty, ObjectProperty, NumericProperty
from kivy.lang.builder import Builder
Builder.load_string("""
<-RoundedButton>:
    canvas.before:
        Color:
            rgba: 1, 1, 1, root.shadow_amount
        BorderImage:
            pos: self.pos[0] + root.shadow_x - root.shadow_x_pos, self.pos[1] - root.shadow_y + root.shadow_y_pos
            size: self.size
            border: [40, 40, 40, 40]
            display_border: [20, 20, 20, 20]
            source: 'shadow2.png'
    canvas:
        Color:
            rgba: self.background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.rounded]
        Color:
            rgba: self.edge_color
        Line:
            width: 1
            rounded_rectangle: (self.pos[0], self.pos[1], self.width, self.height, self.rounded)
        Color:
            rgba: self.color
        Rectangle:
            texture: self.texture
            size: self.texture_size
            pos: int(self.center_x - self.texture_size[0] / 2.), int(self.center_y - self.texture_size[1] / 2.)
    background_color: self.background_color_up
    color: 0,0,0,1
""")

class RoundedButton(Button):
    background_color_down = ColorProperty((.5,.5,.5,1))
    background_color_up = ColorProperty((0.7,0.7,0.7,1))
    edge_color = ColorProperty((0,0,0,.5))
    rounded = NumericProperty(10)
    shadow_x = NumericProperty(10)
    shadow_x_pos = NumericProperty(0)
    shadow_y = NumericProperty(10)
    shadow_y_pos = NumericProperty(0)
    shadow_amount = NumericProperty(0.75)
    animate_duration = NumericProperty(0.05)
    button_animate = ObjectProperty(allownone=True)

    def on_state(self, *_):
        if self.state == 'normal':
            color = self.background_color_up
            shadow_x = 0
            shadow_y = 0
        else:
            color = self.background_color_down
            shadow_x = self.shadow_x
            shadow_y = self.shadow_y
        self.button_animate = Animation(shadow_x_pos=shadow_x, shadow_y_pos=shadow_y, background_color=color, duration=self.animate_duration)
        self.button_animate.start(self)

class Test(App):
    def build(self):
        kv = """
BoxLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    padding: 20
    RoundedButton:
        text: 'Yay'
        """
        return Builder.load_string(kv)
Test().run()
