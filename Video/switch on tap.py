from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder

Builder.load_string("""
<IntroScreen>:
    Video:
        id: videoPlayer
        on_eos: root.play_video()
        source: 'transparent.png'
    Button:
        opacity: 0
        on_press: app.manager.current = 'main'

<MainScreen>:
    Label:
        text: 'screen 2'
""")

class IntroScreen(Screen):
    def on_enter(self):
        self.play_video()

    def play_video(self):
        video_player = self.ids['videoPlayer']
        video_player.source = 'video.mp4'
        video_player.state = 'play'
        
    def on_leave(self):
        video_player = self.ids['videoPlayer']
        video_player.state = 'stop'

class MainScreen(Screen):
    pass

class Test(App):
    def build(self):
        self.manager = ScreenManager()
        self.manager.add_widget(IntroScreen(name='intro'))
        self.manager.add_widget(MainScreen(name='main'))
        return self.manager

if __name__ == '__main__':
    Test().run()
