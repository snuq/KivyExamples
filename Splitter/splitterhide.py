"""
Example that demonstrates how to use a Splitter widget to show a resizeable and toggle-able area.
"""
from kivy.app import App
from kivy.properties import *
from kivy.uix.splitter import Splitter
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'vertical'
        Button:
            text: 'Top Area'
        Button:
            size_hint_y: None
            height: 40
            text: 'Show Bottom' if bottom_area.height == 0 else 'Hide Bottom'
            on_release: bottom_area.toggle_area()
    SplitterToggle:
        id: bottom_area
        size_hint_y: None
        strip_size: 20
        min_size: self.strip_size
        max_size: self.parent.height / 2
        sizable_from: 'top'
        Button:
            text: 'Bottom Area'
"""


class SplitterToggle(Splitter):
    strip_size_backup = 20  #Used as a temporary storage for the strip size when area is hidden
    height_backup = 200  #Used as a temporary storage for height when the area is hidden
    hide_height = NumericProperty(100)

    def on_height(self, *_):
        if 0 < self.height < self.hide_height:
            self.opacity = 0.5
        elif self.height == 0:
            self.opacity = 0
        else:
            self.opacity = 1

    def on_release(self, *_):
        #This is used to hide the area by dragging it smaller than a specific size
        if 0 < self.height < self.hide_height:
            self.hide_area()

    def toggle_area(self):
        if self.height > 0:
            self.hide_area()
        else:
            self.show_area()

    def hide_area(self):
        self.strip_size_backup = self.strip_size
        self.height_backup = self.height
        self.strip_size = 0
        self.height = 0
        self.disabled = True

    def show_area(self):
        if self.height_backup < self.hide_height:
            self.height_backup = self.hide_height
        self.strip_size = self.strip_size_backup
        self.height = self.height_backup
        self.disabled = False


class Test(App):
    def build(self):
        return Builder.load_string(KV)


Test().run()
