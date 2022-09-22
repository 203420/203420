import mysql.connector
import concurrent.futures
import threading
import requests
import time


thrading_local = threading.local()

#Consumir un servicio que descargue por lo menos 5000 registros
def service(url):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(get_service(url))

def get_service(url):
    #Implementación de requests
    req = requests.get(url)
    res = req.json()
    write_db(res)

def write_db(data):
    #Escribir el response en una base de datos
    try:
        db = mysql.connector.connect(user='root', host='localhost', database='python', port='3307')
        if db.is_connected():
            print("Conexión exitosa...")
            cursor = db.cursor()
            for x in data:
                sql = "INSERT INTO data(title) VALUES('"+x["title"]+"')"
                cursor.execute(sql)
                db.commit()

    except e as e:
        print("Error al conectarse: ", e)
    finally:
        if db.is_connected():
            db.close()
            print("Conexión finalizada")
   

if __name__=="__main__":
    url = "https://jsonplaceholder.typicode.com/photos"
    init_time = time.time()
    service(url)
    end_time = time.time() - init_time
    print("---------------------------------")
    print(end_time)