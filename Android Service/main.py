"""
Example of how to run, stop, and communicate with a service in android
"""

from kivy.app import App
from kivy.clock import mainthread
from kivy.lang.builder import Builder
from kivy.properties import *
from kivy.utils import platform

if platform == 'android':
    #import tools for communicating with service
    from oscpy.server import OSCThreadServer
    from oscpy.client import OSCClient

    #import android-specific stuff
    from jnius import autoclass
    from android.permissions import request_permission, check_permission, Permission

    #check for and request service permissions
    can_internet = check_permission(Permission.INTERNET)  #Internet permission is required for communication between service and app
    if not can_internet:
        request_permission(Permission.INTERNET)

    can_foreground = check_permission(Permission.FOREGROUND_SERVICE)
    if not can_foreground:
        request_permission(Permission.FOREGROUND_SERVICE)


KV = """
GridLayout:
    cols: 1
    Label: 
        text: "Last Message From Service: "+app.message
    Button:
        text: "Stop Service" if app.background_service else "Start Service"
        on_release: app.toggle_service()
    Button:
        text: "Tell Service To Restart Count"
        on_release: app.send_command_to_service("Reset")
"""


class ServiceTestApp(App):
    message = StringProperty()

    background_service = ObjectProperty(allownone=True)  #store the background service so it can easily be shut down later
    osc_server = None  #store the communication server so it can be shut down later
    osc_client = None  #store the communication client so it can be used to send messages

    def send_command_to_service(self, message):
        if self.osc_client:
            self.osc_client.send_message(b'/app_command_receive', [message.encode("utf8")])

    def receive_message_from_service(self, message):
        self.message = message

    @mainthread
    def start_service(self):
        if platform == 'android':
            if not self.background_service:
                #Create or import the background service (will automatically import if already running)
                #class name will be (variables from buildozer.spec):
                #   service_name = services.split(':')[0]
                #   package.domain + '.' + package.name + '.Service' + service_name.title()
                self.background_service = autoclass('com.snuq.servicetest.ServiceServicetestbg')
                m_activity = autoclass('org.kivy.android.PythonActivity').mActivity
                argument = ''
                self.background_service.start(m_activity, argument)
            if not self.osc_client:
                #setup the message client for sending messages to service
                self.osc_client = OSCClient("localhost", 30105)  #this port must match the one used by the service's osc_server
            if not self.osc_server:
                #setup the message server for receiving messages from the service
                self.osc_server = OSCThreadServer(encoding="utf8")
                self.osc_server.listen("localhost", port=30104, default=True)  #this port must match the one used by the service's osc_client
                #any number of message 'channels' can be used to communicate in either direction
                self.osc_server.bind(b"/service_message_receive", self.receive_message_from_service)
                self.osc_server.bind(b"/service_stop_request", self.stop_service)

    def stop_service(self, *_):
        #run this in the same thread as the caller, so it runs while screen is off
        if self.background_service:
            m_activity = autoclass('org.kivy.android.PythonActivity').mActivity
            self.background_service.stop(m_activity)
            self.background_service = None
        self.stop_service_support()

    @mainthread
    def stop_service_support(self):
        #run this in main thread so it only runs while screen is on, must be run before server is started again
        if platform == 'android':
            if self.osc_server:
                self.osc_server.stop_all()  #Stop all sockets
                self.osc_server.terminate_server()  #Request the handler thread to stop looping
                self.osc_server.join_server()
                self.osc_server = None
            if self.osc_client:
                self.osc_client = None

    def toggle_service(self):
        if self.background_service:
            self.stop_service()
        else:
            self.start_service()

    def build(self):
        self.start_service()
        return Builder.load_string(KV)

    def on_stop(self):
        self.stop_service()


ServiceTestApp().run()
