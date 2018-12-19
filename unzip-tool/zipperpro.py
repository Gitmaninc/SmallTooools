#!/usr/bin/env python3
# .zip .rar .tar .tgz .tar.gz .tar.bz2 .tar.bz .tar.tgz
import os
import zlib
import unrar
import shutil
import zipfile
import tarfile
import argparse
import time
import threading
from time import sleep
from itertools import chain
from unrar import rarfile


filepath = "./filepath"  #relative path
thread_num = 1

class BaseTool(object):
    def __init__(self):
        super(BaseTool, self).__init__()
        self.compress = [".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz",".zip",".rar"]

    def run_threads(self, threads_number: int, target_function: any, *args, **kwargs) -> None:
        """ Run function across specified number of threads
        :param int thread_number: number of threads that should be executed
        :param func target_function: function that should be executed accross specified number of threads
        :param any args: args passed to target_function
        :param any kwargs: kwargs passed to target function
        :return None
        """

        threads = []
        threads_running = threading.Event()
        threads_running.set()

        for thread_id in range(int(threads_number)):
            thread = threading.Thread(
                target=target_function,
                args=chain((threads_running,), args),
                kwargs=kwargs,
                name="thread-{}".format(thread_id),
            )
            threads.append(thread)

            # print("{} thread is starting...".format(thread.name))
            thread.start()

        start = time.time()
        try:
            while thread.isAlive():
                thread.join(1)

        except KeyboardInterrupt:
            threads_running.clear()

        for thread in threads:
            thread.join()
            # print("{} thread is terminated.".format(thread.name))

        print("Elapsed time: {} seconds".format(time.time() - start))

    def iszip(self,  file):
        for z in self.compress:
            if file.endswith(z):
                return z

    def zip_to_path(self, file):
        for i in self.compress:
            file = file.replace(i,"")
        return file

    def error_record(self, info):
        with open("error.txt","a+") as w:
            w.write(info+"\n")

    def remove(self, filepath):
        if os.path.exists(self.zip_to_path(filepath)) and os.path.exists(filepath):
            os.remove(filepath)

    def un_zip(self, src, dst):
        """ src : aa/asdf.zip
            dst : unzip/aa/asdf.zip
        """
        try:
            zip_file = zipfile.ZipFile(src)
            uz_path = self.zip_to_path(dst)
            if not os.path.exists(uz_path):
                os.makedirs(uz_path)
            for name in zip_file.namelist():
                zip_file.extract(name, uz_path)
            zip_file.close()
        except zipfile.BadZipfile:
            pass
        except RuntimeError:
            self.error_record("pass required : "+src)
            return "PassRequired"
        except zlib.error:
            print("zlib error : "+src)
            self.error_record("zlib error : "+src)
        except Exception as e:
            print(e)
            self.error_record(str(e)+src)  

    def un_rar(self, src, dst):
        try:
            rar = unrar.rarfile.RarFile(src)
            uz_path = self.zip_to_path(dst)
            rar.extractall(uz_path)
        except unrar.rarfile.BadRarFile:
            pass
        except Exception as e:
            print(e)
            self.error_record(str(e)+src)    

    def un_tar(self, src, dst):
        try:
            tar = tarfile.open(src)
            uz_path = self.zip_to_path(dst)
            tar.extractall(path = uz_path)
        except tarfile.ReadError:
            pass
        except Exception as e:
            print(e)
            self.error_record(str(e)+src)


class LockedIterator(object):
    def __init__(self, it):
        self.lock = threading.Lock()
        self.it = it.__iter__()

    def __iter__(self):
        return self

    def next(self):
        self.lock.acquire()
        try:
            item = next(self.it)

            if type(item) is tuple:
                return (item[0].strip(), item[1].strip(), item[2].strip())
            elif type(item) is str:
                return item.strip()

            return item
        finally:
            self.lock.release()


class UnZip(BaseTool):
    """ UnZip files """
    def __init__(self, path):
        super(UnZip, self).__init__()
        self.path = path
        self.threads = thread_num
        self.output = "./unzip/"
        self.current_path = os.getcwd()+"/"
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-v","--verbose", action="store_true", help="./zipperpro.py -v")
        self.args = self.parser.parse_args()

    def run(self):
        self.main_unzip(self.path)

    def recursive_unzip(self, repath):
        """recursive unzip file
        """
        task_list = []
        for (root, dirs, files) in os.walk(repath):
            for filename in files:
                filename = filename.strip("./")
                src = os.path.join("./"+root,filename)
                data = (src, src, "child")
                task_list.append(data)
        data = LockedIterator(chain(task_list))
        print("[+] child unzip ...")
        self.run_threads(self.threads, self.do_unzip, data)
                
    def main_unzip(self, mainpath):
        task_list = []
        print("Initialization......")
        for (root, dirs, files) in os.walk(mainpath):
            for filename in files:
                zippath = os.path.join(self.output,root)
                if not os.path.exists(zippath):
                    os.makedirs(zippath)
                src = os.path.join(root,filename)
                dst = os.path.join(self.output,root,filename)
                if not os.path.exists(self.zip_to_path(dst)):
                    data = ((src, dst, "main"))
                    task_list.append(data)
        data = LockedIterator(chain(task_list))
        print("[+] main unzip ...")
        self.run_threads(self.threads, self.do_unzip, data)
        self.recursive_unzip(self.output+self.path)

    def do_unzip(self, running, data):
        while running.is_set():
            try:
                (src, dst, flag) = data.next()
                if flag == "main":
                    if self.iszip(src) == ".zip":
                        if self.args.verbose:
                            print("[+] main unzip : "+src)
                        self.un_zip(src,dst)
                    elif self.iszip(src) == ".rar":
                        if self.args.verbose:
                            print("[+] main unrar : "+src)
                        self.un_rar(src,dst)
                    elif self.iszip(src) in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz"):
                        if self.args.verbose:
                            print("[+] main untar : "+src)
                        self.un_tar(src,dst)
                    else:
                        try:
                            shutil.copyfile(src,dst)
                        except OSError as e:
                            print(str(e))
                            self.error_record(str(e))
                elif flag == "child":
                    if self.iszip(src) == ".zip":
                        if self.args.verbose:
                            print("[+] child unzip: "+src)
                        if not self.un_zip(src, src) == "PassRequired":
                            self.remove(src)
                            self.recursive_unzip(self.zip_to_path(src))
                        sleep(0.1)
                    elif self.iszip(src) == ".rar":
                        if self.args.verbose:
                            print("[+] child unrar : "+src)
                        self.un_rar(src,src) 
                        self.remove(src)
                        self.recursive_unzip(self.zip_to_path(src))
                        sleep(0.1)
                    elif self.iszip(src) in (".tar.gz",".tar.bz2",".tar.bz",".tar.tgz",".tar",".tgz"):
                        if self.args.verbose:
                            print("[+] child untar : "+src)
                        self.un_tar(src,src)
                        self.remove(src)
                        self.recursive_unzip(self.zip_to_path(src))
                        sleep(0.1)
                    
            except StopIteration:
                break


def main():
    z = UnZip(filepath) 
    z.run()
    


if __name__ == '__main__':
    main()