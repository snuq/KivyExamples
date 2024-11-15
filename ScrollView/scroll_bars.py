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
        #Placeholder for subclassed jump-to function
        pass

    def on_touch_down(self, touch):
        if not self.disabled and self.collide_point(*touch.pos):
            self.jump_bar(touch.pos)
            touch.grab(self)
            if 'button' in touch.profile and touch.button.startswith('scroll'):
                btn = touch.button
                scroll_direction = ''
                if btn in ('scrollup', 'scrollright'):
                    scroll_direction = 'up'
                elif btn in ('scrolldown', 'scrollleft'):
                    scroll_direction = 'down'
                return self.wheel_scroll(scroll_direction)
            
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

    def wheel_scroll(self, direction):
        return False


class ScrollBarX(ScrollBar):
    """Horizontal scrollbar widget.  See 'ScrollBar' for more information."""

    scroll = NumericProperty(0.)
    def _get_hbar(self):
        if self.width > 0:
            min_width = self.height / self.width  #mdified to prevent scroller size from being too small
        else:
            min_width = 0
        #following code is copied directly from ScrollView
        vw = self.viewport_size[0]
        w = self.scroller_size[0]
        if vw < w or vw == 0:
            return 0, 1.
        pw = max(min_width, w / float(vw))
        sx = min(1.0, max(0.0, self.scroll))
        px = (1. - pw) * sx
        return (px, pw)
    hbar = AliasProperty(_get_hbar, bind=('scroller_size', 'scroll', 'viewport_size', 'width'), cache=True)

    def in_hbar(self, pos_x):
        #convenience function to make it easy for jump_bar to check if click is valid
        local_x = pos_x - self.x
        local_per = local_x / self.width
        hbar = self.hbar
        hbar_top = hbar[0] + hbar[1]
        hbar_bottom = hbar[0]
        half_hbar_height = hbar[1] / 2
        if local_per > hbar_top:
            return local_per - hbar_top + half_hbar_height
        elif local_per < hbar_bottom:
            return local_per - hbar_bottom - half_hbar_height
        else:  #hbar_top > local_per > hbar_bottom:
            return 0

    def jump_bar(self, pos):
        position = self.in_hbar(pos[0])
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
        if (direction == 'up' and self.scroll >= 1) or (direction == 'down' and self.scroll <= 0):
            return False
        
        if self.viewport_size[0] > self.scroller_size[0]:
            scroll_percent = self.scroll_wheel_distance / self.viewport_size[0]
            if direction == 'up':
                new_scroll = self.scroll - scroll_percent
            else:
                new_scroll = self.scroll + scroll_percent
            self.scroll = min(max(new_scroll, 0), 1)
            return True
        return False


class ScrollBarY(ScrollBar):
    """Vertical scrollbar widget.  See 'ScrollBar' for more information."""

    scroll = NumericProperty(1.)
    def _get_vbar(self):
        if self.height > 0:
            min_height = self.width / self.height  #prevent scroller size from being too small
        else:
            min_height = 0
        #following code is copied directly from ScrollView
        vh = self.viewport_size[1]
        h = self.scroller_size[1]
        if vh < h or vh == 0:
            return 0, 1.
        ph = max(min_height, h / float(vh))
        sy = min(1.0, max(0.0, self.scroll))
        py = (1. - ph) * sy
        return (py, ph)
    vbar = AliasProperty(_get_vbar, bind=('scroller_size', 'scroll', 'viewport_size', 'height'), cache=True)

    def in_vbar(self, pos_y):
        #convenience function to make it easy for jump_bar to check if click is valid
        local_y = pos_y - self.y
        local_per = local_y / self.height
        vbar = self.vbar
        vbar_top = vbar[0] + vbar[1]
        vbar_bottom = vbar[0]
        half_vbar_height = vbar[1] / 2
        if local_per > vbar_top:
            return local_per - vbar_top + half_vbar_height
        elif local_per < vbar_bottom:
            return local_per - vbar_bottom - half_vbar_height
        else:  #vbar_top > local_per > vbar_bottom:
            return 0

    def jump_bar(self, pos):
        position = self.in_vbar(pos[1])
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
        if (direction == 'up' and self.scroll >= 1) or (direction == 'down' and self.scroll <= 0):
            return False
        
        if self.viewport_size[1] > self.scroller_size[1]:
            scroll_percent = self.scroll_wheel_distance / self.viewport_size[1]
            if direction == 'up':
                new_scroll = self.scroll - scroll_percent
            else:
                new_scroll = self.scroll + scroll_percent
            self.scroll = min(max(new_scroll, 0), 1)
            return True
        return False


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
