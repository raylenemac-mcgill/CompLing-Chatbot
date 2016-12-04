
import re
import nltk
import punlist
import random
from nltk.corpus import wordnet as wn
import Nickel2
import random

MASTER_LIST = []
for l in punlist.pundict.values():
    for joke in l:
        if joke not in punlist.notrandompuns:
            MASTER_LIST.append(joke)


GREETING_KEYWORDS = ("hello", "hi", "hey", "yo")

GREETING_RESPONSES = ["Don't you mean heaveno?", "Are you?", "I'm not a cow, I don't eat hay",
                      "Yo, gurt day! I love dairy ^_^"] #extend if we feel like it

FAREWELL_RESPONSES = ["GOOD DAY.","I don't believe in capitalism. Nothing is ever a 'good buy'.",
                      "Have a nice day! :)", "I'll miss you ;)", "I'm just a piece of technology to you... something"
                                                                 "something Best Bye... I'm done making puns."]
PROMPTS = ["What's your favourite animal?", "How are you today?", "What's your favourite colour?",
           "What are you wearing? ;)", "What's on your mind?", "Give me a suggestion for a joke.",
           "What do you love?", "What do you fear?", "Tell me about your day."]
def main():
    print("Hello, my name is Penny but my friends call me 'Punny'. I hope my jokes make cents. If you don't want to "
          "talk to me anymore, just say 'goodbye'!")
    first = True
    while(True):
        if first:
            user_input_punctuation = input("enter a phrase: ").lower()
        else:
            user_input_punctuation = input(random.choice(PROMPTS)).lower()
        output = "Penny: "
        first = False
        user_input = re.sub(r'[!\.?\',#&();:"$]', " ", user_input_punctuation)
        if user_input == "goodbye":
            rand = random.randrange(0, len(FAREWELL_RESPONSES))
            print(FAREWELL_RESPONSES[rand])                     # continue asking for input until the input is "goodbye"
            exit(0)
        else:
            words = user_input.split()
            words_punctuation = user_input_punctuation.split()
            pun = keyword_puns(words)
            if pun:
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

def closest_word(word1, list):pass

def find_the_pos(words):
    tsents = nltk.pos_tag(words)
    return tsents


def get_nouns(tags):
    nouns = []
    for (word, tag) in tags:
        if tag == "NN" or tag == "NNS": #for nns, take singular
            nouns.append(word)
    return nouns

def keyword_puns(words):
    tags = find_the_pos(words)
    nouns = get_nouns(tags)
    for n in nouns:                                                         # find nouns that are keys in pun dictionary
        if n in punlist.pundict.keys():
            rand = random.randrange(0, len(punlist.pundict[n]))
            return punlist.pundict[n][rand]                                                                 # return pun
    thresh = 0
    best_key = ""
    for n in nouns:
        for key2 in punlist.pundict.keys():         # find nouns that are semantically similar to keys in pun dictionary
            curr_thresh = Nickel2.find_semantic_similarity2(n, key2, 2.7)
            if curr_thresh > thresh:
                thresh = curr_thresh
                best_key = key2
    if best_key == "" : return None
    else:
        rand = random.randrange(0, len(punlist.pundict[best_key]))
        return punlist.pundict[best_key][rand]                                                              # return pun

def check_for_greeting(words):
    """If any of the words in the user's input was a greeting, return a greeting response"""
    for w in words:
        if w in GREETING_KEYWORDS:
            return GREETING_RESPONSES[GREETING_KEYWORDS.index(w)]
    return None

def check_for_clothes(words):
    clothing_type = ["clothes", "pants", "shirt", "jacket", "sweater", "shoes", "jewelry"]
    for w in words:
        for c in clothing_type:
            if Nickel2.find_semantic_similarity2(w, c, 2.7):
                return "take off your " + w + " ;)"
    return None

def check_for_ego(words_punctuation):
    for i, w in enumerate(words_punctuation):
        if w == "i'm":
            return "No I'M " + " ".join(words_punctuation[i+1:])
        elif w == "i":
            return "No I " + " ".join(words_punctuation[i+1:])


main()





