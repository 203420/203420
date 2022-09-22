from asyncio import streams
import pytube
import concurrent.futures
import threading
import time

thrading_local = threading.local()

def threads(urls, path):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(cicle(urls, path))
    
def cicle(urls, path):
    for i in urls:
        download_vid(i, path)

def download_vid(url, path):
    yt = pytube.YouTube(url)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download(path)
    #yt.streams.first().download(path)

if __name__=="__main__":
    urls = ["https://youtu.be/RlOB3UALvrQ", "https://youtu.be/zzBIzYmxatU", "https://youtu.be/fWQrd6cwJ0A", "https://youtu.be/In8fuzj3gck", "https://youtu.be/wxN1T1uxQ2g"]
    path = "./clase 7_09_22/videos"

    init_time = time.time()
    threads(urls, path)
    end_time = time.time() - init_time
    print("---------------------")
    print(end_time)
    print("---------------------")