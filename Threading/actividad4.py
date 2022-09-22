import mysql.connector
import requests
import threading
import pytube
import time

#Actividad 4 - Hiram Emilio Lache Toledo 203420

#Generar una solicitud a randomuser de 50 usuarios diferentes
def get_services():
    time.sleep(10)
    print("Iniciando descarga de videos...")
    for _ in range(0,50):
        response = requests.get('https://randomuser.me/api/')
        if response.status_code == 200:
            results = response.json().get('results')
            name = results[0].get('name').get('first')
            print(name)
    print("PROCESO 50 USUARIOS FINALIZADO")
 
#Descargar 5 videos
def download_vid(urls):
    path = "./clase 8_09_22/videos"
    time.sleep(5)
    for i in urls:
        yt = pytube.YouTube(i)
        #yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(path)
        yt.streams.first().download(path)
    print("PROCESO VIDEOS FINALIZADO")

#Escribir 2000 registros en base de datos
def get_service2():
    req = requests.get("https://jsonplaceholder.typicode.com/photos?_start=0&_limit=2000")
    res = req.json()
    write_db(res)

def write_db(data):
    try:
        db = mysql.connector.connect(user='root', host='localhost', database='python', port='3307')
        if db.is_connected():
            print("Conexión exitosa...")
            cursor = db.cursor()
            for x in data:
                sql = "INSERT INTO testdb(title) VALUES('"+x["title"]+"')"
                cursor.execute(sql)
                db.commit()

    except e as e:
        print("Error al conectarse: ", e)
    finally:
        if db.is_connected():
            db.close()
            print("Conexión finalizada")
            print("PROCESO BASE DATOS FINALIZADO")
   


if __name__ == '__main__':
    urls = ["https://youtu.be/RlOB3UALvrQ", "https://youtu.be/zzBIzYmxatU", "https://youtu.be/fWQrd6cwJ0A", "https://youtu.be/In8fuzj3gck", "https://youtu.be/wxN1T1uxQ2g"]

    th1 = threading.Thread(target=get_services)
    th2 = threading.Thread(target=get_service2)
    th3 = threading.Thread(target=download_vid, args= [urls])

    th1.start()
    th2.start()
    th3.start()