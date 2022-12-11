from functools import partial
from kivy.app import App
from kivy.input.motionevent import MotionEvent
from kivy.properties import NumericProperty, AliasProperty, ObjectProperty, ListProperty, ColorProperty, BooleanProperty
from kivy.lang.builder import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.stencilview import StencilView
from kivy.config import Config
# When we are generating documentation, Config doesn't exist
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
        Rectangle:
            pos: root._handle_x_pos or (0, 0)
            size: root._handle_x_size or (0, 0)
    size_hint_y: None
    orientation: 'horizontal'
    height: 40

<ScrollBarY>:
    _handle_y_pos: self.x, self.y + self.height * self.vbar[0]
    _handle_y_size: self.width, self.height * self.vbar[1]
    canvas:
        Color:
            rgba: self._bar_color if (self.viewport_size[1] > self.scroller_size[1]) else [0, 0, 0, 0]
        Rectangle:
            pos: root._handle_y_pos or (0, 0)
            size: root._handle_y_size or (0, 0)
    size_hint_x: None
    orientation: 'vertical'
    width: 40
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
    scroll_wheel_distance = NumericProperty('20sp')
    bar_color = ColorProperty([.7, .7, .7, .9])
    bar_inactive_color = ColorProperty([.7, .7, .7, .2])
    viewport_size = ListProperty([0, 0])
    scroller_size = ListProperty([0, 0])

    _bar_color = ListProperty([0, 0, 0, 0])
    _bind_inactive_bar_color_ev = None

    def _set_scroller_size(self, instance, value):
        self.scroller_size = value

    def _set_viewport_size(self, instance, value):
        self.viewport_size = value

    def _set_scroll(self, instance, value):
        self.scroll = value

    def _bind_inactive_bar_color(self, *l):
        self.funbind('bar_color', self._change_bar_color)
        self.fbind('bar_inactive_color', self._change_bar_color)
        Animation(_bar_color=self.bar_inactive_color, d=.5, t='out_quart').start(self)

    def _change_bar_color(self, inst, value):
        self._bar_color = value

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.update_bar_color()

    def on_touch_down(self, touch):
        if not self.disabled and self.collide_point(*touch.pos):
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
        pass

    def on_scroller(self, instance, value):
        if value:
            value.bind(size=self._set_scroller_size)
            value.bind(viewport_size=self._set_viewport_size)
            self.scroller_size = value.size
            self.viewport_size = value.viewport_size

    def update_bar_color(self):
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
        vw = self.viewport_size[0]
        w = self.scroller_size[0]
        if vw < w or vw == 0:
            return 0, 1.
        pw = max(0.01, w / float(vw))
        sx = min(1.0, max(0.0, self.scroll))
        px = (1. - pw) * sx
        return (px, pw)
    hbar = AliasProperty(_get_hbar, bind=('scroller_size', 'scroll', 'viewport_size', 'width'), cache=True)

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
        vh = self.viewport_size[1]
        h = self.scroller_size[1]
        if vh < h or vh == 0:
            return 0, 1.
        ph = max(0.01, h / float(vh))
        sy = min(1.0, max(0.0, self.scroll))
        py = (1. - ph) * sy
        return (py, ph)
    vbar = AliasProperty(_get_vbar, bind=('scroller_size', 'scroll', 'viewport_size', 'height'), cache=True)

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


