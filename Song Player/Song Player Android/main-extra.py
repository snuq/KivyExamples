import os
if 'ANDROID_ARGUMENT' in os.environ:
    from kivy.core.audio import SoundLoader
    from audio_android import SoundAndroid
    SoundLoader.register(SoundAndroid)

else:
    os.environ['KIVY_AUDIO'] = 'ffpyplayer'
    import ffpyplayer.player.core
    from kivy.core.audio import SoundLoader

from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, BooleanProperty, NumericProperty, DictProperty, OptionProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.progressbar import ProgressBar
from kivy.uix.video import Image
from kivy.clock import Clock
from kivy.lang.builder import Builder
KV = """
<SongPlayer>:
    canvas.after:
        Color:
            rgba: 0, 0, 0, .5 if self.disabled else 0
        Rectangle:
            size: self.size
            pos: self.pos
    rows: 1
    size_hint_y: None
    height: '44dp'
    disabled: not root._song

    SongPlayerStop:
        size_hint_x: None
        song: root
        width: '44dp'
        source: root.image_stop
        allow_stretch: True

    SongPlayerPlayPause:
        size_hint_x: None
        song: root
        width: '44dp'
        source: root.image_pause if root.state == 'play' else root.image_play
        allow_stretch: True

    Widget:
        size_hint_x: None
        width: 5

    SongPlayerProgressBar:
        song: root
        max: 1
        value: root.position

    Widget:
        size_hint_x: None
        width: 10

BoxLayout:
    orientation: 'vertical'
    BoxLayout:
        orientation: 'horizontal'
        Button:
            text: 'Volume 0'
            on_release: song.volume = 0
        Button:
            text: 'Volume 0.5'
            on_release: song.volume = 0.5
        Button:
            text: 'Volume 1'
            on_release: song.volume = 1
        ToggleButton:
            text: 'Loop'
            state: 'down' if song.loop else 'normal'
            on_release: song.loop = not song.loop
    SongPlayer:
        id: song
        source: "music.mp3"
    
"""

class SongPlayerPlayPause(Image):
    song = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.song.state == 'play':
                self.song.state = 'pause'
            else:
                self.song.state = 'play'
            return True


class SongPlayerStop(Image):
    song = ObjectProperty(None)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.song.state = 'stop'
            return True


class SongPlayerProgressBar(ProgressBar):
    song = ObjectProperty(None)
    seek = NumericProperty(None, allownone=True)
    scrub = BooleanProperty(True)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        touch.grab(self)
        self._update_seek(touch.x)
        if self.song.state != 'play':
            self.song.state = 'play'
        self.song.seek(self.seek)
        self.seek = None
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is not self:
            return
        if self.scrub:
            self._update_seek(touch.x)
            self.song.seek(self.seek)
            self.seek = None
        return True

    def on_touch_up(self, touch):
        if touch.grab_current is not self:
            return
        touch.ungrab(self)
        if self.seek is not None:
            self.song.seek(self.seek)
        self.seek = None
        return True

    def _update_seek(self, x):
        if self.width == 0:
            return
        x = max(self.x, min(self.right, x)) - self.x
        self.seek = x / float(self.width)


class SongPlayer(GridLayout):
    source = StringProperty('')
    length = NumericProperty(-1)
    position = NumericProperty(0)
    volume = NumericProperty(1.0)
    loop = BooleanProperty(False)
    state = OptionProperty('stop', options=('play', 'pause', 'stop'))
    image_play = StringProperty('atlas://data/images/defaulttheme/media-playback-start')
    image_stop = StringProperty('atlas://data/images/defaulttheme/media-playback-stop')
    image_pause = StringProperty('atlas://data/images/defaulttheme/media-playback-pause')
    _song = ObjectProperty(allownone=True)

    def __init__(self, **kwargs):
        self._song = None
        super(SongPlayer, self).__init__(**kwargs)

    def on_source(self, instance, value):
        if self._song is not None:
            self._song.unload()
            self._song = None
        if os.path.exists(self.source):
            self._song = SoundLoader.load(self.source)
            if self._song is None:
                return
            self._song.volume = self.volume
            self._song.state = self.state
            self.length = self._song.length

    def _update_position(self, *_):
        if self._song is None:
            return
        if self.state == 'play':
            self.position = (self._song.get_pos() / self.length)
            Clock.schedule_once(self._update_position)

    def on_state(self, instance, value):
        if self._song is not None:
            if value == 'play':
                self._song.play()
                self.seek(self.position)
                self._update_position()
            elif value == 'pause':
                self._song.stop()
            else:
                self._song.stop()
                self.position = 0

    def on_volume(self, instance, value):
        if not self._song:
            return
        self._song.volume = value

    def on_loop(self, instance, value):
        if not self._song:
            return
        self._song.loop = value

    def seek(self, percent):
        if not self._song:
            return
        self._song.seek(percent * self.length)


class Test(App):
    def build(self):
        return Builder.load_string(KV)

if __name__ == '__main__':
    Test().run()
