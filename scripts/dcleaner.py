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
from unicodedata import category as chtype

from autocorrect import spell  # pip install autocorrect


# Ascii punctuations
ascii_puncts = set(string.punctuation) - set('\'.,')

# Unicode Punctuations
unicode_puncts = set(filter(lambda x: chtype(x).startswith('P')
                            or chtype(x).startswith('S'),
                            map(chr, range(sys.maxunicode))))

# exclude apostrophe - it has special meaning
unicode_puncts -= set(".',-፣")   # exclude these chars / preserve them as they are
OCR_gibber = unicode_puncts | set(range(10))

unicode_puncts |= set(",")  # remove any left over comma at the end

punct_trans_tab = {i: ' ' for i in map(ord, unicode_puncts)}    # translate all of 'em to white space
punct_trans_tab.update({ord('`'): '\'', ord('’'): '\''})    # quotes

unicode_puncts = set(filter(lambda x: chtype(x).startswith('P')
                            or chtype(x).startswith('S'),
                            map(chr, range(sys.maxunicode))))

print('Total Punctuations:', len(punct_trans_tab))

def norm_puncts(text):
    text = text.translate(punct_trans_tab)
    return re.sub(r'\s+', ' ', text).strip()

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
    matched = re.match(r'(.+)\([a-zA-Z0-9\\. ]+\)(.*)', e)
    if matched:
        print(">Remove paranthesis %s into %s" % (f, matched.groups()))
        e = ' '.join(filter(lambda x: x, matched.groups()))
    return [(f, e)]


def remove_puncts(f, e):
    """
    Removes all punctuations
    :param f:
    :param e:
    :return:
    """
    f, e = norm_puncts(f), norm_puncts(e)
    return [(f, e)] if f and e else []


def no_to_be(f, e):
    """
    Removes  'to' or 'be' or both of those tokens in the beginning of phrases
    For example:
       be known -> known
       to drink -> drink
    :param f:
    :param e:
    :return:
    """
    e_ = re.sub('^(to\s)?(be\s)?', '', e)
    if e != e_:
        print('> NO_TO_BE: %s -> %s' % (e, e_))
    return [(f, e_)] if e_ else []


def ethiopic_comma_syns(f, e):
    """
    Splits foreign phrase by ethiopic comma(፣) and treats the parts as synonyms
    :param f:
    :param e:
    :return:
    """
    if '፣' in f:
        parts = list(filter(lambda x: x, map(lambda x: x.strip(), f.split('፣'))))
        print(">ETHIOPIC_SYNS:%s -> %s" % (f, parts))
        return [(p, e) for p in parts]
    else:
        return [(f, e)]


def remove_ending_punct(f, e):
    f = re.sub(r"[,\\.]+$", '', f)
    e = re.sub(r"[,\\.]+$", '', e)
    return [(f, e)]


def spellcheck(f, e):
    """
    corrects spelling of english text. Powered by autocorrect
     https://github.com/phatpiglet/autocorrect
     http://norvig.com/spell-correct.html
    :param f:
    :param e:
    :return:
    """
    e_ = " ".join(map(spell, e.split()))
    if e != e_:
        print(">Spell Correct: %s | %s -> %s" % (f, e, e_))
    return [(f, e_)]


class CorefMem(object):
    def __init__(self):
        self.index = {}  # Multi map
        self.pending = {}  # multi map

    def add_entry(self, f, e):

        if f not in self.index:
            self.index[f] = set()
        self.index[f].add(e)

    def queue(self, f1, f2):
        """
        Add to the Queue, that F2 is same as F1.
        :param f1:
        :param f2:
        :return:
        """
        if f1 not in self.pending:
            self.pending[f1] = set()
        self.pending[f1].add(f2)

    def get_all(self, tag='coref'):
        for f1, syns in self.pending.items():
            if f1 not in self.index:
                print(">COREF_ERROR: Cant resolve %s; no entry for %s" % (syns, f1))
                continue
            for f2 in syns: # all the synonyms of f1
                for e in self.index[f1]: # multiple meanings
                    yield (tag, f2, e)

cr_mem = CorefMem()


def coref_resolver(f, e, mem=cr_mem):
    """
    Resolves co references like:
      F1 -> same as F2
      F2 -> E2
    Since the results are passed as stream, it uses memory to resolve the references
    :param f:
    :param e:
    :return:
    """
    if e.startswith('same as '):
        f_ = e.replace('same as', '').strip()
        mem.queue(f_, f)
        return []
    else:
        mem.add_entry(f, e)
        return [(f, e)]


# Cleaning Functions END

pre_mappers = [lambda k, v: [(k.strip(), v.strip())],    # white space remover
               small_parenthesis]
post_mappers = [remove_puncts, no_to_be, remove_ending_punct]
rules_cache = {}


def get_rules(tag):
    """
    gets rules applicable to record
    :param tag: tag or group name of record
    :return: sequence of mappers  or rules for cleaning the record
    """
    if tag in rules_cache:
        return rules_cache[tag]

    rules = []
    rules.extend(pre_mappers)
    if 'il5' in tag:
        rules.append(ethiopic_comma_syns)

    if 'OCR' in tag:
        rules.append(ocr_gibberish_clean)
    if 'tg-ebookOCR' in tag:
        rules.append(comma_swap)
        rules.append(comma_synonyms)

    if 'tg-glosbe-eng_il5' == tag:
        rules.append(comma_synonyms)
    if 'glosbe' in tag:
        rules.append(spellcheck)
    if 'rpi-ne-il6_eng' == tag:
        rules.append(parenthesis_inner_drop)
    if 'geezexp' in tag:
        rules.append(comma_synonyms)

    if 'il6' in tag:
        rules.append(abbreviations_expand)

    rules.extend(post_mappers)
    rules.append(coref_resolver)
    rules_cache[tag] = rules
    return rules


# transformation pipeline, where mappers can produce zero or more records
def transform(tag, fgn_word, eng_word, mappers, i=0):
    """
    Transformer pipeline (uses recursion on mapper stages)
    :param tag:
    :param fgn_word:
    :param eng_word:
    :param mappers: List of mappers, analogous to stages in pipeline
    :param i: Index of stage in pipeline
    :return:
    """
    if i >= len(mappers):
        yield (tag, fgn_word, eng_word)
    else:
        for fw, ew in mappers[i](fgn_word, eng_word):
            yield from transform(tag, fw, ew, mappers, i+1)


def cleanup(src_file):
    """
    cleans a dictionary
    :param src_file: path to source file having <TAG>\t<FOREIGN_PHRASE>\t<ENGLISH_PHRASE>
    :return: generator of records
    """
    with copen(src_file, 'r', encoding='utf-8') as inp:
        for line in inp:
            tag, fgn_word, eng_word = line.split('\t')
            rules = get_rules(tag)
            yield from transform(tag, fgn_word, eng_word, rules)
        yield from cr_mem.get_all('coref-resolver')


def dump_stream(recs, out=None):
    """
    Writes records to output stream
    :param recs: stream of records
    :param out: None, string or a file stream
    :return: None
    """
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
