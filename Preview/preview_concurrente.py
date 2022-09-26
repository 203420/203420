import threading
import requests
import time

#Se incluyen 3 urls que no funcionan, estas son nombradas como "fakeurls"
urls = ["https://github.com","https://developer.mozilla.org/es/", "https://www.w3schools.com", "https://www.youtube.com","https://www.twitch.tv",
"https://cinepolis.com", "https://cinemex.com", "https://www.apple.com/mx/", "https://www.xbox.com/es-MX", "https://www.fakeurls.com",
"https://www.nintendo.com/es-mx/", "https://www.playstation.com/es-mx/ps5/", "https://www.epicgames.com/fortnite/es-MX/home", "https://www.bershka.com/mx/", "https://www.nvidia.com/es-la/",
"https://disneylatino.com/", "https://www.netflix.com/mx/", "https://www.logitech.com/es-mx", "https://www.beatsbydre.com/mx", "https://www.amazon.com.mx/",
"https://www.samsung.com/mx/", "https://www.fakeurls2.com", "https://mx.puma.com/", "https://www.fakeurls3.com", "https://www.redbull.com/mx-es/"]

def site_requests(url):
    try:
        res = requests.head(url)
        print("\n--------------------------")
        print("URL: "+ url)
        print("Response: " +str(res.status_code))
        
        if res.status_code == 200:
            print("Pagina activa")
        else:
            print("La solicitud no se proceso correctamente")
        print("--------------------------")
    except:
        print("\n--------------------------")
        print("URL: "+ url)
        print("Error al conectar. Pagina inactiva")
        print("--------------------------")

    
class Hilo(threading.Thread):
    def __init__(self, id, url):
        threading.Thread.__init__(self)
        self.id=id
        self.url=url

    def run(self):
        site_requests(self.url)

if __name__=="__main__":
    for i in range(4):    #Realiza 4 verificaciones en 8 minutos
        print("Verificación "+str(i+1))
        for u in urls:
            h = Hilo(urls.index(u), u)
            h.start()
            time.sleep(0.25)
        time.sleep(120)

