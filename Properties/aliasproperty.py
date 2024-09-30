"""Simple example showing how to use AliasProperty to generate complex expressions for use in kvlang"""
from kivy.properties import *
from kivy.uix.widget import Widget
from kivy.lang.builder import Builder
Builder.load_string("""
<MyWidget>:
    canvas:
        Color:
            rgba: 1, 0, 0, 1
        Line:
            width: 2
            rounded_rectangle: self.rectangle_coords
""")

class MyWidget(Widget):
    def _get_rect_coords(self, *_):  #Called whenever rectangle_coords is needed, just needs return whatever value it should be set too
        return [self.x, self.y, self.width, self.height, self.width/4]
    rectangle_coords = AliasProperty(_get_rect_coords, bind=['width', 'height', 'x', 'y'])  #Only need to worry about the getter function in this situation, setter is never called

from kivy import app; app.runTouchApp(MyWidget())