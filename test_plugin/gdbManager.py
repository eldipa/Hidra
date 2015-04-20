import gdb.gdbSpawmer
import publish_subscribe.eventHandler 
import os
from time import sleep
import socket


NOTIFIER_UP = True
NOTIFIER_DOWN = False

class gdbManager:
    
    def __init__(self):
        self.spawmer = None
        self.events = []
        os.system("python ../src/py/publish_subscribe/notifier.py start")
        self.wait_until(NOTIFIER_UP)
        self.eventHandler = publish_subscribe.eventHandler.EventHandler()
        self.eventHandler.subscribe("", self.registerEvent)
        
        
    def registerEvent(self, event):
        self.events.append(event)
        
    def loadPlugIn(self, plugin):
        self.spawmer = gdb.gdbSpawmer.GdbSpawmer(log=True, debugPlugin=plugin)
        
    def starNewProcess(self, path):
        gdbPid = self.spawmer.startNewProcessWithGdb(path)
        return gdbPid
        
    def publish(self, topic, data):
        self.eventHandler.publish(topic, data)
        
    def close(self):
        self.spawmer.shutdown()
        self.eventHandler.close()
        os.system("python ../src/py/publish_subscribe/notifier.py stop")
        self.wait_until(NOTIFIER_DOWN)
            
    # #COPIA DE EVENTHANDLER
    def _get_address(self):
        import os, ConfigParser
        script_home = os.path.abspath(os.path.dirname(__file__))
        parent = os.path.pardir

        # TODO This shouldn't be hardcoded!
        config_file = os.path.join(script_home, parent, "config", "publish_subscribe.cfg")

        config = ConfigParser.SafeConfigParser(defaults={
                    'wait_on_address': "localhost",
                    'wait_on_port': "5555",
                     })

        config.read([config_file])
        if not config.has_section("notifier"):
            config.add_section("notifier")


        address = (config.get("notifier", 'wait_on_address'), config.getint("notifier", 'wait_on_port'))

        return address
    
    def tryNewConection(self):
        isUp = None
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(self._get_address())
            isUp = True
        except Exception as inst:
            isUp = False
#             print "Exception: " + str(type(inst)) + " errno:" + os.strerror(inst.errno)
        
        return isUp
            
    def wait_until(self, stopConditon):
        timeout = 2
        step = 0.01
        stop = False
        while not stop  and timeout > 0:
            sleep(step)
            timeout -= step
            status = self.tryNewConection()
            if (status == stopConditon):
                stop = True
        
        if not stop:
            raise Exception
        
        
    
    
    