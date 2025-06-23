from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform

desktop = platform in ['win', 'linux', 'macosx', 'unknown']


class Test(App):
    window_top = None
    window_left = None
    window_width = None
    window_height = None
    window_maximized = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_resize=self.window_on_size)
        Window.bind(on_draw=self.window_on_draw)
        Window.bind(on_maximize=lambda x: setattr(self, 'window_maximized', True))
        Window.bind(on_restore=lambda x: setattr(self, 'window_maximized', False))

    def build_config(self, config):
        """Setup config file if it is not found"""

        config.setdefaults(
            'Settings', {
                'remember_window': 1,
                'window_maximized': 0,
                'window_top': 50,
                'window_left': 100,
                'window_width': 800,
                'window_height': 600,
            })

    def window_init_position(self, *_):
        #Set window position from saved settings
        self.window_top = self.config.getint('Settings', 'window_top')
        self.window_left = self.config.getint('Settings', 'window_left')
        Window.left = self.window_left
        Window.top = self.window_top

    def window_on_draw(self, *_):
        #need to have this because kivy on windows will not trigger Window.on_resize on startup...
        if self.window_height is None:
            self.window_on_size()

    def window_on_size(self, *_):
        if self.window_height is None:
            #app just started, window is uninitialized, load in stored size if enabled
            if self.config.getboolean("Settings", "remember_window") and desktop:
                self.window_maximized = self.config.getboolean('Settings', 'window_maximized')
                self.window_width = self.config.getint('Settings', 'window_width')
                self.window_height = self.config.getint('Settings', 'window_height')
                Window.size = (self.window_width, self.window_height)
                if self.window_maximized:
                    Window.maximize()
                else:
                    Clock.schedule_once(self.window_init_position)  #Need to delay this to ensure window has time to resize first
        else:
            #Window is resized by user
            self.check_window()

    def check_window(self, *_):
        #Checks window size and position, stores if they changed
        self.config.set("Settings", "window_maximized", 1 if self.window_maximized else 0)
        if not self.window_maximized:
            if Window.left != self.window_left and self.window_left is not None:  # Left changed
                self.window_left = Window.left
                self.config.set('Settings', 'window_left', self.window_left)
            if Window.top != self.window_top and self.window_top is not None:  #Top changed
                self.window_top = Window.top
                self.config.set('Settings', 'window_top', self.window_top)
            if Window.width != self.window_width and self.window_width is not None:  #Width changed
                self.window_width = Window.width
                self.config.set('Settings', 'window_width', self.window_width)
            if Window.height != self.window_height and self.window_height is not None:  #Height changed
                self.window_height = Window.height
                self.config.set('Settings', 'window_height', self.window_height)

    def save_window(self):
        self.check_window()
        self.config.write()

    def on_stop(self):
        self.save_window()


if __name__ == '__main__':
    Test().run()
