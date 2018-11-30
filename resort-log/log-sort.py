#coding:utf-8
""" resorted the log by time
"""
import re
import time

def time_stamp(item):
    tm = time.strptime(item, '%d/%b/%Y:%H:%M:%S')
    timeStamp = int(time.mktime(tm))
    return timeStamp

def main(i,o):
    fp = open(infile, "r")
    fw = open(outfile, "w")
    cont = fp.readlines()
    new_list = sorted(cont, key=lambda i:int(time_stamp(re.findall(r"\d+/\w+/\d+:\d+:\d+:\d+",i)[0])))
    for i in new_list:
        fw.write(i)    
    fp.close()
    fw.close()

if __name__ == '__main__':
    infile = "test.txt"
    outfile = "xxx.txt"
    main(infile,outfile)

