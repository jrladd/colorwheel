#! /usr/bin/env python

import regularize as reg
import sys, codecs, re, glob, json
from nltk.corpus import wordnet as wn

def _recurse_all_hyponyms(synset, all_hyponyms):
    synset_hyponyms = synset.hyponyms()
    if synset_hyponyms:
        all_hyponyms += synset_hyponyms
    for hyponym in synset_hyponyms:
        _recurse_all_hyponyms(hyponym, all_hyponyms)

def all_hyponyms(synset):
    hyponyms = []
    _recurse_all_hyponyms(synset, hyponyms)
    all_words = []
    for hyponym in hyponyms:
        for lemma in hyponym.lemmas():
            all_words.append(lemma.name())
    all_words = [a.replace("_"," ") for a in all_words]
    return all_words

colors = {}
for h in wn.synset('chromatic_color.n.01').hyponyms():
    colors[h.lemmas()[0].name()] = [l.name() for l in h.lemmas()]
    colors[h.lemmas()[0].name()].extend(all_hyponyms(h)) 
for h in wn.synset('achromatic_color.n.01').hyponyms():
    colors[h.lemmas()[0].name()] = [l.name() for l in h.lemmas()]
    colors[h.lemmas()[0].name()].extend(all_hyponyms(h)) 


search_terms = {k: [re.compile('\\b'+c+'\\b') for c in v] for k,v in colors.items()}

files = glob.glob('../data/fq*.txt')

print files 

all_files = {}
for fq in files:
    color_lines = {}
    with codecs.open(fq, 'r', 'utf8') as f:
        for line in f:
            line = reg.modernize(line.strip(' \n\r'))
            line = re.sub(r'\xa0+', '', line)
            for k,v in search_terms.items():
                for c in v:
                    if c.search(line) != None:
                        if k not in color_lines:
                            color_lines[k] = [line]
                        else:
                            color_lines[k].append(line)

    color_lines = {k: list(set(v)) for k,v in color_lines.items()}
    all_files['Book '+fq[2:-4]] = color_lines

final_dict = []
for k,v in all_files.items():
    text = {}
    for key,val in v.items():
        text['text'] = k
        text['color'] = key
        text['sentences'] = val

with codecs.open('../data/colors.json', 'w', 'utf8') as outfile:
    json.dump(final_dict, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
