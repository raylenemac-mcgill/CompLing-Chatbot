from nltk.corpus import cmudict
import csv
from PyDictionary import PyDictionary
dictionary=PyDictionary()
import random
subtlex = csv.reader(open("subtlexcsv.csv"), delimiter=',')
cmu = cmudict.dict()

# *** this function is not our original code; it comes from a class assignment ***
def levenshtein(s1, s2): #find phonetic distance between suggested word and words in cmudict
    if len(s1) < len(s2):
        return levenshtein(s2, s1) #this is the levenshtein function from an assignment we did in class
    if len(s2) == 0: #however, it computes the distance between phonetic transcriptions, not spellings.
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


pos_dict = dict()
for row in subtlex:
    if row[1] == "FREQcount":  #prevents error of trying to convert table header to an integer
        continue
    elif int(row[1])>20:
        pos_dict[row[0]]=row[9].lower() #creates a dictionary of acceptable words (frequency of 20+) and their POS


def findamatch(word):
    if word not in cmu.keys(): #in case the word does not exist in the dictionary
        return None
    if "noun" == pos_dict[word]: #if the word is a noun,
        desired_pos = "adjective" #then we want to pair it with an adjective to make a "phrase"
    elif "adjective" == pos_dict[word]:
        desired_pos = "noun"
    else:
        return None
    return findclosest(word, desired_pos) #gets a word in CMUDict which is close phonetically

def findclosest(word, desired_pos):  #find a word in cmudict that is phonetically similar to the suggested word
    b = cmu[word] #get phonetic transcription of input word
    for k in cmu.keys(): #loop through all words in CMUDict
        a = cmu[k] #get phonetic transcription of current key
        for l1 in a: #for each transcription for the first word (CMUDict gives a list of them)
            for l2 in b:
                if levenshtein(l1, l2) <= 1: #if the lev. dist. is small enough
                    if k in pos_dict.keys(): #check if word has a subtlex FREQcount of 20+
                        if pos_dict[k] == desired_pos:  #ensure word is an adjective if suggestion was a noun, and vice versa
                            return k #return the FIRST word in CMUDict which is one phoneme away from the input word
    return None


def syn(word): #returns a synonym for a word
    good_syns = []
    for w in dictionary.synonym(word):  #generates a list of synonyms for a word, taken from dictionary.com
        for key in pos_dict.keys():
            if w == key and pos_dict[w] == pos_dict[word]: #filters synonyms to match POS of word, have a subtlex FREQcount of 20+
                good_syns.append(w)
    return random.choice(good_syns)
    #returns a random synonym from a list of acceptable synonyms

def joke(word):
    try:
        homophone = findamatch(word) #finds a homophone (differs by at most one phoneme) for the original word
        hsyn = syn(homophone) #finds a synonym for the homophone
        osyn=syn(word) #finds a synonym for the original word
        str = "What do you call a"
        str2 = "? A"
        vowels = "aeiou"
        if "noun" == pos_dict[word]: #if the input word is a noun, make a joke with the right template
            if hsyn[0] in vowels: #avoid returning a joke with 'a' + vowel
                str += "n"
            if homophone[0] in vowels: #if first letter is a vowel
                str2 += "n"
            return  str + " " + hsyn + " " + osyn + str2 + " " + homophone+" "+word+"!"
            #joke template
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


def get_joke(words):  #make a joke with the first acceptable word in input
    for w in words: #loops through the words in the input and tries to find a joke for each
        j = joke(w)
        if j:
            return j
    return None

