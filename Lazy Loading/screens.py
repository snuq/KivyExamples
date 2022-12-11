from kivy.uix.screenmanager import Screen
from kivy.lang.builder import Builder
Builder.load_string("""
<Screen1>:
    BoxLayout:
        Label:
            text: 'Screen 1'
        Button:
            text: 'Switch To Screen 2'
            on_release: app.show_screen2()
        Button:
            text: 'Switch To Screen 3'
            on_release: app.show_screen3()

<Screen2>:
    BoxLayout:
        Label:
            text: 'Screen 2'
        Button:
            text: 'Switch To Screen 1'
            on_release: app.show_screen1()
        Button:
            text: 'Switch To Screen 3'
            on_release: app.show_screen3()

<Screen3>:
    BoxLayout:
        Label:
            text: 'Screen 3'
        Button:
            text: 'Switch To Screen 1'
            on_release: app.show_screen1()
        Button:
            text: 'Switch To Screen 2'
            on_release: app.show_screen2()
""")

class Screen1(Screen):
    pass

class Screen2(Screen):
    pass

class Screen3(Screen):
    pass
