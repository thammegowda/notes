#!/usr/bin/env python2.7
#encoding: utf-8
#author : ThammeGowda N
#Licence : Apache 2.0


import libxml2
import argparse
import sys

def xpath_eval(xml_f, xp_qry):
    '''
    :param: xml_f - path to xml document
    :param: xp_qry: xpath query
    :returns: result of xpath query evaluation
    '''
    doc = libxml2.parseFile(xml_f)
    res = doc.xpathEval2(xp_qry)
    return res

def main(argv):
    parser = argparse.ArgumentParser(description='Xpath Eval Function')
    parser.add_argument('-f','--file', help='XML file', required=True)
    parser.add_argument('-x','--xpath', help='Xpath Query', required=True)
    args = vars(parser.parse_args())
    res = xpath_eval(args['file'], args['xpath'])
    if res:
        for r in res:
            print r

if __name__ == '__main__':
    main(sys.argv)
