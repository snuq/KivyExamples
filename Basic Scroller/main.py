"""
An example that shows how to use the custom 'basicscroller' widgets that implement scrollbars that can be used with a kivy scrollview.
"""
from kivy.app import App
from basicscroller import *
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,disable_multitouch')

KV = """
BoxLayout:
    orientation: 'vertical'
    TouchScroller:
        exclude_widgets: [innerScroller, innerScrollerBar]
        allow_drag: True
        id: outerScroller
        BoxLayout:
            size_hint_x: None
            width: self.minimum_width
            BoxLayout:
                size_hint: None, 1
                width: 400
                TouchScroller:
                    allow_drag: True
                    allow_flick: True
                    id: innerScroller
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        height: self.minimum_height
                        Button:
                            text: 'First'
                            size_hint: 1, None
                            height: 200
                            on_press: print('clicked 1')
                        Button:
                            text: 'Second'
                            size_hint: 1, None
                            height: 200
                            on_press: print('clicked 2')
                        Button:
                            text: 'Third'
                            size_hint: 1, None
                            height: 200
                            on_press: print('clicked 3')
                        Button:
                            text: 'Fourth'
                            size_hint: 1, None
                            height: 200
                            on_press: print('clicked 4')
                        Button:
                            text: 'Fifth'
                            size_hint: 1, None
                            height: 200
                            on_press: print('clicked 5')
                ScrollBarY:
                    id: innerScrollerBar
                    scroller: innerScroller
            Button:
                size_hint_x: None
                width: 600
    ScrollBarX:
        scroller: outerScroller
    Button:
        size_hint_y: None
        height: 50
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)
Test().run()
