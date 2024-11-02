"""Automatically generate menus with sub menus from simple lists"""
from kivy.app import App
from kivy.uix.button import Button
from kivy.properties import *
from kivy.factory import Factory
from kivy.uix.dropdown import DropDown
from functools import partial
from kivy.lang.builder import Builder
KV = """
GridLayout:
    cols: 3
    Widget:
    ListMenu:
        menu: app.menu
        text: 'Open Menu'
    Widget:
        size_hint_x: 4
    Widget:
        size_hint_y: 10
"""


class SideCapableDropDown(DropDown):
    #special dropdown subclass that can attach to the side of a widget insted of above/below
    attach_side = BooleanProperty(False)

    def _reposition(self, *largs):
        if not self.attach_side:
            return super()._reposition(*largs)  #use original method

        #modified method to invert vertical position and move to the right
        win = self._win
        if not win:
            return
        widget = self.attach_to
        if not widget or not widget.get_parent_window():
            return
        wx, wy = widget.to_window(*widget.pos)
        wright, wtop = widget.to_window(widget.right, widget.top)

        if self.auto_width:
            self.width = wright - wx

        x = wx + widget.width  #move to the right
        if x + self.width > win.width:
            x = win.width - self.width
        if x < 0:
            x = 0
        self.x = x

        if self.max_height is not None:
            height = min(self.max_height, self.container.minimum_height)
        else:
            height = self.container.minimum_height

        h_bottom = wy - height
        h_top = win.height - (wtop + height)
        if h_bottom > 0:
            self.top = wtop  #invert pinning
            self.height = height
        elif h_top > 0:
            self.y = wy  #invert pinning
            self.height = height
        else:
            if h_top < h_bottom:
                self.top = self.height = wtop  #invert pinning
            else:
                self.y = wy  #invert pinning
                self.height = win.height - wtop


class ListMenu(Button):
    button_viewclass = ObjectProperty('Button')  #Class name internal menu buttons
    dropdown_viewclass = ObjectProperty('SideCapableDropDown')  #Class name for dropdown itself
    spacer_viewclass = ObjectProperty('Widget')  #Class name for menu spacers

    button_height = NumericProperty(-1)  #Default height for internal buttons, if negative, will default to self.height
    spacer_height = NumericProperty(-1)  #Default height for spacers, if negative, will default to self.height / 4
    menu_auto_width = BooleanProperty(True)  #If True, menu will be same width as this button
    menu_width = NumericProperty(100)  #Width of menu if menu_auto_width is False
    menu = ListProperty()  #Stores a list of elements that defines the menu
    #   Each element must be a dictionary, or a 'None'
    #   Any element that is None will generate a spacer at that position
    #   Element dictionaries must have a 'name' attribute, this will be the text of the button.
    #   Optional Attributes:
    #       'function': the function that this button will call when clicked
    #       'args': additional arguments to pass to the function (no arguments are passed by default).  This should be a list of variables
    #       'submenu': another list object, same format as this, will automatically open a sub-menu when this button is clicked
    #       'menu_auto_width': boolean, only relevant for sub-menus: determines if this sub-menu will use auto_width.
    #       'menu_width': numeric, only relevant for sub-menus: the width of this submenu if auto_width is True

    menu_object = ObjectProperty(allownone=True)
    menu_tree = ListProperty()
    is_submenu = BooleanProperty(False)

    def on_release(self, *_):
        self.open()

    def open(self, *_):
        #self.dismiss()

        #get classes
        menu_object_class = getattr(Factory, self.dropdown_viewclass)
        self.menu_object = menu_object_class(auto_width=self.menu_auto_width, width=self.menu_width)
        menu_button_class = getattr(Factory, self.button_viewclass)
        spacer_class = getattr(Factory, self.spacer_viewclass)

        #set up heights
        if self.button_height < 0:
            button_height = self.height
        else:
            button_height = self.button_height
        if self.spacer_height < 0:
            spacer_height = button_height / 4
        else:
            spacer_height = self.spacer_height

        #generate menu
        for menu_data in self.menu:
            if menu_data is None:
                #Spacer
                spacer = spacer_class(size_hint_y=None, height=spacer_height)
                self.menu_object.add_widget(spacer)
            else:
                #Button
                button_name = menu_data['name']
                if 'submenu' in menu_data.keys():
                    #submenu, create a new button of same type as self
                    button = type(self)(text=button_name, size_hint_y=None, height=button_height, menu=menu_data['submenu'])
                    button.is_submenu = True
                    if 'menu_auto_width' in menu_data.keys():
                        button.menu_auto_width = menu_data['menu_auto_width']
                    if 'menu_width' in menu_data.keys():
                        button.menu_width = menu_data['menu_width']
                    button.menu_tree = self.menu_tree + [self]
                else:
                    #just a normal button
                    button = menu_button_class(text=button_name, size_hint_y=None, height=button_height)
                    if 'function' in menu_data.keys():
                        #bind functions if they are set
                        button_function = menu_data['function']
                        if 'args' in menu_data.keys():
                            args = menu_data['args']
                            button.bind(on_release=partial(self.function_passthrough, button_function, *args))
                        else:
                            button.bind(on_release=partial(self.function_passthrough, button_function))
                self.menu_object.add_widget(button)
        if self.is_submenu:
            try:
                self.menu_object.attach_side = True
            except:
                pass
        self.menu_object.open(self)

    def function_passthrough(self, button_function, *args):
        self.dismiss()
        button_function(*args[:-1])  #strip off the calling button, gets automatically appended to partial's args

    def dismiss(self, *_):
        if self.menu_object:
            if self.menu_tree:  #Close parent menus as well
                for parent_menu in self.menu_tree:
                    parent_menu.dismiss()
                self.menu_tree = []
            self.menu_object.dismiss()
            self.menu_object = None


class Test(App):
    menu = ListProperty()

    def test_function(self, *args):
        print(args)

    def build(self):
        self.menu = [
            {'name': 'New', 'function': self.test_function, 'args': ['New clicked', 'second variable']},
            {'name': 'Save', 'function': self.test_function, 'args': ['Save clicked']},
            {'name': 'Open', 'submenu': [
                {'name': 'First', 'function': self.test_function, 'args': ['Open first clicked']},
                {'name': 'Second', 'function': self.test_function, 'args': ['Open second clicked']},
                {'name': 'Third', 'function': self.test_function, 'args': ['Open third clicked']},
                {'name': 'Fourth', 'function': self.test_function, 'args': ['Open fourth clicked']}]},
            None,
            {'name': 'Quit', 'function': self.stop}
        ]
        return Builder.load_string(KV)


if __name__ == '__main__':
    Test().run()
