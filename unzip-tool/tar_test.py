import tarfile
import os
def untar(fname, dirs):
    t = tarfile.open(fname)
    t.extractall(path = dirs) 

if __name__ == "__main__":
    untar("aaa.tar.bz2", "./unzip")


# .tar.gz
# .tar.tgz
# .tar.bz
# .tar.bz2
# .tgz
# .tar