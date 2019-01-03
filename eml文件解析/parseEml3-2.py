#!/usr/bin/env python3
# version: 3.2

import re
import time
import email
import xlwt
import hashlib
import os,shutil
import collections
import random,string


class baseTools(object):
    def __init__(self):
        self.nowTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    def random_text(self, length=8, alph=string.ascii_letters + string.digits):
        """ Random text generator. 

        Generates random text with specified length and alphabet.
        """
        return ''.join(random.choice(alph) for _ in range(length))

    def url_regex(self, raw):
        """
        regex url
        :: return list
        """
        urls = []
        regex_two = r"((?:https?|ftp|file|\w+)(?::\/\/|\.)[\-A-Za-z0-9+&@#/%?=~_|!:,.;\*]+[\-A-Za-z0-9+&@#/%=~_|])"
        try:
            urls = re.findall(regex_two,str(raw))
        except Exception as e:
            print (e)
            pass
        return urls

    def ip_regex(self, raw):
        """
        Collect legal ip
        1.1.1.1 | 10.1.1.1 | 256.10.1.256 | 222.212.22.11 | 0.0.150.150 | 232.21.234.256
        """
        ips = []
        try:
            re_ips = re.findall(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}',str(raw))
            for ip in re_ips:
                compile_ip = re.compile(r'^((?:(?:[1-9])|(?:[1-9][0-9])|(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])))(?:\.(?:(?:[0-9])|(?:[1-9][0-9])|(?:(?:1[0-9][0-9])|(?:2[0-4][0-9])|(?:25[0-5])))){3})$')
                if compile_ip.match(ip):
                    ips.append(ip)
        except Exception as e:
            print (e)
            pass
        return ips

    def write_data_to_excel(self, total_excel_dic):
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet("Sheet1",cell_overwrite_ok=True)
        name_list=["日期","主题","发件人","收件人","链接","ip","附件名","md5"]
        for i in range(len(name_list)):
            sheet.col(i).width = (30*200)
            sheet.write(0,i,name_list[i])
            for j in range(len(total_excel_dic)):
                try:
                    sheet.write(j+1,i,total_excel_dic[j][name_list[i]])
                except TypeError as a:
                    pass
        wbk.save(self.nowTime+'.xls')

    def mv_error_file(self, eml, err):
        try:
            print(err)
            time.sleep(1)
            errors_path = "./errors"
            if not os.path.exists(errors_path):
                os.makedirs(errors_path)
            shutil.move(eml, errors_path)
        except Exception as e:
            print(e)

    def cp_error_file(self, eml, err):
        try:
            print(err)
            errors_path = "./errors"
            if not os.path.exists(errors_path):
                os.makedirs(errors_path)
            shutil.copy(eml, errors_path)
        except Exception as e:
            print(e)

    def get_md5(self, content):
        md = hashlib.md5()
        md.update(content)
        return md.hexdigest()


class emlParse(baseTools):
    def __init__(self):
        super(emlParse, self).__init__()
        
    def email_parse(self, eml):
        url_regex_tmp = []
        url_regex_list = ""
        ip_regex_list = ""
        file_name_list = ""
        file_name = []
        files_path = "./files/"
        data_md5_list = ""

        # analyse eml header
        try:
            print(eml)
            fp = open(eml, errors='ignore')
            msg = email.message_from_file(fp)  
            headers = str(msg).split('\n\n')[0]
            time_data = msg.get("Date")
            if not time_data:
            	time_data = "no time data"
            subject = msg.get("subject")
            if subject:
                subject_data = ""
                dh = email.header.decode_header(subject)
                for i in range(len(dh)):
                    if type(dh[i][0]) is str:
                        temp_data = dh[i][0]
                    else:
                        if dh[i][1]:
                            temp_data = dh[i][0].decode(dh[i][1])
                        else:
                            temp_data = dh[i][0]
                    subject_data += str(temp_data) 
                subject_data = subject_data.replace("b'","").replace("'","")      
            else:
                subject_data = "<no subject>"
        except AttributeError as e:
            subject_data = subject
        except Exception as err:
            print("[-] "+str(err))
            self.mv_error_file(eml, err)
            # self.cp_error_file(eml, err)

        # extend from & to
        try:
            from_data = email.utils.parseaddr(msg.get("from"))[1]
            to_data = email.utils.parseaddr(msg.get("to"))[1]
        except Exception as err:
            print("[-] "+str(err))
            self.mv_error_file(eml, err)
            #self.cp_error_file(eml, err)
     
        # analyse eml body
        try: 
            for par in msg.walk():
                if not par.is_multipart():
                    name = par.get_param("name")
                    if name:
                        dh = email.header.decode_header(name)
                        if type(dh[0][0]) is str:
                            fname = dh[0][0]
                        else:
                            fname = dh[0][0].decode(dh[0][1])
                        data = par.get_payload(decode=True)
                        extend_path = files_path+eml.strip(".eml")[1:100]+"/"
                        try:
                            if not os.path.exists(extend_path):
                                os.makedirs(extend_path)
                            f = open(extend_path + fname, 'wb')
                        except Exception as e:
                            print ('附件名有非法字符，自动换一个')
                            f = open(extend_path+self.nowTime+"_"+self.random_text(), 'wb')
                        data_md5 = self.get_md5(data)
                        file_name.append((fname,data_md5))
                        f.write(data)
                        f.close()
                    else:                                          
                        content = (par.get_payload(decode=True))
            for i in self.url_regex(content):
                url_regex_tmp.append(i)
            for z in set(url_regex_tmp):
                url_regex_list += z
                url_regex_list += ' | ' 
            for j in file_name:
                file_name_list += j[0]
                file_name_list += ' | '
                data_md5_list += j[1]
                data_md5_list += ' | '
            ip_regexs_tmp = self.ip_regex(headers)
            for x in set(ip_regexs_tmp[::-1]):
                ip_regex_list += x
                ip_regex_list += ' | '
            excel_dic = {
                "日期": time_data,
                "主题": subject_data,
                "发件人": from_data,
                "收件人": to_data,
                "链接":  url_regex_list.strip('| '),
                "ip": ip_regex_list.strip('| '),
                "附件名": file_name_list.strip('| '),
                "md5": data_md5_list.strip('| '),
            }
            return excel_dic
        # except AttributeError:
        #     pass
        except Exception as err:
            print("[-] "+str(err))
            self.mv_error_file(eml, err)
            #self.cp_error_file(eml, err)


def main():
    total = []
    emlfile = [eml for eml in os.listdir("./") if eml.endswith('.eml')]
    em = emlParse()
    for eml in emlfile:
        excel_dic = em.email_parse(eml)
        # print(excel_dic)
        total.append(excel_dic)
    em.write_data_to_excel(total)


if __name__ == '__main__':
    main()