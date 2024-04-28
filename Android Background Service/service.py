import time
from oscpy.server import OSCThreadServer
from oscpy.client import OSCClient
from jnius import autoclass
counter = 0


def receive_command_from_app(message):  #this function will be executed in the osc_server's thread, so the variables it sets could change at any time during the main loop below
    #message channels can be used to communicate many different things or run multiple commands
    if message == 'Reset':
        global counter
        counter = 0


#Set up communications with the app
osc_client = OSCClient("localhost", 30104)  #This port must match the port of the osc_server in the app
osc_server = OSCThreadServer(encoding="utf8")
osc_server.listen("localhost", port=30105, default=True)  #This port must match the port of the osc_client in the app
osc_server.bind(b"/app_command_receive", receive_command_from_app)  #Any number of communication 'channels' may be created to send data.

while True:  #This loop must not be broken out of! This will cause android to complain about the service 'crashing'
    #Send a message to the app to update status of service
    osc_client.send_message(b"/service_message_receive", ["Counter: ".encode("utf8")+str(counter).encode("utf8")])

    #Run some code here
    time.sleep(0.5)
    counter += 1

    if counter > 30:
        #Service is all done, ask the app to terminate the service
        background_service = autoclass('com.snuq.servicetest.ServiceServicetestbg')
        osc_client.send_message(b"/service_stop_request", ['Stop'.encode("utf8")])
