"""
Functions:
- open sources
- open word list
- count occurrence of words
- write to txt

RegEx Informationen:

- Einfaches Wort = \bAktien\b
- Wort nach Satzzeichen Gross = ([\.\:\?\!]\s)\bWord\b
- Nomen ohne Bindestrich = [^-]\bAktien\b

"""

import re
import codecs

# Resources Infiles
wordlist_file = "./source/wordlist.txt"
wwf_file = "./source/wwf_korpus.txt"
info_file = "./source/infobrief_korpus.txt"

# Output
wwf_result = "./result/wwf_result.txt"
info_result = "./result/info_result.txt"


def annika_search(wordlist, source, result):
    """
    Function takes three arguments as target files
    wordlist is the formatted word list including the word type
    source is the source to be read and searched through
    result is the result file that will be written by this program
    """

    with codecs.open(wordlist, encoding='utf-8') as fp:
        words = fp.readlines()
        words = [t.strip('\n').split(";") for t in words]

    with codecs.open(source, encoding='utf-8') as source_text:
        full_text = source_text.read()

    with codecs.open(result, "ab", encoding='utf-8') as resultfile:
        resultfile.write("WORT,WORTART,NOMEN,VERB_ADJEKTIV,VA INTERPUNKTION" + "\n")
        for word in words:
            found_noun = 0
            found_verb_adj = 0
            found_verb_adj_cap = 0

            if word[1] == 'N':
                # find exact noun without - before, capitalizing the word
                regex_noun = re.compile(r'[^-]\b%s\b' % word[0].title(), re.UNICODE)
                list_noun = re.findall(regex_noun, full_text)
                found_noun = len(list_noun)

            else:
                # find verb of adjective as a word
                regex_verb_adj = re.compile(r'\b%s\b' % word[0], re.UNICODE)
                list_verb_adj = re.findall(regex_verb_adj, full_text)
                found_verb_adj = len(list_verb_adj)

                # find Verbs due to capitalization after punctuaction
                regex_verb_adj_cap = re.compile(r'([\.\:\?\!]\s)\b%s\b' % word[0].title(), re.UNICODE)
                list_verb_adj_cap = re.findall(regex_verb_adj_cap, full_text)
                found_verb_adj_cap = len(list_verb_adj_cap)
            # write to file
            resultfile.write(word[0] + "," + word[1] + "," + str(found_noun) + "," + str(found_verb_adj) + "," + str(found_verb_adj_cap) + "\n")

annika_search(wordlist=wordlist_file, source=wwf_file, result=wwf_result)
annika_search(wordlist=wordlist_file, source=info_file, result=info_result)
