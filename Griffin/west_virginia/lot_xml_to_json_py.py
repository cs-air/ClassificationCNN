from xmljson import parker, Parker
from xmljson import yahoo
from xml.etree.ElementTree import fromstring
from json import dumps,loads
import pprint as pp
import sys


def xmltojson(file_name,out_file=None):
    fp = open(file_name,'r')

    xmldata = fp.read()

    jsond = dumps(yahoo.data(fromstring(xmldata)))

    jsond = loads(jsond)

    spaces = jsond['parking']['space']

    if not out_file is None:
        f = open(out_file,'w')
        f.write(dumps(spaces,indent=4, separators=(',', ': ')))
        f.close()

    for space in spaces:
        print(space['contour'])
        for point in space['contour']['point']:
            print(point)

if __name__=='__main__':
    usage = "USAGE: python lot_xml_to_json.py input.xml output.json"
    if len(sys.argv) < 3:
        print(usage)
        sys.exit()
    xmltojson(sys.argv[1],sys.argv[2])
