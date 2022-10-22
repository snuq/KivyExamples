from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, ListProperty, BooleanProperty, AliasProperty, NumericProperty, DictProperty
from kivy.lang.builder import Builder

Builder.load_string("""
<SplitterArea>:
    canvas.before:
        Color:
            rgba: [1, 1, 1, .3]
        Rectangle:
            size: self.size
            pos: self.pos
    canvas.after:
        Color:
            rgba: 1, 1, 1, 1 if self.splitter_show_x else 0
        Rectangle:
            pos: self.pos[0] + (self.splitter_percent * self.width) - 5, self.pos[1]
            size: (10, self.height)
        Color:
            rgba: 1, 1, 1, 1 if self.splitter_show_y else 0
        Rectangle:
            pos: self.pos[0], self.pos[1] + (self.splitter_percent * self.height) - 5
            size: (self.width, 10)
    orientation: 'vertical'
    BoxLayout:
        size_hint_y: None
        height: 60
        orientation: 'horizontal'
        Button:
            text: 'Type'
            size_hint_x: None
            width: self.height
            on_release: root.select_area()
        Widget:
        Button:
            text: 'Remove'
            size_hint_x: None
            width: self.height
            on_press: root.remove_area()
        DragDirection:
            size_hint_x: None
            width: self.height
            owner: root
    BoxLayout:
        id: mainArea
        Label:
            text: str(root.ident)

<SplitterDivider>:
    size: 10, 10

<AreaHolderDouble>:
    BoxLayout:
        id: area_1
        size_hint_x: 1 if root.orientation == 'vertical' else (1 + root.split_percent)
        size_hint_y: (1 - root.split_percent) if root.orientation == 'vertical' else 1
    SplitterDivider:
        id: splitter
        size_hint_x: 1 if root.orientation == 'vertical' else None
        size_hint_y: None if root.orientation == 'vertical' else 1
    BoxLayout:
        id: area_2
        size_hint_x: 1 if root.orientation == 'vertical' else (1 - root.split_percent)
        size_hint_y: (1 + root.split_percent) if root.orientation == 'vertical' else 1

<AreaHolderSingle>:
    BoxLayout:
        id: area_1
""")

class SplitterDivider(BoxLayout):
    def touch_percent(self, pos):
        x = (pos[0] - self.parent.pos[0]) / self.parent.width
        y = (pos[1] - self.parent.pos[1]) / self.parent.height
        return [x, y]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            percent = self.touch_percent(touch.pos)
            if self.parent.orientation == 'vertical':
                split_percent = (percent[1] - .5) * 2
            else:
                split_percent = (percent[0] - .5) * 2
            self.parent.split_percent = split_percent

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)

class DragDirection(BoxLayout):
    owner = ObjectProperty()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            dx = abs(touch.pos[0] - touch.opos[0])
            dy = abs(touch.pos[1] - touch.opos[1])
            percent = self.touch_percent(touch.pos)
            if dx > dy:
                self.owner.splitter_show_x = True
                self.owner.splitter_show_y = False
                self.owner.splitter_percent = percent[0]
            else:
                self.owner.splitter_show_y = True
                self.owner.splitter_show_x = False
                self.owner.splitter_percent = percent[1]

    def touch_percent(self, pos):
        x = (pos[0] - self.owner.pos[0]) / self.owner.width
        y = (pos[1] - self.owner.pos[1]) / self.owner.height
        return [x, y]

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            self.owner.splitter_show_x = False
            self.owner.splitter_show_y = False
            touch.ungrab(self)
            dx = abs(touch.pos[0] - touch.opos[0])
            dy = abs(touch.pos[1] - touch.opos[1])
            percent = self.touch_percent(touch.pos)
            if dx > dy:
                self.owner.split_area(split_direction='horizontal', percent=percent[0])
            else:
                self.owner.split_area(percent=percent[1])

class AreaHolder(BoxLayout):
    split_percent = NumericProperty(0)
    area_1 = ObjectProperty(allownone=True)
    area_2 = ObjectProperty(allownone=True)
    
    def which_area(self, widget):
        if self.area_1 == widget:
            return 'area_1'
        elif self.area_2 == widget:
            return 'area_2'
        return None

    def split_area(self, area_name, split_direction='vertical', percent=.5):
        area_holder = self.ids[area_name]
        area_to_split = getattr(self, area_name)
        area_holder.clear_widgets()
        other_area = SplitterArea(root=area_to_split.root, area_type=area_to_split.area_type, ident=area_to_split.ident+1)
        new_holder = AreaHolderDouble(orientation=split_direction)
        new_holder.set_area('area_1', area_to_split)
        new_holder.set_area('area_2', other_area)
        new_holder.split_percent = (percent - .5) * 2
        setattr(self, area_name, new_holder)
        area_holder.add_widget(new_holder)

    def remove_area(self, area_name):
        if area_name == 'area_1':
            other_area = self.area_2
        else:
            other_area = self.area_1
        other_area.parent.remove_widget(other_area)
        area_name = self.parent.parent.which_area(self)
        self.parent.parent.set_area(area_name, other_area)

    def set_area(self, area_name, area):
        if area is None:
            self.remove_area(area_name)
        else:
            setattr(self, area_name, area)
            area_holder = self.ids[area_name]
            area_holder.clear_widgets()
            area_holder.add_widget(area)

class AreaHolderDouble(AreaHolder):
    pass

class AreaHolderSingle(AreaHolder):
    def remove_area(self, area_name):
        pass

class SplitterArea(BoxLayout):
    area_type = StringProperty()
    area_index = StringProperty('')
    ident = NumericProperty(0)
    root = ObjectProperty()
    splitter_percent = NumericProperty(0)
    splitter_show_x = BooleanProperty(False)
    splitter_show_y = BooleanProperty(False)

    def select_area(self):
        pass

    def split_area(self, split_direction='vertical', percent=.5):
        area_name = self.parent.parent.which_area(self)
        self.parent.parent.split_area(area_name, split_direction=split_direction, percent=percent)

    def remove_area(self):
        area_name = self.parent.parent.which_area(self)
        self.parent.parent.set_area(area_name, None)

class Test(App):
    def build(self):
        screen = AreaHolderSingle()
        area = SplitterArea()
        screen.set_area('area_1', area)
        return screen

if __name__ == '__main__':
    Test().run()
