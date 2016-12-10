import re
import nltk
import punlist
from nltk.corpus import wordnet as wn
import Nickel2
import random

MASTER_LIST = []
for l in punlist.pundict.values(): #create a "master list" of puns for returning as random responses
    for joke in l:
        if joke not in punlist.notrandompuns: #eliminate puns which are not appropriate for random response
            MASTER_LIST.append(joke)


GREETING_KEYWORDS = ("hello", "hi", "hey", "yo")

GREETING_RESPONSES = ["Don't you mean heaveno?", "Are you?", "I'm not a cow, I don't eat hay",
                      "Yo, gurt day! I love dairy ^_^"]

FAREWELL_RESPONSES = ["GOOD DAY.","I don't believe in capitalism. Nothing is ever a 'good buy'.",
                      "Have a nice day! :)", "I'll miss you ;)", "I'm just a piece of technology to you... something"
                                                                 "something Best Bye... I'm done making puns."]
PROMPTS = ["What's your favourite animal? ", "How are you today? ", "What's your favourite colour? ",
           "What are you wearing? ;) ", "What's on your mind? ", "Give me a suggestion for a joke. ",
           "What do you love? ", "What do you fear? ", "Tell me about your day. "]
def main():
    print("Hello, my name is Penny but my friends call me 'Punny'. I hope my jokes make cents. If you don't want to "
          "talk to me anymore, just say 'goodbye'!")
    first = True
    while(True): #loops forever until the user enters "goodbye"
        if first:
            user_input_punctuation = input("enter a phrase: ").lower() #the first prompt is always "enter a phrase"
        else:
            user_input_punctuation = input(random.choice(PROMPTS)).lower() #after the first time we select a random prompt
        output = "Penny: "
        first = False
        user_input = re.sub(r'[!\.?\',#&();:"$]', " ", user_input_punctuation) #strip punctuation using regex
        if user_input == "goodbye":  #if the user wants to quit the program
            rand = random.randrange(0, len(FAREWELL_RESPONSES)) #return random response to goodbye and quit
            print(FAREWELL_RESPONSES[rand])
            exit(0)
        else:
            words = user_input.split()
            words_punctuation = user_input_punctuation.split()
            pun = keyword_puns(words)
            if pun: #if "pun" is not None (ie, if an appropriate pun was found)
                output += pun                                     # if a pun from punlist.py can be returned, return pun
            else:
                greeting = check_for_greeting(words)
                if greeting:
                    output += greeting                              # if a greeting is found, return a greeting response
                else:
                    j = Nickel2.get_joke(words)
                    if j:
                        output += j              # if a noun or adjective can be made into a homophone joke, return joke
                    else:
                        clothes = check_for_clothes(words)
                        if clothes:
                            output += clothes    # if a word is a type of clothing, return "take off your [clothing] ;)"
                        else:
                            ego = check_for_ego(words_punctuation)
                            if ego:
                                output += ego            # if the input contains "I" or "I'm", return "No I" or "No I'M"
                            else:
                                rand = random.randrange(0, len(MASTER_LIST))
                                output += "You’re boring me **TOPIC CHANGE** "+MASTER_LIST[rand]     # return random pun
        print(output)



def find_the_pos(words): #get a list of (word, POS_tag) pairs for every word in the input
    tsents = nltk.pos_tag(words)
    return tsents


def get_nouns(tags): #filter the input to only include words tagged as Nouns or Plural Nouns
    nouns = []
    for (word, tag) in tags:
        if tag == "NN" or tag == "NNS":
            nouns.append(word)
    return nouns


def find_semantic_similarity(word1, word2, lch_threshold): #compare lch distances between pairs of words in both synsets
    results = []
    for net1 in wn.synsets(word1): #get synset for first word
        for net2 in wn.synsets(word2): #get synset for second word
            try:
                lch = net1.lch_similarity(net2) #get lch for each pair in the two synsets
                if lch >= lch_threshold:
                    results.append(lch) #gather the lch scores above the threshold into a list
            except:
                continue
    if results:
        return max(results) #return the maximum score in the results list
    return 0 #if none pass the threshold, return 0


def keyword_puns(words):
    tags = find_the_pos(words)
    nouns = get_nouns(tags)
    for n in nouns:    # check if any nouns are actually keys in the dictionary
        if n in punlist.pundict.keys():
            rand = random.randrange(0, len(punlist.pundict[n]))
            return punlist.pundict[n][rand]    # return a random pun from the proper list
    thresh = 0 #otherwise, we start measuring semantic similarity
    best_key = ""
    for n in nouns:
        for key2 in punlist.pundict.keys(): # find nouns that are semantically similar to keys in pun dictionary
            curr_thresh = find_semantic_similarity(n, key2, 2.7)
            if curr_thresh > thresh: #if the current noun and keyword are close enough semantically,
                thresh = curr_thresh #then this is the new "best" match
                best_key = key2 #this is the new best key
    if best_key == "" : return None #if none are close enough, return None
    else: #otherwise, return a random pun from the list whose key is close semantically to a noun in the input
        rand = random.randrange(0, len(punlist.pundict[best_key]))
        return punlist.pundict[best_key][rand]    # return pun


def check_for_greeting(words):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for w in words:
        if w in GREETING_KEYWORDS:
            return GREETING_RESPONSES[GREETING_KEYWORDS.index(w)] #return the corresponding greeting (by index)
    return None


def check_for_clothes(words):
    clothing_type = ["clothes", "pants", "shirt", "jacket", "sweater", "shoes", "jewelry"]
    for w in words:
        for c in clothing_type:
            if find_semantic_similarity(w, c, 2.7): #if any word in the user input is close semantically to a clothing word
                return "take off your " + w + " ;)" #ask them to take it off
    return None


def check_for_ego(words_punctuation): #if user says "I" or "I'm", return the rest of the phrase but with "No I" or "No I'M" before
    for i, w in enumerate(words_punctuation):
        if w == "i'm":
            return "No I'M " + " ".join(words_punctuation[i+1:])
        elif w == "i":
            return "No I " + " ".join(words_punctuation[i+1:])


main()





