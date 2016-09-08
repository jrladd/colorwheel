#! /usr/bin/env python

import regularize as reg
import sys, codecs, re, glob, json
from nltk.corpus import wordnet as wn

# Two functions for recursing down WordNet's tree of hyponyms
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

def get_colors():
    """
    Uses the two functions above to recurse through hyponyms for "chromatic color"
    and "achromatic color," yielding a dictionary with basic color terms as keys and
    a list of related terms as values.
    """
    colors = {}
    for h in wn.synset('chromatic_color.n.01').hyponyms():
        colors[h.lemmas()[0].name()] = [l.name() for l in h.lemmas()]
        colors[h.lemmas()[0].name()].extend(all_hyponyms(h)) 
    for h in wn.synset('achromatic_color.n.01').hyponyms():
        colors[h.lemmas()[0].name()] = [l.name() for l in h.lemmas()]
        colors[h.lemmas()[0].name()].extend(all_hyponyms(h)) 
    return colors

colors = get_colors()
stop_colors = ['rose', 'buff', 'fawn', 'hazel', 'wine', 'cherry'] # A list of colors not to use.

# Create a dictionary where the keys remain the same but the values are changed to regex.
search_terms = {k: [re.compile('\\b'+c+'\\b') for c in v if c not in stop_colors] for k,v in colors.items() if k != 'olive'}

files = glob.glob('../data/*.txt') # Get all files.

print files 

all_files = {}
for fq in files:
    color_lines = {}
    with codecs.open(fq, 'r', 'utf8') as f:
        for line in f:
            line = reg.modernize(line.strip(' \n\r')) # Modernize spelling in each line
            line = re.sub(r'\xa0+', '', line) # Remove pesky special character.
            for k,v in search_terms.items(): # Iterate through search terms, looking for any terms in a line.
                for c in v:
                    if c.search(line) != None:
                        if k not in color_lines:
                            color_lines[k] = [c.sub("<span class='"+k+"'>"+c.search(line).group(0)+"</span>", line)]
                        else:
                            color_lines[k].append(c.sub("<span class='"+k+"'>"+c.search(line).group(0)+"</span>", line))

    # For each Book of FQ, create a dictionary with basic color terms as keys and values of a list of lines that include that color.
    color_lines = {k: list(set(v)) for k,v in color_lines.items()}
    #color_lines['id'] = 'Book '+fq[10:-4]
    all_files['Book '+fq[10:-4]] = color_lines



# Put master dictionary in a JSON file for use by D3 code.
with codecs.open('../vis/line_data.json', 'w', 'utf8') as outfile:
    json.dump(all_files, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
