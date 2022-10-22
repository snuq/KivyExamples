from kivy.app import App
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
KV = """
ScrollView:
    scroll_type: ['bars', 'content']
    bar_width: 30
    scroll_timeout: 150
    do_scroll_x: False
    BoxLayout:
        orientation: 'vertical'
        size_hint_y: None
        height: 1000
        ScrollView:
            scroll_type: ['bars', 'content']
            bar_width: 30
            scroll_timeout: 100
            size_hint_y: None
            height: 300
            do_scroll_y: False
            do_scroll_x: True
            Label:
                font_size: 100
                size_hint_x: None
                width: 1000
                text: 'test1test1test1test1test1test1test1test1'
        ScrollView:
            scroll_type: ['bars', 'content']
            bar_width: 30
            scroll_timeout: 100
            size_hint_y: None
            height: 300
            do_scroll_y: False
            do_scroll_x: True
            Label:
                font_size: 100
                size_hint_x: None
                width: 1000
                text: 'test2test2test2test2test2test2test2test2'
        ScrollView:
            scroll_type: ['bars', 'content']
            bar_width: 30
            scroll_timeout: 100
            size_hint_y: None
            height: 300
            do_scroll_y: False
            do_scroll_x: True
            Label:
                font_size: 100
                size_hint_x: None
                width: 1000
                text: 'test3test3test3test3test3test3test3test3'
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)
Test().run()
