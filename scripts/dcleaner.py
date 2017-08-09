#!/usr/bin/env python3
# Author = Thamme Gowda tg@isi.edu
# Date = August 9th, 2017
# Title = Dictionary Cleaner
# Description =
#        This script has a dictionary cleaning pipeline.
#        Note: You have to setup your rules in get_rules() function


# TODO: Do spelling correction of english words using edit distance (for glosbe)

from argparse import ArgumentParser
from codecs import open as copen
import sys
import re
import string
import unicodedata


# Ascii punctuations
ascii_puncts = set(string.punctuation) - set('\'.,')
# Unicode Punctuations
unicode_puncts = {ch for ch in map(chr, range(sys.maxunicode)) if unicodedata.category(ch).startswith('P')}

# exclude apostrophe - it has special meaning

unicode_puncts -= set("',-፣")    # do not mark these as bad characters from OCR
OCR_gibber = unicode_puncts | set(range(9))

unicode_puncts |= set(",")  # remove any left over comma at the end
unicode_punct_tab = {i: None for i in map(ord, unicode_puncts)}
normalize_punct_tab = {ord('`'): '\'', ord('’'): '\''}

stop_words = {'be', 'get'}

# Cleaning functions START
#  args:
#    foreign_word : unicode string
#    eng_word : unicode string
# returns:
#   list of (f_word, e_word)
#    List can have any number of records, it shall ne empty  when the record needs to be dropped
#

def small_parenthesis(f, e):
    """
    Drops small words (length <= 2) that is inside a parenthesis.
     This is usually a part of speech like (n), (v).
    :param f:
    :param e:
    :return:
    """
    f_ = re.sub(r'\s*\([^\\)]{,2}\)', '', f)
    e_ = re.sub(r'\s*\([^\\)]{,2}\)', '', e)
    if f_ != f or e_ != e:
        print(">Remove POS: %s -> %s \t %s -> %s" % (f, f_, e, e_))
    return [(f_, e_)] if f_ and e_ else []



def normalize_puncts(f, e, t_table=normalize_punct_tab):
    """
    Translates advanced punctuations with simple punctuations.
    For example: back quote --> apostrophe : ` --> '
    :param f:
    :param e:
    :param t_table:
    :return:
    """
    return [(f.translate(t_table), e.translate(t_table))]


def ocr_gibberish_clean(f, e, bad_chars=OCR_gibber):
    """
    Drops any record that contains gibberish characters
    :param f:
    :param e:
    :param bad_chars:
    :return:
    """
    if set(f) & bad_chars or set(e) & bad_chars:
        print(">OCR GIBBERISH:", f, e)
        return []
    return [(f, e)]


def comma_swap(f, e):
    """
    Swaps two words separated by comma, then removes stop words.
    For example: 'away, get' -> 'get away' -> away
    :param f:
    :param e:
    :return:
    """
    if ',' in e:
        parts = e.split(',')
        if len(parts) == 2:
            print(">SWAP_COMMA:", e)
            e = '%s %s' % (parts[1], parts[0])
            e = ' '.join(filter(lambda x: x not in stop_words, e.split()))
    return [(f, e)] if f and e else []


def comma_synonyms(f, e):
    """
    Expands comma separated words as synonyms.
    For example: ('house, home') -> ('house'), ('home')
    :param f:
    :param e:
    :return:
    """
    if ',' in e:
        parts = list(filter(lambda x: x, map(lambda x: x.strip(), e.split(','))))
        if len(parts) > 1:
            print(">COMMA_SYNS", f, e, '-->', parts)
            return [(f, p) for p in parts]
    return [(f, e)]


def abbreviations_expand(f, e):
    """
    Expands abbreviation as synonyms
    :param f:
    :param e:
    :return:
    """
    matched = re.match(r'(.+)\(([a-zA-Z0-9\\. ]+)\)', f)
    if matched:
        print(">Splitting %s into %s" % (f, matched.groups()))
        return [(grp, e) for grp in filter(lambda x: x, matched.groups())]
    else:
        return [(f, e)]


def parenthesis_inner_drop(f, e):
    """
    Removes inner word in parenthesis.
    For example: 'take off (slowly)' -> 'take off'
    :param f:
    :param e:
    :return:
    """
    matched = re.match(r'(.+)\([a-zA-Z0-9\\. ]+\)(.*)', f)
    if matched:
        print(">Splitting %s into %s" % (f, matched.groups()))
        e = ' '.join(filter(lambda x: x, matched.groups()))
    return [(f, e)]


def remove_puncts(f, e, t_table=unicode_punct_tab):
    """
    Removes all punctuations
    :param f:
    :param e:
    :return:
    """
    f, e = f.translate(t_table), e.translate(t_table)
    return [(f, e)] if f and e else []

# Cleaning Functions END

pre_mappers = [lambda k, v: [(k.strip(), v.strip())],    # white space remover
               small_parenthesis, normalize_puncts]
post_mappers = [remove_puncts]
rules_cache = {}


def get_rules(tag):
    if tag in rules_cache:
        return rules_cache[tag]

    rules = []
    rules.extend(pre_mappers)
    if 'OCR' in tag:
        rules.append(ocr_gibberish_clean)
    if 'tg-ebookOCR' in tag:
        rules.append(comma_swap)
        rules.append(comma_synonyms)

    if 'tg-glosbe-eng_il5' == tag:
        rules.append(comma_synonyms)
    if 'rpi-ne-il6_eng' == tag:
        rules.append(parenthesis_inner_drop)
    if 'il6' in tag:
        rules.append(abbreviations_expand)

    rules.extend(post_mappers)
    rules_cache[tag] = rules
    return rules


# transformation pipeline, where mappers can produce zero or more records
def transform(tag, fgn_word, eng_word, mappers, i=0):
    if i >= len(mappers):
        yield (tag, fgn_word, eng_word)
    else:
        for fw, ew in mappers[i](fgn_word, eng_word):
            yield from transform(tag, fw, ew, mappers, i+1)


def cleanup(src_file):
    with copen(src_file, 'r', encoding='utf-8') as inp:
        for line in inp:
            tag, fgn_word, eng_word = line.split('\t')
            rules = get_rules(tag)
            yield from transform(tag, fgn_word, eng_word, rules)


def dump_stream(recs, out=None):
    opened = False
    if out is None:
        out = sys.stdout
    elif type(out) is str:
        out = copen(out, 'w', encoding='utf-8')
        opened = True
    for rec in recs:
        out.write("%s\t%s\t%s\n" % rec)
    if opened:
        out.close()


if __name__ == '__main__':
    parser = ArgumentParser(description='Dictionary Cleaner')
    parser.add_argument('-i', '--in', help='Input CSV file', required=True)
    parser.add_argument('-o', '--out', help='Output TSV File. Default=STDOUT', required=False)
    args = vars(parser.parse_args())
    recs = cleanup(args['in'])
    dump_stream(recs, args['out'])
