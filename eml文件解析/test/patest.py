import datetime
import json
import eml_parser
from eml_parser import eml_parser

def json_serial(obj):
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial

def emlParser(eml):
    with open(eml, "rb") as fhdl:
        raw_email = fhdl.read()

    parsed_eml = eml_parser.decode_email_b(raw_email)
    # parsed_eml = eml_parser.get_raw_body_text(raw_email)
    # print(parsed_eml["header"]["subject"])
    # print(parsed_eml["header"]["header"]["to"])
    # print(parsed_eml["attachment"][0]["hash"]["md5"])
    print(parsed_eml["header"]["header"]["received"])
    # print(json.dumps(parsed_eml, default=json_serial, indent=1))


# emlParser("2018-12-21 00.03.21.952011000.eml")
emlParser("./aa/test.eml")


# import base64

# s = "0HctgvRgA6K0wY9IE1UvLvH/qI1C7mfJ1bGDwNvk1P4=|eyJzdWJhY2NvdW50X2l\tkIjoiMCIsInRlbmFudF9pZCI6ImNvdXJzZXJhIiwiY3VzdG9tZXJfaWQiOiIxIiw\ticiI6Ijk3MDg1NzM3N0BxcS5jb20iLCJtZXNzYWdlX2lkIjoiMDAxZTljMzZhMjV\tjNWI0MDk3YWYifQ=="


# print(base64.b64decode(s))