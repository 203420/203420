# CALLBACKS
import requests
import threading

def get_service_1(reponse_json_data):
    print(reponse_json_data)

def get_error_1():
    print("Error en la solicitud")

def get_service_2(reponse_json_data):
    print(reponse_json_data)

def get_error_2():
    print("Error en la solicitud")

def request_data(url, success_callback, error_callback):
    response = requests.get(url)
    if response.status_code == 200:
        success_callback(response.json())
    else:
        error_callback()

class Hilo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        h1 = threading.Thread(target=request_data,
        kwargs={
            'url':'https://randomuser.me/api/',
            'success_callback': get_service_1,
            'error_callback': get_error_1
        })
        h1.start()

        h2 = threading.Thread(target=request_data,
        kwargs={
            'url':'https://jsonplaceholder.typicode.com/todos?_start=0&_limit=10',
            'success_callback': get_service_2,
            'error_callback': get_error_2
        })
        h2.start()

hilo = Hilo()
hilo.start()