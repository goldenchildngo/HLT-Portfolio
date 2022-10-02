# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 13:05:55 2022

@author: Prachi
"""

#import libraries
import nltk
from nltk import word_tokenize
import sys
import pathlib 
import pickle
from nltk.util import ngrams

#create model function
def makemodel(filepath):
    #get raw text from file
    raw_text = ''
    with open(pathlib.Path.cwd().joinpath(filepath), 'r', encoding='utf-8') as f:
        raw_text = f.read().replace('\n', ' ')
        
    #get the tokens, bigrams, and unigrams from the text
    tokens = word_tokenize(raw_text)
    unigrams = list(ngrams(tokens, 1))
    bigrams = list(ngrams(tokens, 2))
    
    #create a unigram and bigram dictionary and return it
    unigram_dictionary = {tok:unigrams.count(tok) for tok in set(unigrams)}
    bigram_dictionary = {tok:bigrams.count(tok) for tok in set(bigrams)}
    
    return unigram_dictionary, bigram_dictionary




if  __name__ == '__main__':
    #check for proper amount of inputs
    if (len(sys.argv) < 2):
        print('Please input a filename as a system arg')
    else:
        #get the filepaths for each file
        fpEng = sys.argv[1]
        fpFrench = sys.argv[2]
        fpItalian = sys.argv[3]
        
        #get the unigram and bigram dictionary for each language, put the filepath
        #as input
        Eng_uni, Eng_bi = makemodel(fpEng)
        French_uni, French_bi = makemodel(fpFrench)
        Italian_uni, Italian_bi = makemodel(fpItalian)
        
        # save dictionary to pickle file
        pickle.dump(Eng_uni, open('EngUnigram.p', 'wb'))
        pickle.dump(Eng_bi, open('EngBigram.p', 'wb'))
        
        
        pickle.dump(French_uni, open('FrenchUnigram.p', 'wb'))
        pickle.dump(French_bi, open('FrenchBigram.p', 'wb'))
        
        pickle.dump(Italian_uni, open('ItalianUnigram.p', 'wb'))
        pickle.dump(Italian_bi, open('ItalianBigram.p', 'wb'))
        