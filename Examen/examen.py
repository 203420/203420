import threading
import time

#Hiram Emilio Lache Toledo - 203420
#Programación concurrente Evaluación C1

#Arreglo de mutexes para verificar si el palillo esta en uso o libre
palillos = [threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock(),threading.Lock(), threading.Lock(), threading.Lock(), threading.Lock()]

mutex = threading.Lock()

def liberar_palillos(id):
    if id == len(palillos)-1:
        if "locked _thread.lock" in str(palillos[0]):  
            palillos[0].release()                       
    else:
        if "locked _thread.lock" in str(palillos[id+1]):  
            palillos[id+1].release()


def obtener_palillos(id):
    res = 0
    if "unlocked _thread.lock" in str(palillos[id]):  #Verificiar si el palillo(izq) esta bloqueado
        palillos[id].acquire()
        if id == len(palillos)-1:
            palillos[0].release()
            if "unlocked _thread.lock" in str(palillos[0]): #Verificiar si el palillo(der) esta bloqueado 
                palillos[0].acquire()                       #Caso especial para la ultima persona (su palillo derecho vuelve a ser el primero)
                res = 1
        else:
            if "unlocked _thread.lock" in str(palillos[id+1]):  #Verificiar si el palillo(der) esta bloqueado
                palillos[id+1].acquire()
                res = 1
    return res


def comer(id):
    ciclo = True
    while ciclo == True:
        comer = obtener_palillos(id)  #0 = No tiene 2 palillos      1 = Tiene 2 palillos
        time.sleep(0.5)
        if comer == 1: 
            print("\nPersona "+str(id+1)+" comiendo...")
            time.sleep(5)
            print("\nPersona "+str(id+1)+" termino de comer!")
            liberar_palillos(id)
            ciclo = False
        
        
                
class Persona(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id=id

    def run(self):
        mutex.acquire()
        comer(self.id)
        mutex.release()
        
        
if __name__=="__main__": 
    for i in range(8):
        p = Persona(i)
        p.start()
    