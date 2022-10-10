from queue import Queue
import threading
import time

#Hiram Emilio Lache Toledo 203420
#Actividad 01-02 Programación concurrente 7B

bodega = Queue(maxsize=10)
mutex1 = threading.Lock()
mutex2 = threading.Lock()

class Consumidor(threading.Thread):
    cont = 0

    def __init__(self):
        super(Consumidor, self).__init__()
        self.id = Consumidor.cont
        Consumidor.cont += 1

    def consumir(self):
        print("Consumiendo...")
        time.sleep(1.25)

        mutex2.acquire()
        time.sleep(0.15)
        bodega.get()
        mutex2.release()

        print("Se consumio un producto")

    def run(self):
        while True:
            if bodega.empty() == False:
                self.consumir()   
            print("Bodega: "+ str(list(bodega.queue)))
            time.sleep(10)


class Productor(threading.Thread):
    cont = 0

    def __init__(self):
        super(Productor, self).__init__()
        self.id = Productor.cont
        Productor.cont += 1

    def producir(self):
        print("Productor "+str(self.id+1)+" produciendo...")
        time.sleep(2)

        mutex1.acquire()
        time.sleep(0.05)
        bodega.put("x")
        mutex1.release()

        print("Se agrego un nuevo producto")

    def run(self):
        while True:
            if bodega.full() == False:
                self.producir()   
            print("Bodega: "+ str(list(bodega.queue)))
            time.sleep(10)

if __name__ == "__main__":
    consumidores = []
    productores = []

    for i in range(12):
        productores.append(Productor())
        consumidores.append(Consumidor())   

    for p in productores:
        p.start()

    for c in consumidores:
        c.start()

    
