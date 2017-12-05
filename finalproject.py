"""
Created on Mon Nov 27 16:10:58 2017

@author: Anna Truelove and JaBria Owens

This code assumes that both words used in the blend are real words that can
be found in the CMU dictionary"""

import nltk
from nltk.corpus import cmudict
from curses.ascii import isdigit
import pyphen # hyphenator we used, to access the hyphenator when running our 
# code, run "pip install pyphen" in the terminal.

vowels = 'aeiou'
consonants = 'bcdfghjklmnpqrstvwxyz'

d = cmudict.dict()

"""Function for determining number of syllables in a word"""
def numSyl(word):
    return max([len([y for y in x if isdigit(y[-1])]) for x in d[word.lower()]]) 
     
"""Function to hyphenate word"""
def hyphen(word):
    dic = pyphen.Pyphen(lang='en')
    return dic.inserted(word)
# example: hyphen("animation") --> an-i-ma-tion

"""Function to determine if words overlap by 2+ characters"""
def isOverlap(string1, string2):
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): 
                    answer = match
                match = ""
    if answer != "" and len(answer) > 1: #if overlap exists and has more than 1 character
        return True
    else:
        return False

"""Function to blend overlaps"""
def overlap(word1, word2):
    answer = ""
    len1, len2 = len(word1), len(word2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and word1[i + j] == word2[j]):
                match += word2[j]
            else:
                if (len(match) > len(answer)): 
                    answer = match
                match = ""
    # removes characters after overlap for word1
    segment1 = ""
    for j in range(len(word1)):
       while answer not in segment1:
           segment1 += word1[j]
           j += 1
  
    # removes characters before overlap for word2
    segment2 = ""
    for k in range(len(word2)):
       while answer not in segment2:
           segment2 += word2[k]
           k += 1
    segment2edit = word2 
    segment2edit = answer + segment2edit.replace(segment2, "")
           
    return segment1.replace(answer, "") + segment2edit


"""Function to blend when words are both 1 syllable"""
def oneSyl(word1, word2):
        # if word1 starts with CC & word2 starts with CV
        if word1[0] in consonants and word1[1] in consonants and word2[0] in consonants and word2[1] in vowels:
            return word1[:2] + word2[1:]
        
        # if word2 starts with CC & word1 starts with CV
        if word2[0] in consonants and word2[1] in consonants and word1[0] in consonants and word1[1] in vowels:
            return word2[:2] + word1[1:]
        
        # if both words start with a V
        if word1[0] in vowels and word2[0] in vowels:
            return word1[:1] + word2[1:]
        
        # if one starts with a V and the other with a C
            # V, C
        if word1[0] in vowels and word2[0] in consonants:
            return word2[:2] + word1
            # C, V
        if word2[0] in vowels and word1[0] in consonants:
            return word1[:2] + word2
        
        # if both start with CC or CV
        if word1[1] in consonants and word2[1]in consonants or word1[1] in vowels and word2[1] in vowels:
            return word1[:2] + word2[2:]
           
        return "one syl error"

"""Function to blend 1 syllable word and 2+ syllable word"""
def oneAndMore(word1, word2):
    # if word1 starts with CC & word2 starts with CV
    if word1[0] in consonants and word1[1] in consonants and word2[0] in consonants and word2[1] in vowels:
        return word1[:2] + word2[1:]
    
    # if word2 starts with CC & word1 starts with CV
    if word2[0] in consonants and word2[1] in consonants and word1[0] in consonants and word1[1] in vowels:
        return word2[:2] + word1[1:]
    
    # if both start with CC or CV
    if word1[1] in consonants and word2[1]in consonants or word1[1] in vowels and word2[1] in vowels:
        return word1[:2] + word2[2:]
    
    # if one starts with a V and the other with a C
        # V , C
    if word1[0] in vowels and word2[0] in consonants:
        return word1[:-2] + word2
        # C, V
    if word2[0] in vowels and word1[0] in consonants:
        return word1 + word2[2:]
    
    # if both words start with a V
    if word1[0] in vowels and word2[0] in vowels:
        return word1 + word2[1:]
    
    return  "one and more error"

