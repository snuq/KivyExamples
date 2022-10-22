from kivy.app import App
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.clock import Clock
from kivy.lang import Builder
Builder.load_string("""
#:import kivy kivy
<Screen1>:
    Label:
        id: countdown
        text: 'Switching In: '+str(root.count)

<Screen2>:
    Label:
        text: 'screen 2'
""")

class Screen1(Screen):
    count = NumericProperty()
    def on_enter(self):
        self.count = 3
        Clock.schedule_once(self.update_count, 1)

    def update_count(self, *_):
        self.count -= 1
        if self.count == 0:
            app = App.get_running_app()
            app.manager.current = 'screen 2'
        else:
            Clock.schedule_once(self.update_count, 1)

class Screen2(Screen):
    pass

class Test(App):
    def build(self):
        self.manager = ScreenManager()
        self.manager.add_widget(Screen1(name='screen 1'))
        self.manager.add_widget(Screen2(name='screen 2'))
        return self.manager

if __name__ == '__main__':
    Test().run()
