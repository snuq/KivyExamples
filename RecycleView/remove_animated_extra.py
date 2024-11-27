"""Example showing how to remove elements from a RecycleView.  This version includes more advanced animations for element removal."""
from kivy.app import App
from kivy.animation import Animation
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.lang.builder import Builder
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.boxlayout import BoxLayout
KV = """
<RecycleItem>:
    orientation: 'horizontal'
    Label:
        text: root.text
    Button:
        text: 'Remove'
        on_press: root.remove()

RecycleView:
    id: rv
    data: app.data
    viewclass: 'RecycleItem'
    AnimatedRecycleBoxLayout:
        spacing: 10
        default_size: None, dp(80)
        default_size_hint: 1, None
        cols: 1
        size_hint_y: None
        height: self.minimum_height
        remove_callback: app.delete_element
"""


class AnimatedRecycleBoxLayout(RecycleGridLayout):
    remove_callback = ObjectProperty()  #needs to be set to a function that will actually remove this index from the data list and trigger a refresh
    remove_length = NumericProperty(0.25)
    slide_delay = NumericProperty(0.15)
    slide_length = NumericProperty(0.25)
    remove_fly_out = BooleanProperty(False)
    _remove_animation = ObjectProperty(allownone=True)
    _move_animations = ListProperty()
    _original_data = []
    _remove_index = NumericProperty()

    def remove_element(self, index):
        if not self._remove_animation:
            self._original_data = []
            self._remove_index = index
            previous_child = None
            for child in reversed(self.children):
                self._original_data.append([child, child.pos, child.opacity])  #store un-animated data
                if child.index == index:
                    if self.remove_fly_out:
                        target_x = child.x-child.width
                    else:
                        target_x = child.x
                    self._remove_animation = Animation(opacity=0, duration=self.remove_length, x=target_x)+Animation(duration=max(self.slide_length+self.slide_delay-self.remove_length, 0))
                    self._remove_animation.start(child)  #animate a fly-out and opacity fade on element being removed
                    self._remove_animation.bind(on_complete=self.remove_finish)
                elif previous_child and child.index > index:  #child element is lower in list, needs to be animated to show removal
                    anim = Animation(duration=self.slide_delay)+Animation(x=previous_child.x, y=previous_child.y, duration=self.slide_length)
                    anim.start(child)
                    self._move_animations.append(anim)
                previous_child = child

    def remove_finish(self, *_):
        for move_animation in self._move_animations:  #just in case some animations end up going an extra frame, cancel them all
            move_animation.cancel_all(widget=None)
        for data in self._original_data:  #need to restore non-animated values before updating the recycleview or elements will be positioned wrong
            child, pos, opacity = data
            child.pos = pos
            child.opacity = opacity
        self._original_data = []
        self._move_animations = []
        self._remove_animation = None
        self.remove_callback(self._remove_index)


class RecycleItem(RecycleDataViewBehavior, BoxLayout):
    index = NumericProperty()
    text = StringProperty()

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(RecycleItem, self).refresh_view_attrs(rv, index, data)

    def remove(self):
        self.parent.remove_element(self.index)


class Test(App):
    data = ListProperty()

    def delete_element(self, index):
        self.data.pop(index)

    def build(self):
        self.data = [{"text": "Label "+str(x), 'owner': self} for x in range(20)]
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
