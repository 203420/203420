import mysql.connector
import requests
import time

#Actividad 3 - Hiram Emilio Lache Toledo 203420

#Implementación de requests
def get_service(url):
    req = requests.get(url)
    res = req.json()
    write_db(res)


#Escribir el response en una base de datos 
def write_db(data):
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
    get_service(url)
    end_time = time.time() - init_time
    print("---------------------------------")
    print(end_time)