"""Function to blend 2+ syllable words"""
def twoAndMore(word1, word2):
    count1 = 0
    count2 = 0
    finalWord1 = ''
    finalWord2 = ''
    for l in hyphen(word1):
        if l == '-':
            count1 = count1 + 1
    for l in hyphen(word2):
        if l == '-':
            count2 = count2 + 1
            
    #finalWord1 = leftmost 2 syllables
    if count1 % 2 == 0: #if odd num of syllables (even hyphen count)
        i = 0
        hypCount = 0
        while i < len(hyphen(word1)) and hypCount < 2:
            finalWord1 = finalWord1 + hyphen(word1)[i]
            if hyphen(word1)[i] == '-':
                hypCount = hypCount + 1
            i = i + 1
            
    #finalWord1 = first half of syllables
    if count1 % 2 != 0: # if even # of syllables (odd hyphen count)
        i = 0
        j = 0
        hypCount1 = 0
        hypCount2 = 0
        totalHyp = 0
        
        # gets total hyphens in word1
        for l in hyphen(word1):
            if l == '-':
                totalHyp = totalHyp + 1
                
        # if 2 syll (1 hyphen)      
        if totalHyp == 1:
            while i < len(hyphen(word1)) and hypCount1 == 0:
                finalWord1 = finalWord1 + hyphen(word1)[i]
                if hyphen(word1)[i] == '-':
                    hypCount1 = hypCount1 + 1
                i = i + 1
        # if more than 2 syll, loop and add to finalWord1 until hypCount is one less than totalHyp
        if totalHyp > 1:
            while j < len(hyphen(word1)) and hypCount2 < totalHyp:
                finalWord1 = finalWord1 + hyphen(word1)[j]
                if hyphen(word1)[j] == '-':
                    hypCount2 = hypCount2 + 1
                j = j + 1
                
    #finalWord2 = rightmost 2 (get leftmost and subtract from whole word, then take out hyphens)
    if count2 % 2 == 0: #if odd num of syllables (even hyphen count)
        i = 0
        while i < len(hyphen(word2)) and hyphen(word2)[i] != '-':
            finalWord2 = finalWord2 + hyphen(word2)[i]
            i = i + 1
        finalWord2 = hyphen(word2).replace(finalWord2, "")
    
    #finalWord2 = second half 
    if count2 % 2 != 0: # if even # of syllables (odd hyphen count)
        i = 0
        j = 0
        hypCount1 = 0
        hypCount2 = 0
        totalHyp = 0
        # gets totalHyp
        for l in hyphen(word2):
            if l == '-':
                totalHyp = totalHyp + 1
        #if 2 syll/ 1 hyphen       
        if totalHyp == 1:
            while i < len(hyphen(word2)) and hypCount1 == 0:
                finalWord2 = finalWord2 + hyphen(word2)[i]
                if hyphen(word2)[i] == '-':
                    hypCount1 = hypCount1 + 1
                i = i + 1
            finalWord2 = hyphen(word2).replace(finalWord2, "")        

        if totalHyp > 1:
            while j < len(hyphen(word2)) and hypCount2 < totalHyp:
                finalWord2 = finalWord2 + hyphen(word2)[j]
                if hyphen(word2)[j] == '-':
                    hypCount2 = hypCount2 + 1
                j = j + 1
            finalWord2 = hyphen(word2).replace(finalWord2, "")        
    
    # get rid of all hyphens still in the word
    result = finalWord1.replace('-', "") + finalWord2.replace('-', "")
    return result
    
"""MAIN FUNCTION"""

"""Function to blend 2 words together"""
def blend(word1, word2):
    blend = ""
    # if the words overlap
    if isOverlap(word1, word2):
        return  overlap(word1, word2)
    # if both words are 1 syllable
    if numSyl(word1) == 1 and numSyl(word2) == 1:
        return oneSyl(word1, word2)
    # if one syll + 2+ syll
    if numSyl(word1) == 1 and numSyl(word2) > 1 or numSyl(word2) == 1 and numSyl(word1) > 1:
        return oneAndMore(word1, word2)
    # if both greater than 1 syllable
    if numSyl(word1) > 1 and numSyl(word2) > 1:
        return twoAndMore(word1, word2)
    return blend