class BasicScroller(StencilView):
    """
    Simplified version of Kivy's ScrollView.  Removes scrollbars and any touch control.
    """

    scroll_x = NumericProperty(0.)
    scroll_y = NumericProperty(1.)
    viewport_size = ListProperty([0, 0])

    _viewport = ObjectProperty(None, allownone=True)

    def _set_viewport_size(self, instance, value):
        self.viewport_size = value

    def on__viewport(self, instance, value):
        if value:
            value.bind(size=self._set_viewport_size)
            self.viewport_size = value.size

    def __init__(self, **kwargs):
        self._trigger_update_from_scroll = Clock.create_trigger(
            self.update_from_scroll, -1)
        # create a specific canvas for the viewport
        from kivy.graphics import PushMatrix, Translate, PopMatrix, Canvas
        self.canvas_viewport = Canvas()
        self.canvas = Canvas()
        with self.canvas_viewport.before:
            PushMatrix()
            self.g_translate = Translate(0, 0)
        with self.canvas_viewport.after:
            PopMatrix()

        super().__init__(**kwargs)

        # now add the viewport canvas to our canvas
        self.canvas.add(self.canvas_viewport)

        trigger_update_from_scroll = self._trigger_update_from_scroll
        fbind = self.fbind
        fbind('scroll_x', trigger_update_from_scroll)
        fbind('scroll_y', trigger_update_from_scroll)
        fbind('pos', trigger_update_from_scroll)
        fbind('size', trigger_update_from_scroll)

        trigger_update_from_scroll()

    def transformed_touch(self, touch, touch_type='down'):
        touch.push()
        touch.apply_transform_2d(self.to_local)
        #touch.apply_transform_2d(self.to_widget)
        if touch_type == 'down':
            ret = super().on_touch_down(touch)
        elif touch_type == 'up':
            ret = super().on_touch_up(touch)
        elif touch_type == 'move':
            ret = super().on_touch_move(touch)
        touch.pop()
        return ret

    def on_touch_down(self, touch):
        return self.do_touch_down(touch)
        
    def on_touch_move(self, touch):
        return self.do_touch_move(touch)

    def on_touch_up(self, touch):
        return self.do_touch_up(touch)

    def do_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            return self.transformed_touch(touch, touch_type='down')

    def do_touch_move(self, touch):
        return self.transformed_touch(touch, touch_type='move')

    def do_touch_up(self, touch):
        return self.transformed_touch(touch, touch_type='up')

    def to_local(self, x, y, **k):
        tx, ty = self.g_translate.xy
        return x - tx, y - ty

    def to_parent(self, x, y, **k):
        tx, ty = self.g_translate.xy
        return x + tx, y + ty

    def _apply_transform(self, m, pos=None):
        tx, ty = self.g_translate.xy
        m.translate(tx, ty, 0)
        return super()._apply_transform(m, (0, 0))

    def scroll_to_widget(self, widget, padding=10, animate=True):
        '''Scrolls the viewport to ensure that the given widget is visible,
        optionally with padding and animation. If animate is True (the
        default), then the default animation parameters will be used.
        Otherwise, it should be a dict containing arguments to pass to
        :class:`~kivy.animation.Animation` constructor.
        .. versionadded:: 1.9.1
        '''
        if not self.parent:
            return

        # if _viewport is layout and has pending operation, reschedule
        if hasattr(self._viewport, 'do_layout'):
            if self._viewport._trigger_layout.is_triggered:
                Clock.schedule_once(
                     lambda *dt: self.scroll_to_widget(widget, padding, animate))
                return

        if isinstance(padding, (int, float)):
            padding = (padding, padding)

        pos = self.parent.to_widget(*widget.to_window(*widget.pos))
        cor = self.parent.to_widget(*widget.to_window(widget.right, widget.top))

        dx = dy = 0

        if pos[1] < self.y:
            dy = self.y - pos[1] + dp(padding[1])
        elif cor[1] > self.top:
            dy = self.top - cor[1] - dp(padding[1])

        if pos[0] < self.x:
            dx = self.x - pos[0] + dp(padding[0])
        elif cor[0] > self.right:
            dx = self.right - cor[0] - dp(padding[0])

        dsx, dsy = self.convert_distance_to_scroll(dx, dy)
        sxp = min(1, max(0, self.scroll_x - dsx))
        syp = min(1, max(0, self.scroll_y - dsy))

        if animate:
            if animate is True:
                animate = {'d': 0.2, 't': 'out_quad'}
            Animation.stop_all(self, 'scroll_x', 'scroll_y')
            Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp

    def scroll_to(self, per_x, per_y, animate=True):
        sxp = min(1, max(0, per_x))
        syp = min(1, max(0, per_y))
        Animation.stop_all(self, 'scroll_x', 'scroll_y')
        if animate:
            if animate is True:
                animate = {'d': 0.2, 't': 'out_quad'}
            Animation(scroll_x=sxp, scroll_y=syp, **animate).start(self)
        else:
            self.scroll_x = sxp
            self.scroll_y = syp

    def scroll_by(self, per_x, per_y, animate=True):
        self.scroll_to(self.scroll_x + per_x, self.scroll_y + per_y, animate=animate)

    def convert_distance_to_scroll(self, dx, dy):
        '''Convert a distance in pixels to a scroll distance, depending on the
        content size and the scrollview size.
        The result will be a tuple of scroll distance that can be added to
        :data:`scroll_x` and :data:`scroll_y`
        '''
        if not self._viewport:
            return 0, 0
        vp = self._viewport
        if vp.width > self.width:
            sw = vp.width - self.width
            sx = dx / float(sw)
        else:
            sx = 0
        if vp.height > self.height:
            sh = vp.height - self.height
            sy = dy / float(sh)
        else:
            sy = 1
        return sx, sy

    def update_from_scroll(self, *largs):
        '''Force the reposition of the content, according to current value of
        :attr:`scroll_x` and :attr:`scroll_y`.
        This method is automatically called when one of the :attr:`scroll_x`,
        :attr:`scroll_y`, :attr:`pos` or :attr:`size` properties change, or
        if the size of the content changes.
        '''
        if not self._viewport:
            self.g_translate.xy = self.pos
            return
        vp = self._viewport

        # update from size_hint
        if vp.size_hint_x is not None:
            w = vp.size_hint_x * self.width
            if vp.size_hint_min_x is not None:
                w = max(w, vp.size_hint_min_x)
            if vp.size_hint_max_x is not None:
                w = min(w, vp.size_hint_max_x)
            vp.width = w

        if vp.size_hint_y is not None:
            h = vp.size_hint_y * self.height
            if vp.size_hint_min_y is not None:
                h = max(h, vp.size_hint_min_y)
            if vp.size_hint_max_y is not None:
                h = min(h, vp.size_hint_max_y)
            vp.height = h

        if vp.width > self.width:
            sw = vp.width - self.width
            x = self.x - self.scroll_x * sw
        else:
            x = self.x

        if vp.height > self.height:
            sh = vp.height - self.height
            y = self.y - self.scroll_y * sh
        else:
            y = self.top - vp.height

        # from 1.8.0, we now use a matrix by default, instead of moving the
        # widget position behind. We set it here, but it will be a no-op most
        # of the time.
        vp.pos = 0, 0
        self.g_translate.xy = x, y

    def add_widget(self, widget, *args, **kwargs):
        if self._viewport:
            raise Exception('ScrollView accept only one widget')
        canvas = self.canvas
        self.canvas = self.canvas_viewport
        super().add_widget(widget, *args, **kwargs)
        self.canvas = canvas
        self._viewport = widget
        widget.bind(size=self._trigger_update_from_scroll, size_hint_min=self._trigger_update_from_scroll)
        self._trigger_update_from_scroll()

    def remove_widget(self, widget, *args, **kwargs):
        canvas = self.canvas
        self.canvas = self.canvas_viewport
        super().remove_widget(widget, *args, **kwargs)
        self.canvas = canvas
        if widget is self._viewport:
            self._viewport = None


