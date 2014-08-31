
'''
Created on 31/08/2014

@author: nicolas
'''

import gdb

bp1 = gdb.Breakpoint("pipe")

def stopHandler(stopEvent):
    for b in stopEvent.breakpoints:
        if b == bp1:
            print "Se hizo Pipe"
#             print "args = " + gdb.Symtab
            gdb.execute("info args")
            gdb.execute("continue")

gdb.events.stop.connect(stopHandler)