"""TESTS USING BLENDED WORDS CORPUS"""

""" ~Overlap Test~
If there is a common sequence of 1 or more characters that overlap"""
# In overlaps, sometimes the overlapping sequence of words falls in the middle of one or
# both words. When this happens, the remaining characters following the overlap in the first
# word and preceding the overlap in the second word must be clipped.
# example: alaska and eskimo. overlap is "sk", so 'a' in alaska is clipped and 'e' in eskimo 
# is clipped to form 'alaskimo'

"""Both are clipped"""
blend("abnormal", "enormous") # abNORMous
blend("abortion", "mortuary") # abORTuary
blend("absolute", "obsolete") # aBSOLete
blend("administration", "australia") # adminiSTRalia
blend("advertisement", "antique") # adverTIque
blend("alaska", "eskimo") # alaSKimo

"""One is clipped, the other is whole"""
blend("integral", "graph") # inteGRAph
blend("lamb", "hamburger") # lAMBurger 
blend("lock", "octagon") # lOCtagon
blend("scrap", "shrapnel") # scRAPnel
blend("adapt", "aptitude") # adAPTitude
blend("administration", "trivia") # adminisTRivia
blend("amplifier", "fire") # ampliFIre
blend("commune", "university") # comUNiversity


""" Whole parts of both words preserved"""
blend("africa", "car") # afriCAr
blend("anise", "seed") # aniSEed
blend("brat", "attitude") # brATtitude
blend("abhor", "horrible") # abHORrible
blend("alcohol", "holiday") # alcoHOLiday
blend("durable", "blend") # durablend


""" ~1 Syll Each Test~
Most one syllable words are relatively short and follow the same patterns when blended.
The resulting blended word will also be 1 syllable."""

# When one word starts with CC and another with CV, the CC will be the first part
# of the blended word.
#Formation used: The end of one word is appended to the beginning of the other """
blend("spoon", "fork") # spork
blend("fork", "spoon") # spork

blend("smoke", "fog")  # smog
blend("fog", "smoke")  # smog

blend("smack", "mash") # smash
blend("mash", "smack") # smash

blend("sheep", "goat") # shoat
blend("goat", "sheep") # shoat

blend("smoke", "haze") # smaze
blend("haze", "smoke") # smaze

blend("smell", "health") # smealth
blend("health", "smell") # smealth

# When both words start with CC, word order matters
blend("flat", "sharp") # flarp
blend("skirt", "short") # skort
blend("blow", "snort") # blort

# When both words begin with V, word order matters
# very uncommon
blend("ice", "egg") # igg

# When both words start with CV, word order matters
blend("wad", "wedge") # wadge
blend("yard", "lawn") # yawn
blend("lawn", "yard") # lard

# When one word starts with a V and the other a C
blend("smoke", "ice") # smice
blend("ice", "smoke") # smice


""" 1 syll + 2+ syll
if one word has 1 syll and the other has more than 1"""

# When one word starts with CC and another with CV, the CC will be the first part
blend("breakfast", "lunch") # brunch
blend("lunch", "breakfast")

blend("fried", "pickles") # frickles

blend("grim", "dismal") # grismal

# When both words start with CC, word order matters
blend("break", "slipper") # bripper
blend("slide", "trickle") # slickle

# When both words begin with V, word order matters
blend("air", "abrasive") # airbrasive
blend("america", "aid") # americaid

# When both words start with CV, word order matters
blend("mock", "cocktail") # mocktail
blend("lime", "lemon") # limon
blend("man", "monkey") # mankey
blend("bell", "balcony") #belcony


# When one word starts with a V and the other a C
blend("identity", "kit") # identikit
blend("man", "english") # manglish
blend("america", "cards") # americards


""" 2+ Syllables Each Test """ 
# this function was much more complex and so we did not have time to fix all 
# the bugs, but it works for the most part
blend("argue", "haggle") # argle
blend("aggravate", "annoy") # aggranoy
blend("aggravate", "provoke") # aggravoke
blend("computer", "literate") # computerate
blend("flicker", "glimmer") # flimmer
blend("hectic", "active") # hective

