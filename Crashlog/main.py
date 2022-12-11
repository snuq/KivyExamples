"""
Example that demonstrates how to save a crashlog into a text file for later use.
"""
import os
from kivy.app import App
from kivy.logger import Logger, LoggerHistory
from kivy.lang.builder import Builder
KV = """
BoxLayout:
    Button:
        text: 'Crash!'
        on_press: print(blah)
    Button:
        text: 'Open Crashlog'
        on_press: app.open_crashlog()
"""

class Test(App):
    def build(self):
        return Builder.load_string(KV)

    def open_crashlog(self):
        crashlog = os.path.realpath(self.get_crashlog_file())
        os.startfile(crashlog)

    def get_crashlog_file(self):
        """Returns the crashlog file path and name"""

        savefolder_loc = os.path.split(self.get_application_config())[0]
        crashlog = os.path.join(savefolder_loc, 'testapp_crashlog.txt')
        return crashlog

    def save_crashlog(self):
        """Saves the just-generated crashlog to the current default location"""

        import traceback
        crashlog = self.get_crashlog_file()
        log_history = reversed(LoggerHistory.history)
        crashlog_file = open(crashlog, 'w')
        for log_line in log_history:
            log_line = log_line.msg
            crashlog_file.write(log_line+'\n')
        traceback_text = traceback.format_exc()
        print(traceback_text)
        crashlog_file.write(traceback_text)
        crashlog_file.close()

if __name__ == '__main__':
    try:
        Test().run()
    except Exception as e:
        try:
            Test().save_crashlog()
        except:
            pass
        os._exit(-1)