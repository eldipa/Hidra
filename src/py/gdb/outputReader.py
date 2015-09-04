import threading
from gdb_mi import Output, Record, Stream
import publish_subscribe.eventHandler


class OutputReader(threading.Thread):
    
    def __init__(self, gdbOutput, queue, gdbPid): 
        threading.Thread.__init__(self)
        self.eventHandler = publish_subscribe.eventHandler.EventHandler(name="(output reader of %i)" % gdbPid)
        self.queue = queue
        self.parser = Output()
        self.gdbOutput = gdbOutput
        self.daemon = True
        self.gdbPid = gdbPid
        self.pid = 0
    
    def run(self):
        quit = False

        while not quit:
            line = ""
            try:
                line = self.gdbOutput.readline()
                if line == "":
                  quit = True
                  continue
            except:
                quit = True
                continue

            record = self.parser.parse_line(line)
            
            if record == "(gdb)":
               continue

            if isinstance(record, Record):
                if (record.klass == "thread-group-started"):
                    self.pid = record.results["pid"]
                    self.eventHandler.publish("debugger.new-target.%i" % self.gdbPid , {'gdbPid': self.gdbPid, 'targetPid': self.pid})
                
            data = vars(record)
            data['debugger-id'] = self.gdbPid
            if record.type == "Sync":
               token = 0 if record.token is None else record.token
               topic = "result-gdb.%i.%i.%s" % (self.gdbPid, token, record.klass.lower())

            elif record.type in ("Console", "Target", "Log"):
               # Console: is output that should be displayed as is in the console. 
               #      It is the textual response to a CLI command.
               # Target: is the output produced by the target program.
               # Log: output is output text coming from gdb's internals, 
               #      for instance messages that should be displayed as part of 
               #      an error log. 
               #
               # Source: https://sourceware.org/gdb/onlinedocs/gdb/GDB_002fMI-Output-Syntax.html#GDB_002fMI-Output-Syntax
               assert isinstance(record, Stream)
               topic = "stream-gdb.%i.%s" % (self.gdbPid, record.type.lower())
               
            else:
               # Exec: contains asynchronous state change on the target (stopped, 
               #      started, disappeared). 
               # Status: contains on-going status information about the progress 
               #      of a slow operation. It can be discarded.
               # Notify: contains supplementary information that the client 
               #      should handle (e.g., a new breakpoint information).
               #
               # Source: https://sourceware.org/gdb/onlinedocs/gdb/GDB_002fMI-Output-Syntax.html#GDB_002fMI-Output-Syntax
               assert record.type in ("Exec", "Status", "Notify")
               topic = "notification-gdb.%i.%s.%s" %(self.gdbPid, record.type.lower(), record.klass.lower())
 
            self.eventHandler.publish(topic, data)
        
        # here we are really sure that gdb "is dead"
        self.eventHandler.publish("spawner.debugger-exited", {"debugger-id": self.gdbPid,
                                                              "exit-code": -1})
