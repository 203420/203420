import threading, time, random
from queue import Queue
from termcolor import colored

#Programación Concurrente 7°B 
#Aplicación: Restaurante Marriot  - Monitores

#Hiram Emilio Lache Toledo - 203420
#Raul Alejandro Alvarez Calvo - 203407

CAPACIDAD = 20  
RESERVACIONES = CAPACIDAD * 0.2
MESEROS = CAPACIDAD*0.1
COCINEROS = CAPACIDAD*0.1

class Monitor():
    mutex = threading.Lock()

    condIngresoR = threading.Condition()
    condCapacidad = threading.Condition()

    condAtender = threading.Condition()
    condCocinar = threading.Condition()

    ingresoR = Queue(RESERVACIONES)
    pedidos = Queue()
    comidas = Queue()

    restaurante = Queue(CAPACIDAD)
    restaurante2 = Queue(CAPACIDAD)

    def __init__(self):
        super(Monitor,self).__init__()

    def __reservacion__(self, cliente):
        self.condIngresoR.acquire()
        if self.ingresoR.full() == False:
            self.ingresoR.put(cliente)
            print (colored("Cliente "+str(cliente.id)+" ingreso a la cola con reservación...", "grey"))
            time.sleep(3.5)  
            print (colored("Cliente "+str(cliente.id)+" llego al restaurante (con reservación)", "grey"))
            time.sleep(0.5)

            self.mutex.acquire()
            self.__ingresar__(cliente)
            self.ingresoR.get()

            self.condIngresoR.notify()
            self.condIngresoR.release()           
        else:
            self.condIngresoR.wait()   
                

    def __no_reservacion__(self, cliente):
        self.condIngresoR.acquire()
        print (colored("Cliente "+str(cliente.id)+" llego al restaurante", "grey"))
        time.sleep(1)

        self.mutex.acquire()
        self.__ingresar__(cliente)
                    
        self.condIngresoR.notify()
        self.condIngresoR.release()        
                
    
    def __ingresar__(self, cliente):
        self.condCapacidad.acquire()
        if self.restaurante.full() == False:
            print (colored("Cliente "+str(cliente.id)+" ingreso al restaurante...", "cyan"))
            time.sleep(1.5)
            self.restaurante.put(cliente)
            print (colored("El recepcionista asigno una mesa a cliente: "+str(cliente.id), "blue"))

            self.condAtender.acquire()
            self.condAtender.notify()
            self.condAtender.release()

            self.mutex.release()
            self.condCapacidad.release()
        else:
            print (colored("Cliente "+str(cliente.id)+" esperando una mesa...", "red"))
            self.condCapacidad.wait()


    def __atender__(self, mesero):
        while True:
            time.sleep(2)
            self.condAtender.acquire()  
            if self.restaurante.empty() == False:  
                cliente =  self.restaurante.get()
                if cliente.atendido == False:
                    print (colored("Mesero "+str(mesero.id+1)+" atendiendo a cliente "+str(cliente.id)+"...", "magenta"))
                    print (colored("Se agrego el pedido de cliente "+str(cliente.id)+" a la cola", "magenta"))
                    self.pedidos.put(cliente.id)

                    self.condCocinar.acquire()
                    self.condCocinar.notify()
                    self.condCocinar.release()

                    cliente.atendido = True
                    self.condAtender.release()
                else:
                    self.condAtender.release()
            else:
                print (colored("Mesero "+str(mesero.id+1)+" descansando...", "red"))
                self.condAtender.wait()


    def __cocinar__(self, cocinero):
        while True:
            time.sleep(1)
            self.condCocinar.acquire()
            if self.pedidos.empty() == False:
                pedido = self.pedidos.get()
                print (colored("Cocinero "+str(cocinero.id+1)+" cocinando pedido de cliente "+str(pedido)+"...", "yellow"))
                time.sleep(2.5)
                print (colored("Pedido de cliente "+str(pedido)+" terminado", "yellow"))
                self.comidas.put(pedido)
                self.condCocinar.release()
            else:
                print (colored("Cocinero "+str(cocinero.id+1)+" descansando...", "red"))
                self.condCocinar.wait()


    def __comer__(self):
            time.sleep(0.5)
            if self.comidas.empty() == False:
                c =self.comidas.get()
                print (colored("Cliente "+str(c)+" comiendo...", "green"))
                time.sleep(3.5)
                print (colored("Cliente "+str(c)+" termino de comer!", "green"))
                print (colored("Cliente "+str(c)+" salio del restaurante!", "green"))

            
            
class Cocinero(threading.Thread):   
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id=id

    def run(self):
        monitor.__cocinar__(self)


class Mesero(threading.Thread):   
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id=id

    def run(self):
        monitor.__atender__(self)


class Cliente(threading.Thread):
    atendido = False
    def __init__(self, id, reservacion):
        threading.Thread.__init__(self)
        self.id=id
        self.reservacion = reservacion
    
    def run(self):
        time.sleep(0.15)
        if self.reservacion:
            monitor.__reservacion__(self)
        else:
            monitor.__no_reservacion__(self)
        
        monitor.__comer__()


if __name__ == "__main__":
    monitor = Monitor()

    clientes = []
    meseros = []
    cocineros = []

    for i in range(25):
        value = random.choice([True, False, False])
        clientes.append(Cliente(i, value))

    for i in range(int(MESEROS)):
        meseros.append(Mesero(i))

    for i in range(int(COCINEROS)):
        cocineros.append(Cocinero(i))


    for c in clientes:
        c.start()

    for m in meseros:
        m.start()

    for c in cocineros:
        c.start()