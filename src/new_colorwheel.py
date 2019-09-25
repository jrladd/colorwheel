#! /usr/bin/env python3

# import regularize as reg
import re, glob, json
from nltk.corpus import wordnet as wn
from lxml import etree

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

def find_color_lines(line, color_lines):
    line_list = []
    words = line.findall(".//{*}w")
    for i,w in enumerate(words):
        reg = w.get("reg")
        if reg == None:
            word = w.text
        else:
            word = reg
        if word == "red":
            if words[i-1].get("pos").startswith("p") or "x" in words[i-1].get("pos") or words[i-1].get("lemma") == "have" or words[i-1].get("lemma") == "be":
                word = "read"
        line_list.append(word)
    joined_line = " ".join(line_list)

    for k,v in search_terms.items(): # Iterate through search terms, looking for any terms in a line.
        for c in v:
            if c.search(joined_line) != None:
                if k not in color_lines:
                    color_lines[k] = [c.sub("<span class='"+k+"'>"+c.search(joined_line).group(0)+"</span>", joined_line)]
                else:
                    color_lines[k].append(c.sub("<span class='"+k+"'>"+c.search(joined_line).group(0)+"</span>", joined_line))

colors = get_colors()
stop_colors = ['rose', 'buff', 'fawn', 'hazel', 'wine', 'cherry'] # A list of colors not to use.

# Create a dictionary where the keys remain the same but the values are changed to regex.
search_terms = {k: [re.compile('\\b'+c+'\\b') for c in v if c not in stop_colors] for k,v in colors.items() if k != 'olive'}

print(search_terms)

all_colors = {}
with open("../data/fq_ma.xml", 'rb') as fq:
    fqxml = etree.fromstring(fq.read())
    for book_number,book in enumerate(fqxml.findall('.//{*}div[@type="book"]')):
        color_lines = {}
        total_lines = len(book.findall(".//{*}l"))
        for line in book.findall(".//{*}l"):
            find_color_lines(line, color_lines)
        color_lines = {k: list(set(v)) for k,v in color_lines.items()}
        all_colors['<i>The Faerie Queene</i>, Book '+str(book_number+1)] = color_lines
        all_colors['<i>The Faerie Queene</i>, Book '+str(book_number+1)]["total"] = total_lines

with open("../data/sc_ma.xml", 'rb') as sc:
    scxml = etree.fromstring(sc.read())
    for i,month in enumerate(scxml.findall('.//{*}div[@type="month"]')):
        month_name = month.get("n")
        color_lines = {}
        total_lines = len(month.findall(".//{*}l"))
        for line in month.findall(".//{*}l"):
            find_color_lines(line, color_lines)
        color_lines = {k: list(set(v)) for k,v in color_lines.items()}
        all_colors['<i>The Shepheardes Calender</i>, '+str(100+i)+" "+month_name] = color_lines
        all_colors['<i>The Shepheardes Calender</i>, '+str(100+i)+" "+month_name]["total"] = total_lines
print(all_colors)



# Put master dictionary in a JSON file for use by D3 code.
with open('../docs/new_line_data.json', 'w') as outfile:
    json.dump(all_colors, outfile, sort_keys = True, indent = 4, ensure_ascii = False)
