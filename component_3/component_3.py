import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import random
import sys

def guessing_game(word):
    print('Lets play a word guessing game!')
    word = [c for c in word]
    partial_word = ['_' for c in word]
    guessed_dict = set()
    score = 5
    guess = ''
    while score >=0 and not guess == '!':
        print('Score = ' + str(score) + ': ' + ' '.join(partial_word))
        guess = input('>')
        if not len(guess) == 1:
            print('Invalid guess')
            continue
        guess = guess[0]
        if guess in guessed_dict:
            print("Already guessed '" + guess + "'")
            continue
        guessed_dict.add(guess)
        if guess in word:
            for idx, c in enumerate(word):
                if c == guess:
                    partial_word[idx] = c
            score += 1
            print('Right!')
            if word == partial_word:
                print('You win!')
                return
        else:
            score -= 1
            print('Sorry, guess again')
    
    print('Sorry, you lose. The word was: ' + ''.join(word))



def preprocess(tokens):
    #tokens = [t.lower() for t in tokens] # lowercase all tokens
    tokens = [t.lower() for t in tokens if t.isalpha() and t not in stopwords.words('english') and len(t) > 5] # remove stopwords and punctuation 
    wnl = WordNetLemmatizer()
    lemmas = [wnl.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))
    tagged_lemmas = nltk.pos_tag(lemmas_unique)
    nouns = [t for t, pos in tagged_lemmas if pos == 'NN']
    print("Number of tokens: " + str(len(tokens)) + " Number of nouns: " + str(len(nouns)))
    return tokens, nouns

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("No data path specified.")
    
    with open(sys.argv[1], 'r') as file:
        text = file.read()
        
        # tokenize
        tokens = word_tokenize(text)

        # lexical diversity
        print("Lexical diversity: %.2f" % (len(set(tokens)) / len(tokens)))

        # preprocessing
        tokens, nouns = preprocess(tokens)
        
        # make a count dictionary
        counts = {t:tokens.count(t) for t in nouns}
        most_common_words = list(reversed(sorted(counts, key=counts.get)))[:50]
        guessing_game(random.choice(most_common_words))