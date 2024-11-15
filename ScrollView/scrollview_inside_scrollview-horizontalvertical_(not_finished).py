from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import ListProperty
from kivy.uix.behaviors import FocusBehavior

KV = """
<ScrollView>:
    bar_width: 40
    scroll_type: ['bars', 'content']

<Button>:
    text: 'test'
    size_hint_y: None
    height: 100

CustomScroll:
    do_scroll_x: False
    do_scroll_y: True
    GridLayout:
        padding: 40
        cols: 1
        size_hint: 1, None
        height: self.minimum_height
        Button:
        CustomScroll:
            size_hint: 1, None
            height: 300
            do_scroll_x: True
            do_scroll_y: False
            Label:
                font_size: 200
                size_hint: None, None
                size: 1000, 300
                text: 'test'
        CustomScroll:
            size_hint: 1, None
            height: 300
            do_scroll_x: True
            do_scroll_y: False
            Label:
                font_size: 200
                size_hint: None, None
                size: 1000, 300
                text: 'test'
        Button:
"""

class CustomScroll(ScrollView):
    def on_scroll_move(self, touch):
        if self._get_uid('svavoid') in touch.ud:
            return False

        touch.push()
        touch.apply_transform_2d(self.to_local)
        #if self.dispatch_children('on_scroll_move', touch):
        #    touch.pop()
        #    return True
        touch.pop()

        rv = True

        # By default this touch can be used to defocus currently focused
        # widget, like any touch outside of ScrollView.
        touch.ud['sv.can_defocus'] = True

        uid = self._get_uid()
        if uid not in touch.ud:
            self._touch = False
            return self.on_scroll_start(touch, False)
        ud = touch.ud[uid]

        # check if the minimum distance has been travelled
        if ud['mode'] == 'unknown':
            if not (self.do_scroll_x or self.do_scroll_y):
                # touch is in parent, but _change expects window coords
                touch.push()
                touch.apply_transform_2d(self.to_local)
                touch.apply_transform_2d(self.to_window)
                self._change_touch_mode()
                touch.pop()
                return
            ud['dx'] += abs(touch.dx)
            ud['dy'] += abs(touch.dy)
            if ((ud['dx'] > self.scroll_distance and self.do_scroll_x) or
                    (ud['dy'] > self.scroll_distance and self.do_scroll_y)):
                ud['mode'] = 'scroll'

        if ud['mode'] == 'scroll':
            if not touch.ud['sv.handled']['x'] and self.do_scroll_x \
                    and self.effect_x:
                width = self.width
                if touch.ud.get('in_bar_x', False):
                    dx = touch.dx / float(width - width * self.hbar[1])
                    self.scroll_x = min(max(self.scroll_x + dx, 0.), 1.)
                    self._trigger_update_from_scroll()
                else:
                    if self.scroll_type != ['bars']:
                        self.effect_x.update(touch.x)
                if self.scroll_x < 0 or self.scroll_x > 1:
                    rv = False
                else:
                    touch.ud['sv.handled']['x'] = True
                # Touch resulted in scroll should not defocus focused widget
                touch.ud['sv.can_defocus'] = False
            if not touch.ud['sv.handled']['y'] and self.do_scroll_y \
                    and self.effect_y:
                height = self.height
                if touch.ud.get('in_bar_y', False):
                    dy = touch.dy / float(height - height * self.vbar[1])
                    self.scroll_y = min(max(self.scroll_y + dy, 0.), 1.)
                    self._trigger_update_from_scroll()
                else:
                    if self.scroll_type != ['bars']:
                        self.effect_y.update(touch.y)
                if self.scroll_y < 0 or self.scroll_y > 1:
                    rv = False
                else:
                    touch.ud['sv.handled']['y'] = True
                # Touch resulted in scroll should not defocus focused widget
                touch.ud['sv.can_defocus'] = False
            ud['dt'] = touch.time_update - ud['time']
            ud['time'] = touch.time_update
            ud['user_stopped'] = True
        return rv

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return False
        for child in self.children:
            child.on_touch_down(touch)
        if self.dispatch('on_scroll_start', touch, check_children=False):
            self._touch = touch
            #touch.grab(self)
            return True

    def on_touch_move(self, touch):
        for child in self.children:
            child.on_touch_move(touch)
        if self._touch is not touch:
            # don't pass on touch to children if outside the sv
            if self.collide_point(*touch.pos):
                # touch is in parent
                touch.push()
                touch.apply_transform_2d(self.to_local)
                super(CustomScroll, self).on_touch_move(touch)
                touch.pop()
            return self._get_uid() in touch.ud
        #if touch.grab_current is not self:
        #    return True

        if not any(isinstance(key, str) and key.startswith('sv.')
                   for key in touch.ud):
            # don't pass on touch to children if outside the sv
            if self.collide_point(*touch.pos):
                # touch is in window coordinates
                touch.push()
                touch.apply_transform_2d(self.to_local)
                res = super(CustomScroll, self).on_touch_move(touch)
                touch.pop()
                return res
            return False

        touch.ud['sv.handled'] = {'x': False, 'y': False}
        if self.dispatch('on_scroll_move', touch):
            return

    def on_touch_up(self, touch):
        for child in self.children:
            child.on_touch_up(touch)
        uid = self._get_uid('svavoid')
        if self._touch is not touch and uid not in touch.ud:
            # don't pass on touch to children if outside the sv
            if self.collide_point(*touch.pos):
                # touch is in parents
                touch.push()
                touch.apply_transform_2d(self.to_local)
                if super(CustomScroll, self).on_touch_up(touch):
                    touch.pop()
                    return True
                touch.pop()
            return False

        if self.dispatch('on_scroll_stop', touch, check_children=False):
            #touch.ungrab(self)
            if not touch.ud.get('sv.can_defocus', True):
                # Focused widget should stay focused
                FocusBehavior.ignored_touch.append(touch)
            return True

class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
