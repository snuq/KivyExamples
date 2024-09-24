"""
Example showing Recycleview elements that can animate toggle height based on a click.
"""

from kivy.app import App
from kivy.properties import *
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.clock import Clock
from kivy.uix.togglebutton import ToggleButton
from kivy.lang.builder import Builder
KV = """
<RecycleItem>:

RecycleView:
    data: app.data
    viewclass: 'RecycleItem'
    RecycleBoxLayout:
        spacing: 10
        default_size_hint: 1, None
        default_size: None, 40
        orientation: 'vertical'
        size_hint_y: None
        height: self.minimum_height
"""

class RecycleItem(RecycleDataViewBehavior, ToggleButton):
    small_height = 40
    large_height = 200
    resize_frames = 10
    owner = ObjectProperty()
    index = NumericProperty(0)
    target_height = NumericProperty()

    def on_state(self, widget, state):
        if state != self.owner.data[self.index]['state']:  #prevent extra triggering of set_height
            self.owner.data[self.index]['state'] = state
            if state == 'normal':
                target_height = self.small_height
            else:
                target_height = self.large_height
            self.owner.data[self.index]['target_height'] = target_height
            self.target_height = target_height
            self.set_height()  #start the resize

    def set_height(self, *_):  #Converges height of widget until it is the target height
        if self.height == self.target_height:  #No resize necessary
            return
        height_difference = self.target_height - self.height
        height_change = (self.large_height - self.small_height) / self.resize_frames  #height to change per frame

        if height_difference > height_change:  #needs to grow larger
            height = self.height + height_change
        elif height_difference < -height_change:  #needs to shrink
            height = self.height - height_change
        else:  #size isnt quite correct, need to finish resize
            height = self.target_height
        self.owner.data[self.index]['height'] = height
        self.height = height
        Clock.schedule_once(self.set_height)  #assume the widget is not done resizing, schedule another resize on the next frame

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return_data = super(RecycleItem, self).refresh_view_attrs(rv, index, data)
        self.height = data['height']  #why is this necessary?? height isnt being set by above
        self.set_height()  #Necessary since the widget can change index at any time and needs to resume resizing
        return return_data

class Test(App):
    data = ListProperty()
    def build(self):
        self.data = [{"text": "Button "+str(x), 'owner': self, 'state': 'normal', 'height': 40, 'target_height': 40} for x in range(20)]
        return Builder.load_string(KV)

Test().run()
