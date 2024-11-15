"""Example showing how to exclude a widget in a scrollview from being scrolled.  Useful for putting scrollable widgets inside a larger ScrollView."""
from kivy.uix.scrollview import ScrollView
from kivy.properties import ListProperty


class ScrollWrapper(ScrollView):
    masks = ListProperty()
    def on_touch_down(self, touch):
        for mask in self.masks:
            coords = mask.to_parent(*mask.to_widget(*touch.pos))
            collide = mask.collide_point(*coords)
            if collide:
                touch.apply_transform_2d(mask.to_widget)
                touch.apply_transform_2d(mask.to_parent)
                mask.on_touch_down(touch)
                return True
        super().on_touch_down(touch)


if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder

    class Test(App):
        def build(self):
            return Builder.load_string("""
ScrollWrapper:
    masks: [scroller]
    bar_width: 40
    scroll_type: ['bars', 'content']
    do_scroll_x: False
    GridLayout:
        padding: 40
        cols: 1
        size_hint: 1, None
        height: self.minimum_height
        Button:
            size_hint_y: None
            height: 100
        ScrollView:
            bar_width: 40
            scroll_type: ['bars', 'content']
            id: scroller
            size_hint: 1, None
            height: self.width
            do_scroll_x: True
            do_scroll_y: True
            Label:
                font_size: 500
                size_hint: None, None
                size: 1000, 1000
                text: 'test'
        Button:
            size_hint_y: None
            height: 100
            """)
    Test().run()
