"""Example showing how to make custom scrollbars that will scroll a ScrollView based widget"""
from kivy.properties import *
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
_scroll_timeout = _scroll_distance = 0
if Config:
    _scroll_timeout = Config.getint('widgets', 'scroll_timeout')
    _scroll_distance = '{}sp'.format(Config.getint('widgets', 'scroll_distance'))

Builder.load_string("""
<ScrollBarX>:
    _handle_x_pos: self.x + self.width * self.hbar[0], self.y
    _handle_x_size: self.width * self.hbar[1], self.height
    canvas:
        Color:
            rgba: self._bar_color if (self.viewport_size[0] > self.scroller_size[0]) else [0, 0, 0, 0]
        RoundedRectangle:
            radius: [self.rounding]
            pos: root._handle_x_pos or (0, 0)
            size: root._handle_x_size or (0, 0)
    is_active: not self.viewport_size[0] <= self.scroller_size[0]
    size_hint_y: None
    orientation: 'horizontal'
    height: 40 if self.is_active else 0

<ScrollBarY>:
    _handle_y_pos: self.x, self.y + self.height * self.vbar[0]
    _handle_y_size: self.width, self.height * self.vbar[1]
    canvas:
        Color:
            rgba: self._bar_color if (self.viewport_size[1] > self.scroller_size[1]) else [0, 0, 0, 0]
        RoundedRectangle:
            radius: [self.rounding]
            pos: root._handle_y_pos or (0, 0)
            size: root._handle_y_size or (0, 0)
    is_active: not self.viewport_size[1] <= self.scroller_size[1]
    size_hint_x: None
    orientation: 'vertical'
    width: 40 if self.is_active else 0
""")

class ScrollBar(BoxLayout):
    """
    Base class for a basic scrollbar widget that can control a set ScrollView.
    This class itself should not be used, use ScrollBarX or ScrollBarY for horizontal or vertical scrolling.
    The 'scroller' variable must be set to the ScrollView widget that should be controlled.
    'bar_color' and 'bar_inactive_color' can be set to a rgba color.
    """

    scroll = NumericProperty()
    scroller = ObjectProperty(allownone=True)
    scroller_size = ListProperty([0, 0])
    rounding = NumericProperty(0)
    is_active = BooleanProperty(True)

    #borrow some functions and variables from ScrollView
    scroll_wheel_distance = NumericProperty('20sp')
    bar_color = ColorProperty([.7, .7, .7, .9])
    bar_inactive_color = ColorProperty([.7, .7, .7, .2])
    viewport_size = ListProperty([0, 0])
    _bar_color = ListProperty([0, 0, 0, 0])
    _bind_inactive_bar_color_ev = None
    _set_viewport_size = ScrollView._set_viewport_size
    _bind_inactive_bar_color = ScrollView._bind_inactive_bar_color
    _change_bar_color = ScrollView._change_bar_color

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_bar_color()

    def _set_scroller_size(self, instance, value):
        self.scroller_size = value

    def _set_scroll(self, instance, value):
        self.scroll = value

    def jump_bar(self, pos):
        #Placeholder for subclassed jump-to function, can scroll to a different location in the scrollbar without dragging
        pass

    def on_touch_down(self, touch):
        if not self.disabled and self.collide_point(*touch.pos):
            if 'button' in touch.profile and touch.button.startswith('scroll'):
                btn = touch.button
                return self.wheel_scroll(btn)

            self.jump_bar(touch.pos)
            touch.grab(self)
            self.do_touch_scroll(touch)
            return True

    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.do_touch_scroll(touch)

    def do_touch_scroll(self, touch):
        #Touch events should activate scrolling
        #Splitting this into its own function to make it easier to subclass
        pass

    def on_scroller(self, instance, value):
        #The scroller object has been set, create binds and set up local variables
        if value:
            value.bind(size=self._set_scroller_size)
            value.bind(viewport_size=self._set_viewport_size)
            self.scroller_size = value.size
            self.viewport_size = value.viewport_size

    def update_bar_color(self):
        #in original code, this was in update_from_scroll, but that extra code is not needed
        ev = self._bind_inactive_bar_color_ev
        if ev is None:
            ev = self._bind_inactive_bar_color_ev = Clock.create_trigger(
                self._bind_inactive_bar_color, .5)
        self.funbind('bar_inactive_color', self._change_bar_color)
        Animation.stop_all(self, '_bar_color')
        self.fbind('bar_color', self._change_bar_color)
        self._bar_color = self.bar_color
        ev()

    def do_wheel_scroll(self, direction, scroll_axis):
        scroll_up = ['scrollup', 'scrollright']
        scroll_down = ['scrolldown', 'scrollleft']
        if (direction in scroll_down and self.scroll >= 1) or (direction in scroll_up and self.scroll <= 0):
            return False

        if self.viewport_size[scroll_axis] > self.scroller_size[scroll_axis]:
            scroll_percent = self.scroll_wheel_distance / self.viewport_size[scroll_axis]
            if direction in scroll_up:
                new_scroll = self.scroll - scroll_percent
            elif direction in scroll_down:
                new_scroll = self.scroll + scroll_percent
            else:
                return False
            self.scroll = min(max(new_scroll, 0), 1)
            return True
        return False

    def wheel_scroll(self, direction):
        return False

    def _get_bar(self, axis, min_size):
        viewport_size = self.viewport_size[axis]
        scroller_size = self.scroller_size[axis]
        if viewport_size < scroller_size or viewport_size == 0:
            #not large enough to scroll
            return 0, 1.
        bar_length = max(min_size, scroller_size / float(viewport_size))
        scroll = min(1.0, max(0.0, self.scroll))
        bar_pos = (1. - bar_length) * scroll
        return bar_pos, bar_length

    def _get_vbar(self):
        if self.height > 0:
            min_height = self.width / self.height  #prevent scroller size from being too small
        else:
            min_height = 0
        return self._get_bar(1, min_height)
    vbar = AliasProperty(_get_vbar, bind=('scroller_size', 'scroll', 'viewport_size', 'height'), cache=True)

    def _get_hbar(self):
        if self.width > 0:
            min_width = self.height / self.width  #prevent scroller size from being too small
        else:
            min_width = 0
        return self._get_bar(0, min_width)
    hbar = AliasProperty(_get_hbar, bind=('scroller_size', 'scroll', 'viewport_size', 'width'), cache=True)

    def in_bar(self, click_pos, self_pos, self_size, bar):
        local_pos = click_pos - self_pos
        click_per = local_pos / self_size
        bar_top = bar[0] + bar[1]
        bar_bottom = bar[0]
        half_bar_height = bar[1] / 2
        if click_per > bar_top:
            return click_per - bar_top + half_bar_height
        elif click_per < bar_bottom:
            return click_per - bar_bottom - half_bar_height
        else:  #bar_top > click_per > bar_bottom:
            return 0


