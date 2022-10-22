from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.properties import ListProperty

Builder.load_string("""
<ScrollView>:
    bar_width: 40
    scroll_type: ['bars', 'content']

<Button>:
    text: 'test'
    size_hint_y: None
    height: 100

<ScrollWrapper>:
    masks: [scroller]
    do_scroll_x: False
    GridLayout:
        padding: 40
        cols: 1
        size_hint: 1, None
        height: self.minimum_height
        Button:
        ScrollView:
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
""")

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
        super(ScrollWrapper, self).on_touch_down(touch)

class Test(App):
    def build(self):
        return ScrollWrapper()

if __name__ == '__main__':
    Test().run()
