"""Example showing a screen layout that will automatically change screens after a period of time."""
from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.clock import Clock
KV = """
<Screen1>:
    Label:
        text: 'screen 1'

<Screen2@Screen>:
    Button:
        text: 'screen 2, click to switch'
        on_release: root.manager.current = 'screen 3'

ScreenManager:
    Screen1:
        name: 'screen 1'
    Screen2:
        name: 'screen 2'
    Screen:
        name: 'screen 3'
        Label:
            text: 'screen 3'
"""

class Screen1(Screen):
    def on_enter(self):
        app = App.get_running_app()
        Clock.schedule_once(app.second_screen, 3)

class Test(App):
    def build(self):
        return Builder.load_string(KV)
        
    def second_screen(self, *_):
        self.root.current = 'screen 2'

if __name__ == '__main__':
    Test().run()