class ScrollBarX(ScrollBar):
    """Horizontal scrollbar widget.  See 'ScrollBar' for more information."""

    scroll = NumericProperty(0.)

    def jump_bar(self, pos):
        position = self.in_bar(pos[0], self.x, self.width, self.hbar)
        self.scroller.scroll_x += position

    def on_scroller(self, instance, value):
        super().on_scroller(instance, value)
        if value:
            value.bind(scroll_x=self._set_scroll)
            self.scroll = value.scroll_x

    def on_scroll(self, instance, value):
        if self.scroller is not None:
            self.scroller.scroll_x = value

    def do_touch_scroll(self, touch):
        self.update_bar_color()
        scroll_scale = (self.width - self.width * self.hbar[1])
        if scroll_scale == 0:
            return
        scroll_amount = touch.dx / scroll_scale
        self.scroll = min(max(self.scroll + scroll_amount, 0.), 1.)

    def wheel_scroll(self, direction):
        return self.do_wheel_scroll(direction, 0)


class ScrollBarY(ScrollBar):
    """Vertical scrollbar widget.  See 'ScrollBar' for more information."""

    scroll = NumericProperty(1.)

    def jump_bar(self, pos):
        position = self.in_bar(pos[1], self.y, self.height, self.vbar)
        self.scroller.scroll_y += position

    def on_scroller(self, instance, value):
        super().on_scroller(instance, value)
        if value:
            value.bind(scroll_y=self._set_scroll)
            self.scroll = value.scroll_y

    def on_scroll(self, instance, value):
        if self.scroller is not None:
            self.scroller.scroll_y = value
        
    def do_touch_scroll(self, touch):
        self.update_bar_color()
        scroll_scale = (self.height - self.height * self.vbar[1])
        if scroll_scale == 0:
            return
        scroll_amount = touch.dy / scroll_scale
        self.scroll = min(max(self.scroll + scroll_amount, 0.), 1.)

    def wheel_scroll(self, direction):
        return self.do_wheel_scroll(direction, 1)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.config import Config
    Config.set('input', 'mouse', 'mouse,disable_multitouch')

    class Test(App):
        def build(self):
            return Builder.load_string("""
BoxLayout:
    orientation: 'vertical'
    ScrollView:
        scroll_type: ['bars']
        bar_width: 0
        id: outerScroller
        BoxLayout:
            size_hint_x: None
            width: self.minimum_width
            BoxLayout:
                size_hint: None, 1
                width: 600
                ScrollView:
                    scroll_type: ['content']
                    bar_width: 0
                    id: innerScroller
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        Button:
                            text: 'First'
                            size_hint: 1, None
                            height: 1000
                ScrollBarY:
                    id: innerScrollerBar
                    scroller: innerScroller
            Button:
                text: 'Second'
                size_hint_x: None
                width: 600
    ScrollBarX:
        scroller: outerScroller
            """)
    Test().run()
