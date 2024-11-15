from kivy.animation import Animation
from kivy.lang.builder import Builder
from kivy.properties import *
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
Builder.load_string("""
<-NormalTextInput>:
    canvas.before:
        Color:
            rgba: self._current_background_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [self.rounded]
        Color:
            rgba: self.background_border_color
        Line:
            width: self.background_border_width
            rounded_rectangle: (self.pos[0], self.pos[1], self.width, self.height, self.rounded)
        Color:
            rgba: (self.cursor_color if self.focus and not self._cursor_blink and int(self.x + self.padding[0]) <= self._cursor_visual_pos[0] <= int(self.x + self.width - self.padding[2]) else (0, 0, 0, 0))
        Rectangle:
            pos: self._cursor_visual_pos
            size: root.cursor_width, -self._cursor_visual_height
        Color:
            rgba: self.disabled_foreground_color if self.disabled else ((0, 0, 0, 0) if not self.text else self.foreground_color)
    canvas.after:
        Color:
            rgba: self.cursor_color if root._activated else (0, 0, 0, 0)
        Rectangle:  #underline
            pos: self.x + (self.rounded / 2) + (self.width * self.underline_pos * (1 - self._activated)), self.y
            size: (self.width - self.rounded) * self._activated, self._underline_size
        Color:
            rgba: self.hint_text_color if root.animate_hint or not self.text else (0, 0, 0, 0)
        Rectangle:  #hint text
            size: self._hint_label_size
            pos: self.x + self.padding[0], self.y + self.height - self._hint_label_size[1] - (self.height * .2 * (1 - self._activated_hint))
            texture: self._hint_label_texture if self._hint_label_texture else None
    _underline_size: max(1, self.height / 10)
    padding: max(self.height / 8, self.rounded), (self._hint_max_size * 0.3) + (self.height / 8), max(self.height / 8, self.rounded), self.height / 8
    font_size: self.height * 0.5
    multiline: False
""")

class NormalTextInput(TextInput):
    hint_text = StringProperty("Enter Text Here")
    underline_pos = NumericProperty(0.5)  #Horizontal position (percent) from where the underline will grow from
    activate_time = NumericProperty(0.2)  #Time in seconds for the animate in
    deactivate_time = NumericProperty(0.2)  #Time in seconds for the animate out
    background_color_active = ColorProperty((1, 1, 1, 1))  #Color that the background will fade to when the text input is focused
    background_border_color = ColorProperty((0, 0, 0, 0.5))  #Color of the border line
    background_border_width = NumericProperty(1)  #Thickness of the border line
    rounded = NumericProperty(4)  #Radius of rounded corners on background
    animate_hint = BooleanProperty(True)

    _activated = NumericProperty(0)
    _activated_hint = NumericProperty(0)
    _activate_animation = None
    _underline_size = NumericProperty(1)
    _current_background_color = ColorProperty()
    _hint_label = None
    _hint_max_size = NumericProperty(0)
    _hint_min_size = NumericProperty(0)
    def update_hint_label(self):
        if not self._hint_label:
            self._hint_label = Label(opacity=0, size_hint=(None, None), size=(0, 0))
        self._hint_label.color = 1, 1, 1, 1
        self._hint_label.text = self.hint_text
        self._hint_max_size = min(self.font_size, self.height * 0.5)
        self._hint_min_size = self._hint_max_size * 0.5
        target_range = self._hint_max_size - self._hint_min_size
        self._hint_label.font_size = self._hint_min_size + target_range * (1 - self._activated_hint)
        self._hint_label.texture_update()
        if self._hint_label.texture:
            self._hint_label_size = self._hint_label.texture.size
        return self._hint_label.texture
    _hint_label_texture = AliasProperty(update_hint_label, bind=('size', 'font_size', 'hint_text_color', 'hint_text', '_activated_hint'))
    _hint_label_size = ListProperty([1, 1])

    def on_background_color(self, *_):
        self._current_background_color = self.background_color

    def on_focus(self, widget, is_focused):
        if is_focused:
            self.activate()
        else:
            self.deactivate()

    def stop_animation(self):
        if self._activate_animation:
            self._activate_animation.stop(self)
            self._activate_animation = None

    def activate(self):
        self.stop_animation()
        if self.animate_hint:
            activated_hint_target = 1
        else:
            activated_hint_target = 0
        self._activate_animation = Animation(_activated=1, _activated_hint=activated_hint_target, _current_background_color=self.background_color_active, duration=self.activate_time)
        self._activate_animation.start(self)

    def deactivate(self):
        self.stop_animation()
        if self.text and self.animate_hint:
            activated_hint_target = 1
        else:
            activated_hint_target = 0
        self._activate_animation = Animation(_activated=0, _activated_hint=activated_hint_target, _current_background_color=self.background_color, duration=self.deactivate_time)
        self._activate_animation.start(self)


#Test code starts here
from kivy.app import App
class Test(App):
    def build(self):
        return Builder.load_string("""
BoxLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 0
        Rectangle:
            size: self.size
            pos: self.pos
    orientation: 'vertical'
    spacing: 20
    padding: self.width/8, self.height/4
    NormalTextInput:
        underline_pos: 1
        background_color: 1, 1, 1, 0.2
    NormalTextInput:
        size_hint_y: 0.5
        activate_time: 0.25
        deactivate_time: 0.75
        rounded: 0
        background_border_color: 0, 0, 0, 0
        underline_pos: 0
        foreground_color: 1, 1, 1, 1
        background_color: 1, 1, 1, 0.2
        background_color_active: 1, 1, 1, 0
        hint_text_color: 1, 1, 1, 0.75
        animate_hint: False
    NormalTextInput:
        size_hint_y: 1.5
        activate_time: 0.25
        deactivate_time: 0.25
        rounded: 40
        background_border_color: 0, 0, 0, 0
        background_border_width: 3
        background_border_color: 1, 0, 0, 1
        underline_pos: 0.5
        background_color: 1, 1, 1, 1
        background_color_active: 1, 1, 1, 0.8
        hint_text_color: 1, 0, 0, 1
        """)

Test().run()
