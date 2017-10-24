#!/usr/bin/env python
#encoding: utf-8

"""
A tool for extracting elements out of XML file using  XPATH

Example:
 1. For pure XML file
 $ xpath.py -f myfile.xml -x //ITEM

 2. For HTML files
 $ xpath.py -f index.html -x '//a/@href' --html

---
# author : Thamme Gowda
# License: Apache License 2.0
"""

from lxml import etree
import argparse
import sys

def xpath_eval(xml_f, xp_qry, html_mode=False):
    '''
    :param: xml_f - path to xml document
    :param: xp_qry: xpath query
    :param: html_mode: true if input is HTML file
    :returns: result of xpath query evaluation
    '''
    if html_mode:
        with open(xml_f) as f:
            doc = etree.HTML(f.read())
    else:
        doc = etree.parse(xml_f)
    res = doc.xpath(xp_qry)
    return res

def main(argv):
    parser = argparse.ArgumentParser(description='Xpath Eval Function')
    parser.add_argument('-f','--file', help='XML file', required=True)
    parser.add_argument('-x','--xpath', help='Xpath Query', required=True)
    parser.add_argument('-htm','--html', help='Input is HTML file', action="store_true", default=False)

    args = vars(parser.parse_args())
    res = xpath_eval(args['file'], args['xpath'], args['html'])
    if res:
        for r in res:
            print(r)

if __name__ == '__main__':
    main(sys.argv)
