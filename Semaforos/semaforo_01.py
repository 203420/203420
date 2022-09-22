from threading import Thread, Semaphore
import requests

semaforo = Semaphore(1)

def crito(id):
    print("Hilo " +str(id)+ " descargando ... ")
    descarga(id)
    

def descarga(id):
    urls = ["https://creativereview.imgix.net/content/uploads/2018/12/Unknown-5.jpeg?auto=compress,format&q=60&w=2024&h=", 
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-03/28/1/asset/2b92f7d73e60/sub-buzz-6345-1648431180-3.jpg?downsize=350:*&output-format=auto&output-quality=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-04/4/20/asset/ee31c0fbc1e6/sub-buzz-406-1649104990-4.jpg?downsize=350:*&output-format=auto&output-quality=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-03/28/1/asset/3f02eb8471cd/sub-buzz-6772-1648431308-14.jpg?downsize=350:*&output-format=auto&output-quality=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-03/28/1/asset/5fb7e64ee15e/sub-buzz-6698-1648431332-13.jpg?downsize=350:*&output-format=auto&output-quality=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-04/4/20/asset/0f12255e2129/sub-buzz-817-1649105149-10.jpg?downsize=350%3A%2A&output-quality=auto&output-format=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-03/28/1/asset/fcf0aaaff603/sub-buzz-5991-1648431120-8.jpg?downsize=350:*&output-format=auto&output-quality=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-03/28/1/asset/0b9090d22b9d/sub-buzz-5968-1648431228-18.jpg?downsize=350:*&output-format=auto&output-quality=auto",
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-03/28/1/asset/fcf0aaaff603/sub-buzz-6008-1648431258-9.jpg?downsize=350:*&output-format=auto&output-quality=auto", 
    "https://img.buzzfeed.com/buzzfeed-static/static/2022-04/12/15/asset/b488203589e6/sub-buzz-619-1649777790-9.jpg?downsize=350:*&output-format=auto&output-quality=auto"]

    print(urls[id-1]+"\n")

    nombre = "img" + str(id) +".jpg"
    img = requests.get(urls[id-1]).content

    with open(nombre, 'wb') as handler:
	    handler.write(img)
        
class Hilo(Thread):
    def __init__(self, id):
        Thread.__init__(self)
        self.id=id

    def run(self):
        semaforo.acquire()  #Inicializa el semaforo
        crito(self.id)
        semaforo.release()  #Libera el semaforo e incrementa la variable

threads_semaphore = [Hilo(1), Hilo(2), Hilo(3), Hilo(4), Hilo(5), Hilo(6), Hilo(7), Hilo(8), Hilo(9), Hilo(10)]

for t in threads_semaphore:
    t.start()