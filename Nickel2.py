from nltk import pos_tag
from nltk.corpus import cmudict
from nltk.corpus import wordnet as wn
import csv
from PyDictionary import PyDictionary
dictionary=PyDictionary()
import random

def find_semantic_similarity2(word1, word2, lch_threshold):
    results = []
    for net1 in wn.synsets(word1):
        for net2 in wn.synsets(word2):
            try:
                lch = net1.lch_similarity(net2)
                if lch >= lch_threshold:
                    results.append(lch)
            except:
                continue
    if results:
        return max(results)
    return 0

cmu = cmudict.dict()
def findincmu(word):
    if word in cmu.keys():
        return cmu[word]

def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)
    if len(s2) == 0:
        return len(s1)
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[
                             j + 1] + 1  # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1  # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1]

def find_closest(word, pos_list):
    b = cmu[word]
    for k in cmu.keys():
        a = cmu[k]
        for l1 in a:
            for l2 in b:
                if levenshtein(l1, l2) <= 1:
                    print(k)
                    (word, tag) = pos_tag([k])[0]
                    print(tag)
                    if tag in pos_list:
                        return k
    return None

def find_match(word):
    if word not in cmu.keys():
        return None
    (w, tag) = pos_tag([word])[0]
    print(tag)
    adj = ["JJ", "JJR", "JJS"]
    noun = ["NN", "NNS"]
    if tag in noun:
        pos_list = adj
    elif tag in adj:
        pos_list = noun
    else: return None
    match = find_closest(word, pos_list)
    print(match)

#find_match("bizarre")
#print(findincmu("bazaar"))
#print(findincmu("bizarre"))
#print(pos_tag(["green"]))
#print(find_closest("picture", ["NN", "NNS"]))
pos_dict = dict()

subtlex = csv.reader(open("subtlexcsv.csv"), delimiter=',')
def getpos(word):
    for row in subtlex:
        if row[0] == word:
            return row[9]
    return None

for row in subtlex:
    pos_dict[row[0]] = row[9].lower()

def findamatch(word):
    if word not in cmu.keys():
        return None
    if "noun" == pos_dict[word]:
        desired_pos = "adjective"
    elif "adjective" == pos_dict[word]:
        desired_pos = "noun"
    else:
        return None
    return findclosest2(word, desired_pos)

def findclosest2(word, desired_pos):
    b = cmu[word]
    for k in cmu.keys():
        a = cmu[k]
        for l1 in a:
            for l2 in b:
                if levenshtein(l1, l2) <= 1:
                    if k in pos_dict.keys():
                        if pos_dict[k] == desired_pos:
                            return k
    return None

def syn(word):
 #   good_syns = []
 #   for w in dictionary.synonym(word):
 #       if find_semantic_similarity2(word, w, 0) > 0:
  #          good_syns.append(w)
    return random.choice(dictionary.synonym(word))

def joke(word):
    try:
        homophone = findamatch(word) #finds a homophone for the original word
        hsyn = syn(homophone) #finds a synonym for the homophone
        osyn=syn(word) #finds a synonym for the original word
        str = "What do you call a"
        str2 = "? A"
        vowels = "aeiou"
        if "noun" == pos_dict[word]:
            if hsyn[0] in vowels:
                str += "n"
            if homophone[0] in vowels:
                str2 += "n"
            return  str + " " + hsyn + " " + osyn + str2 + " " + homophone+" "+word+"!"
        elif "adjective" == pos_dict[word]:
            if osyn[0] in vowels:
                str += "n"
            if word[0] in vowels:
                str2 += "n"
            return str + " "+ osyn + " " + hsyn + str2+ " " + word + " " + homophone + "!"
        else:
            return None
    except Exception: #if any errors occur and it cannot create a joke, return None
        return None


def get_joke(words):
    for w in words:
        j = joke(w)
        if j:
            return j
    return None


#def main():
 #   print(joke("table"))

#if __name__ == "__main__":
 #   main()
#What if we went to the Trottier Helpdesk to figure out how to get rid of the warning?

