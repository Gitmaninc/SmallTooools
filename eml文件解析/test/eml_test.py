from email.parser import Parser
from email.header import decode_header
from email.header import Header
from email.utils import parseaddr
import email
import imaplib


def decode_str(s):
    value, charset = decode_header(s)[0]
    print(value)
    print(charset)
    if charset:
        print(type(value))
        value = value.decode("utf-8")
    return value

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos>=0:
            charset = content_type[pos + 8:].strip()
    return charset

def parseHeader(eml):
    fp = open(eml, errors='ignore')
    # msg = Parser().parsestr(fp.read()) 
    msg = email.message_from_file(fp)
    subject = msg.get("subject")
    for header in ['From', 'To', 'Subject', 'Date']:
        value = msg.get(header, '')
        if value:
            if header=='Subject':
                value = decode_str(value)
            elif header == 'Date':
                value = value
            else:
                hdr,addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
        print(value)

if __name__ == '__main__':
    parseHeader("2019-02-16 17.46.32.193447000.eml")