class TouchScroller(BasicScroller):
    """
    Modified version of Kivy's ScrollView widget, allows for finer control over touch events.
    allow_middle_mouse: set this to True to enable scrolling with the middle mouse button (blocks middle mouse clicks on child widgets).
    allow_flick: set this to True to enable touch 'flicks' to scroll the view.
    allow_drag: Set this to True to enable click-n-drag scrolling within the scrollview itself.
    allow_wheel: set this to True to enable scrolling via the mouse wheel.
    exclude_widgets: ListProperty, add any child widgets to this, and they will receive all touches on them, blocking any touch controlls of this widget within their bounds.
    """

    scroll_distance = NumericProperty(_scroll_distance)
    scroll_timeout = NumericProperty(_scroll_timeout)
    scroll_wheel_distance = NumericProperty('20sp')

    allow_middle_mouse = BooleanProperty(True)
    allow_flick = BooleanProperty(True)
    allow_drag = BooleanProperty(True)
    allow_wheel = BooleanProperty(True)
    exclude_widgets = ListProperty()

    _touch_moves = 0
    _touch_delay = None
    _start_scroll_x = 0
    _start_scroll_y = 0

    def do_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            for widget in self.exclude_widgets:
                touch.push()
                #touch.apply_transform_2d(self.to_local)
                touch.apply_transform_2d(self.to_widget)
                if widget.collide_point(*touch.pos):
                    return super().on_touch_down(touch)
                touch.pop()

            #delay touch to check if scroll is initiated
            if 'button' in touch.profile and touch.button.startswith('scroll'):
                if self.allow_wheel:
                    touch.grab(self)
                    btn = touch.button
                    return self.wheel_scroll(btn)
                else:
                    return self.transformed_touch(touch)

            touch.grab(self)
            self._touch_delay = None
            self._touch_moves = 0

            self._start_scroll_x = self.scroll_x
            self._start_scroll_y = self.scroll_y
            if self.allow_middle_mouse and 'button' in touch.profile and touch.button == 'middle':
                return True
            if self.allow_drag or self.allow_flick:
                self._touch_delay = Clock.schedule_once(partial(self._on_touch_down_delay, touch), (self.scroll_timeout / 1000))
            else:
                return self.transformed_touch(touch)
            return True

    def do_touch_up(self, touch):
        if touch.grab_current == self:
            touch.ungrab(self)
        if self.allow_middle_mouse and 'button' in touch.profile and touch.button == 'middle':
            return True
        if self._touch_delay:
            self._touch_delay.cancel()
            self._touch_delay = None
            dx, dy = self.touch_moved_distance(touch)
            if self.allow_flick and (dx or dy):
                per_x = self.scroll_x - ((dx * 2) / self.width)
                per_y = self.scroll_y - ((dy * 2) / self.height)
                self.scroll_to(per_x, per_y)
                self._touch_delay = None
                return True
            else:
                self.transformed_touch(touch)
        return self.transformed_touch(touch, 'up')

    def _on_touch_down_delay(self, touch, *largs):
        self._touch_delay = None
        dx, dy = self.touch_moved_distance(touch)
        if self.allow_drag and (dx or dy):
            #user has satisfied the requirements for scrolling
            return True
        else:
            touch.ungrab(self)
            #Need to fix the touch position since it has been translated by this widget's position somehow...
            touch.push()
            touch.apply_transform_2d(self.to_widget)
            touch.apply_transform_2d(self.to_parent)
            return self.transformed_touch(touch)

    def do_touch_move(self, touch):
        middle_button = 'button' in touch.profile and touch.button == 'middle'
        if not self.allow_drag and not middle_button:
            return
        if self._touch_delay:
            always = False
        else:
            always = True
        if touch.grab_current == self:
            self._touch_moves += 1
            if self._touch_moves == 1 and not middle_button:
                animate = True
            else:
                animate = False
            dx, dy = self.touch_moved_distance(touch, always=always)
            if self.viewport_size[0] != self.width:
                per_x = self._start_scroll_x + (dx / (self.width - self.viewport_size[0]))
            else:
                per_x = self._start_scroll_x
            if self.viewport_size[1] != self.height:
                per_y = self._start_scroll_y + (dy / (self.height - self.viewport_size[1]))
            else:
                per_y = self._start_scroll_y
            self.scroll_to(per_x, per_y, animate=animate)

    def touch_moved_distance(self, touch, always=False):
        #determines if the touch has moved the required distance to allow for scrolling
        can_move_x = self.viewport_size[0] > self.width
        can_move_y = self.viewport_size[1] > self.height
        dx = touch.pos[0] - touch.opos[0]
        dy = touch.pos[1] - touch.opos[1]
        if can_move_x and (always or abs(dx) >= self.scroll_distance):
            pass
        else:
            dx = 0
        if can_move_y and (always or abs(dy) >= self.scroll_distance):
            pass
        else:
            dy = 0
        
        return dx, dy

    def wheel_scroll(self, btn):
        can_move_x = self.viewport_size[0] > self.width
        can_move_y = self.viewport_size[1] > self.height
        scroll_percent_x = self.scroll_wheel_distance / self.viewport_size[0]
        scroll_percent_y = self.scroll_wheel_distance / self.viewport_size[1]

        if can_move_x and can_move_y:
            if btn == 'scrollup':
                self.scroll_by(0, scroll_percent_y, animate=False)
            elif btn == 'scrolldown':
                self.scroll_by(0, 0 - scroll_percent_y, animate=False)
            elif btn == 'scrollleft':
                self.scroll_by(scroll_percent_x, 0, animate=False)
            elif btn == 'scrollright':
                self.scroll_by(0 - scroll_percent_x, 0, animate=False)
        elif can_move_x:
            if btn in ['scrolldown', 'scrollleft']:
                self.scroll_by(scroll_percent_x, 0, animate=False)
            elif btn in ['scrollup', 'scrollright']:
                self.scroll_by(0 - scroll_percent_x, 0, animate=False)
        elif can_move_y:
            if btn in ['scrolldown', 'scrollright']:
                self.scroll_by(0, scroll_percent_y, animate=False)
            elif btn in ['scrollup', 'scrollleft']:
                self.scroll_by(0, 0 - scroll_percent_y, animate=False)
        return True
