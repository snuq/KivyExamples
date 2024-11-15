"""Example showing and expanded ScrollView with more granular control over touch type."""
from functools import partial
from kivy.properties import *
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.stencilview import StencilView
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
_scroll_timeout = _scroll_distance = 0
if Config:
    _scroll_timeout = Config.getint('widgets', 'scroll_timeout')
    _scroll_distance = '{}sp'.format(Config.getint('widgets', 'scroll_distance'))


class TouchScroller(ScrollView):
    """
    Modified version of Kivy's ScrollView widget, removes scrollbars and allows for finer control over touch events.
    allow_middle_mouse: set this to True to enable scrolling with the middle mouse button (blocks middle mouse clicks on child widgets).
    allow_flick: set this to True to enable touch 'flicks' to scroll the view.
    allow_drag: Set this to True to enable click-n-drag scrolling within the scrollview itself.
    allow_wheel: set this to True to enable scrolling via the mouse wheel.
    masks: ListProperty, add any child widgets to this, and they will receive all touches on them, blocking any touch controlls of this widget within their bounds.
    """

    bar_width = NumericProperty(0)
    scroll_distance = NumericProperty(_scroll_distance)
    scroll_timeout = NumericProperty(_scroll_timeout)
    scroll_wheel_distance = NumericProperty('20sp')

    allow_middle_mouse = BooleanProperty(True)
    allow_flick = BooleanProperty(True)
    allow_drag = BooleanProperty(True)
    allow_wheel = BooleanProperty(True)
    masks = ListProperty()

    _touch_moves = 0
    _touch_delay = None
    _start_scroll_x = 0
    _start_scroll_y = 0

    def transformed_touch(self, touch, touch_type='down'):
        #temporarily converts touch to local coords and performs default touch functions
        touch.push()
        touch.apply_transform_2d(self.to_local)
        # touch.apply_transform_2d(self.to_widget)
        if touch_type == 'down':
            ret = StencilView.on_touch_down(self, touch)
        elif touch_type == 'up':
            ret = StencilView.on_touch_up(self, touch)
        else:  #touch_type == 'move'
            ret = StencilView.on_touch_move(self, touch)
        touch.pop()
        return ret

    def scroll_to_point(self, per_x, per_y, animate=True):
        #Scrolls the view to a specific location, can trigger a smooth animation by default.
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
        #convenience function that scrolls the view by a certain amount, can trigger a smooth animation by default
        self.scroll_to_point(self.scroll_x + per_x, self.scroll_y + per_y, animate=animate)

    def on_touch_down(self, touch):
        #Modified touch down from original ScrollView to allow for finer control over touch types
        if self.collide_point(*touch.pos):
            for widget in self.masks:
                #check if touch point is in any of the widgets to exclude
                touch.push()
                touch.apply_transform_2d(self.to_widget)
                if widget.collide_point(*touch.pos):
                    return widget.on_touch_down(touch)
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
                self._touch_delay = Clock.schedule_once(partial(self._on_touch_down_delay, touch),
                                                        (self.scroll_timeout / 1000))
            else:
                return self.transformed_touch(touch)
            return True

    def on_touch_up(self, touch):
        #expanded touch handling to allow for finer control of touch types
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
                self.scroll_to_point(per_x, per_y)
                self._touch_delay = None
                return True
            else:
                self.transformed_touch(touch)
        return self.transformed_touch(touch, 'up')

    def _on_touch_down_delay(self, touch, *largs):
        self._touch_delay = None
        dx, dy = self.touch_moved_distance(touch)
        if self.allow_drag and (dx or dy):
            # user has satisfied the requirements for scrolling
            return True
        else:
            touch.ungrab(self)
            # Need to fix the touch position since it has been translated by this widget's position somehow...
            touch.push()
            touch.apply_transform_2d(self.to_widget)
            touch.apply_transform_2d(self.to_parent)
            return self.transformed_touch(touch)

    def on_touch_move(self, touch):
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
            self.scroll_to_point(per_x, per_y, animate=animate)

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
        #handle mouse wheel or two-finger swipe type scrolling
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


if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.button import Button
    from kivy.lang.builder import Builder
    KV = """
BoxLayout:
    orientation: 'vertical'
    TouchScroller:
        masks: [noScrollButton]
        BoxLayout:
            size_hint: None, None
            size: self.minimum_width, self.minimum_height
            Button:
                id: noScrollButton
                text: 'No Scroll'
                size_hint_x: None
                width: 200
            GridLayout:
                size_hint: None, None
                size: self.minimum_width, self.minimum_height
                id: gridlayout
                cols: 10

    """
    class Test(App):
        def build(self):
            root = Builder.load_string(KV)
            gridlayout = root.ids.gridlayout
            for x in range(50):
                button = Button(size_hint=(None, None), size=(120, 220), text=str(x))
                gridlayout.add_widget(button)
            return root
    Test().run()