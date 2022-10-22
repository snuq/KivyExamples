'''
SoundAndroid: implementation of Sound using Android's Java MediaPlayer class.
Works Android only, will not return anything on other OS's
'''

__all__ = ('SoundAndroid', )

import os
from kivy.core.audio import Sound, SoundLoader

class SoundAndroid(Sound):
    _sound = None

    @staticmethod
    def extensions():
        if 'ANDROID_ARGUMENT' in os.environ:
            return ("aac", "mp3", "flac", "m4a", "wav", "ogg", "mid")
        else:
            return

    def load(self):
        self.unload()
        from jnius import autoclass
        MediaPlayer = autoclass('android.media.MediaPlayer')
        self._sound = MediaPlayer()
        self._sound.setDataSource(self.source)
        self._sound.prepare()

    def unload(self):
        if self._sound:
            self._sound.release()
            self._sound = None
        self.state = 'stop'

    def play(self):
        if not self._sound:
            self.load()
        self._sound.start()
        self.state = 'play'
        super().play()

    def stop(self):
        if self._sound:
            self._sound.pause()
            self.state = 'stop'
        super().stop()

    def seek(self, position):
        if self._sound is None:
            return
        self._sound.seekTo(position / 1000)

    def get_pos(self):
        if self._sound is not None:
            return self._sound.getCurrentPosition() * 1000
        return 0

    def _get_length(self):
        if self._sound is None:
            return 0
        return self._sound.getDuration() * 1000

    def on_volume(self, instance, volume):
        if self._sound:
            self._sound.setVolume(volume, volume)

    def on_loop(self, instance, loop):
        if self._sound:
            self._sound.setLooping(loop)

SoundLoader.register(SoundAndroid)
