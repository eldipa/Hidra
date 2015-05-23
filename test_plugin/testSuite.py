import unittest
import os
import time 
import sys
import pprint
import select
from time import sleep
sys.path.append("../src/py")
sys.path.append("../src/ipc/pyipc")
import gdbManager

testCodePath = "./cppTestCode/"

class CompleteTest(unittest.TestCase):

    
    def setUp(self):
        self.manager = gdbManager.gdbManager()
    
    def test_stdioRedirect_load(self):
        # De quererse configurar el constructor del spawmer con algun argumento en particular, se debe configurar
        # de la siguiente manera, si no se ejecuta esta linea, spawmer tomara los valores por default.
        self.manager.configSpawmer(log=True, inputRedirect=True, debugPlugin=["stdioRedirect.py"])
        
        gdbPid = self.manager.starNewProcess(testCodePath + "stdinTest")
        
        self.manager.publish(str(gdbPid) + ".run", "")
        sleep(2)
        
        # Busco si en los evento generados hay un string en particular
        event = self.manager.anyEventHasThisString("redirecting Output on Breakpoint")
        self.assertIsNotNone(event, "No se encontro el evento de redireccion de salida")
        
        event = self.manager.anyEventHasThisString("redirecting Input on Breakpoint")
        self.assertIsNotNone(event, "No se encontro el evento de redireccion de entrada")
        
        event = self.manager.anyEventHasThisString("Ingrese un texto:")
        self.assertIsNotNone(event, "No se encontro el evento de string en output")
        
        # Para borrar los eventos guardados, y asi poder ver solo los nuevos
        self.manager.resetEvents()
        
        # si quiero escribir/leer por entrada/salida estandar de un gdb:
        gdbIO = self.manager.getGdbIO(gdbPid)
        
#         gdbIO['input'].write("Mensaje de prueba") #esto iria directo a gdb como si de un comando se tratase

        r, w, e = select.select([ gdbIO['output'].fileno() ], [], [], 0)
        msg = None
        if len(r) > 0:
            msg = os.read(gdbIO['output'].fileno(), 10000)  # non block
        
        self.assertIsNone(msg, "Hubo un mensaje en la salida estandar: " + str(msg))
    
      
#     def test_stdioRedirect_attach(self):
#         self.assertTrue(True)
    
    def tearDown(self):
        self.manager.close()    
    
if __name__ == '__main__':
    os.chdir("../src")
    print os.getcwd()
    suite = unittest.TestLoader().loadTestsFromTestCase(CompleteTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
