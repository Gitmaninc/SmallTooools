import os
from unrar import rarfile

def un_rar(file):
    rar = rarfile.RarFile(file)
    rar.extractall(os.path.splitext(file)[0])

un_rar("aaaax.rar")