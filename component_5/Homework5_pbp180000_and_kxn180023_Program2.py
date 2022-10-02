# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 13:27:48 2022

@author: Prachi
"""
#import libraries
import nltk
from nltk import word_tokenize
import sys
import pathlib 
import pickle
from nltk.util import ngrams
import math
import pandas as pd


#create the probability function and enter as arguments the document being tested,
#and the unigram/bigram dictionaries, with v being the length of the vocab size
def probability(test, unidict, bidict, v):
    
    #get unigrams and bigrams of test document and set laplace variable
    unigrams_test = word_tokenize(test)
    bigrams_test = list(ngrams(unigrams_test, 2)) 
    p_laplace = 1   
    
    #get total laplace probability from each bigram and return the probability 
    for bigram in bigrams_test:
        b = bidict[bigram] if bigram in bidict else 0
        u = unidict[bigram[0]] if bigram[0] in unidict else 0
        p_laplace = p_laplace * ((b+1)/(u+v))
        
    return p_laplace
 
#getfile function to get the data from file
def getfile(filepath):
    with open(pathlib.Path.cwd().joinpath(filepath), 'r',  encoding='utf-8') as f:
        text = f.read()
    return text      

if  __name__ == '__main__':
    #check for correct number of inputs
    if (len(sys.argv) < 2):
        print('Please input a filename as a system arg')
    else:
        #load in the pickled dictionaries
        EnglishUni = pickle.load(open('EngUnigram.p', 'rb'))
        EnglishBi = pickle.load(open('EngBigram.p', 'rb'))

        FrenchUni = pickle.load(open('FrenchUnigram.p', 'rb'))
        FrenchBi = pickle.load(open('FrenchBigram.p', 'rb'))
    
        ItalianUni = pickle.load(open('ItalianUnigram.p', 'rb'))
        ItalianBi = pickle.load(open('ItalianBigram.p', 'rb'))
        
        #set the v value to the length of all 3 unigram dictionaries combined
        v = len(EnglishUni) + len(FrenchUni) + len(ItalianUni)
        
        #get filepath and file for the test and solution documents
        fptest = sys.argv[1]
        fpsolution = sys.argv[2]
        test = getfile(fptest)
        solution = getfile(fpsolution)
        
        #seperate file by each line
        test = test.split("\n")        
        solution = solution.split("\n")
        #split solution file into list of lists so we can access both line number and solution
        for i in range(len(solution)):
            solution[i] = solution[i].split(" ")
        
        #create the prediction list
        prediction = []
        for t in test:
            #get the probability of the test line being English, French, or Italian
            engProb = probability(t,EnglishUni, EnglishBi,v)
            frenchProb = probability(t,FrenchUni, FrenchBi,v)
            italianProb = probability(t,ItalianUni, ItalianBi,v)
            
            #whichever probability has the highest value, append that language as
            #the predicted value for that line
            if engProb >= frenchProb and engProb >= italianProb:
                prediction.append("English")
            elif frenchProb >= engProb and frenchProb >= italianProb:
                prediction.append("French")
            elif italianProb >= frenchProb and italianProb >= engProb:
                prediction.append("Italian")
        
        #write predictions to sol.txt
        fpsolutions = open(r'sol.txt', 'w')
        with open(r'sol.txt', 'w'):
            for item in prediction:
                fpsolutions.write("%s\n" % item)
        fpsolutions.close()
        
        #get accuracy
        sumacc = 0
        incorrect = []
        length = len(prediction)
        
        for i in range(length-1):
            #check if prediction and solution are same, if so then add 1 to the total
            #accuracy
            if prediction[i] == solution[i][1]:
                sumacc += 1
            #if not then add the line number to the list of incorrect predictions.
            else:
                incorrect.append(solution[i][0])
        accuracy = sumacc/length
        
        #print out the accuracy and incorrect line numbers
        print("Accuracy is %5f" % accuracy)
        print("Incorrect Line Numbers:")
        print(incorrect)
        