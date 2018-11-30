#coding:utf-8
''' resort logfile by time
    Split the file into several pieces
    Merge multiple files endswith .txt
'''

import re
import time
import os, sys
import argparse

def time_stamp(item):
    tm = time.strptime(item, '%d/%b/%Y:%H:%M:%S')
    timeStamp = int(time.mktime(tm))
    return timeStamp

def log_sort(i):
    """ resorted the log by time
    """
    o = "output.txt"
    fp = open(i, "r")
    fw = open(o, "w")
    cont = fp.readlines()
    new_list = sorted(cont, key=lambda i:int(time_stamp(re.findall(r"\d+/\w+/\d+:\d+:\d+:\d+",i)[0])))
    for line in new_list:
        fw.write(line)    
    fp.close()
    fw.close()


def file_separation(source_file): 
    ''' separation the file
        params:
            source_file = "log.txt"
            sepnum = 200000
    ''' 
    target_dir = './'  
    flag = 0  
    name = 1  
    dataList = []  
    sepnum = 200000
    with open(source_file,'r') as f_source:  
        for line in f_source:  
            flag+=1  
            dataList.append(line)  
            if flag == sepnum:  
                tmp_file_name = "tmp_"+str(name)+".txt"
                print(tmp_file_name)
                with open(target_dir+tmp_file_name,'w+') as f_target:  
                    for data in dataList:  
                        f_target.write(data)  
                name+=1  
                flag = 0  
                dataList = []        
    tmp_file_name = "tmp_"+str(name)+".txt" 
    print(tmp_file_name)
    with open(target_dir+tmp_file_name,'w+') as f_target:  
        for data in dataList:  
            f_target.write(data)  


def file_merge(tofile):
    ''' merge files 
        tmp_1.txt tmp_2.txt -> fin.txt
    '''
    fromdir = "./"
    readsize = 1024
    output = open(tofile, "wb")
    parts  = [file for file in os.listdir(fromdir) if file.endswith('.txt')]
    for filename in parts:
        filepath = os.path.join(fromdir, filename)
        fileobj  = open(filepath, "rb")
        while 1:
            filebytes = fileobj.read(readsize)
            if not filebytes: break
            output.write(filebytes)
    fileobj.close()
    output.close()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--sort", help="resort log file [-s sourcefile]")
    parser.add_argument("-c", "--sep", help="separation file [-c sourcefile]")
    parser.add_argument("-m", "--merg", help="merge files [-m outfile]")
    args = parser.parse_args()
    if args.sort:
        log_sort(args.sort)
    elif args.sep:
        file_separation(args.sep)
    elif args.merg:
        file_merge(args.merg)


if __name__ == '__main__':
    main()
