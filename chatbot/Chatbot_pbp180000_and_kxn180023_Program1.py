import spacy
from spacy import displacy
import itertools
from spacytextblob.spacytextblob import SpacyTextBlob
import requests
from bs4 import BeautifulSoup
import json
import pickle
import os

confidence_weights = {
    'no_name': {
        'getRecipe': 0,
        'opinion': 0,
        'name': 0.15,
    },
    'gather_opinions': {
        'getRecipe': 0,
        'opinion': 0.05,
        'name': 0
    },
    'ready': {
        'getRecipe': 0,
        'opinion': 0,
        'name': 0
    }
}

user_model = {
    'name': '',
    'opinions': dict(),
}

bot_name = 'Alice'
nlp = spacy.load('en_core_web_lg')
nlp.add_pipe('spacytextblob')

verb_dobj_combinations = {
    'getRecipe': [
        ['_any'],
        ['serve', 'make', 'use', 'cook', 'eat', 'try', 'tell', 'show'],
        ['food', 'recipe']
    ],
    'opinion': [
        ['_any'],
        ['like', 'love', 'dislike', 'hate', 'yes', 'no', 'enjoy', 'disgusted', 'want'],
        ['_any']
    ],
    'name': [
        ['name', '_any'],
        ['call', 'is', '_any'],
        ['_any']
    ]
} # Continue adding
bye_words = ['bye', 'goodbye', 'exit']

def product(*args, **kwds):
    # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
    # product(range(2), repeat=3) --> 000 001 010 011 100 101 110 111
    pools = map(tuple, args) * kwds.get('repeat', 1)
    result = [[]]
    for pool in pools:
        result = [x+[y] for x in result for y in pool]
    for prod in result:
        yield tuple(prod)

def get_recipes(ingredients, noningredients):
    

    print('Searching for a recipe with ' + str(ingredients) + ' and without ' + str(noningredients) + '.')

    root_url = 'https://cosylab.iiitd.edu.in'
    url = 'https://cosylab.iiitd.edu.in/recipedb/search_recipe'
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    form_data = {
        'autocomplete_ingredient': ', '.join(ingredients),
        'autocomplete_noningredient': ', '.join(noningredients),
        'page': 0
    }
    res = requests.post(url, data=form_data, headers=headers).text
    soup = BeautifulSoup(res, features='html.parser')
    
    table = soup.find('table', {'id': 'myTable'})
    if table:
        rows = table.find_all('tr')
        recipes = []
        for row in rows:
            link = row.find('a', href=True)
            if link:
                recipes.append({
                    'name': ' '.join(link.text.replace('\n', '').split()), 
                    'href': root_url + link['href']
                })
    else:
        print("Hmm, I can't find what you're looking for, I'll try widening my search.")
        if len(ingredients) > len(noningredients):
            ingredients.pop()
        else:
            noningredients.pop()
        return get_recipes(ingredients, noningredients)
        
    return recipes

def load_user(name):
    if os.path.exists(name + '.pickle'):
        with open(name + '.pickle', 'rb') as infile:
            user_model['name'] = name
            user_model['opinions'] = pickle.load(infile)
    print(user_model)

def save_user():
    if user_model['name']:
        with open(user_model['name'] + '.pickle', 'wb') as fout:
            pickle.dump(user_model['opinions'], fout)

def converse():

    last_state = 'none'
    state = 'no_name'

    message = ''
    while message != 'exit':
        if last_state == 'none' and state == 'no_name':
            print('Hello, my name is ' + bot_name + '! What\'s your name?')
        elif state == 'no_name':
            print('What\'s your name?')
        elif state == 'gather_opinions':
            print('Tell me about the ingredients you like, or don\'t like, in your food.')
        elif state == 'ready':
            print('I think I\'ve got enough here. Feel free to keep telling me your ingredient opinions, but I\'m ready to find some recipes. Just ask!')

        message = input('> ')

        doc = nlp(message)

        if message.lower() in bye_words: # Improve on
            return ("bye", 1)
        
        sentences = list(doc.sents)
        if len(sentences) == 0:
            return ("err", 0)
        if len(sentences) > 1:
            return ("err", 0)

        verb = sentences[0].root
        subj = ''
        obj = ''

        for child in verb.children:
            if child.dep_ == 'nsubj':
                subj = child
            elif child.dep_ == 'dobj':
                obj = child
        
        if not obj:
            for child in verb.children:
                if child.dep_ == 'attr':
                    obj = child

        shortened_sent = ' '.join([subj.text if subj else '', verb.text if verb else '', obj.text if obj else ''])

        if shortened_sent.isspace():
            print("Sorry, I couldn't make heads or tails of that.")
            return ("err", 0)

        shortened_sent = nlp(shortened_sent)
        similarityVector = dict()
        for intention in verb_dobj_combinations:
            similarityVector[intention] = 0
            combinations = list(itertools.product(*(verb_dobj_combinations[intention])))
            for combination in combinations:
                combination = list(combination)
                similarity = 0
                if combination[0] == '_any' and combination[2] == '_any':
                    similarity = shortened_sent.similarity(nlp(combination[1]))
                elif combination[0] == '_any':
                    similarity = shortened_sent.similarity(nlp(' '.join(combination[1:2])))
                elif combination[2] == '_any':
                    similarity = shortened_sent.similarity(nlp(' '.join(combination[0:1])))
                else:
                    similarity = shortened_sent.similarity(nlp(' '.join(combination)))
                similarityVector[intention] = max(similarityVector[intention], similarity)

        # Weight confidence based on expected next intention
        for key in similarityVector:
            similarityVector[key] += confidence_weights[state][key]

        # Select intention with highest confidence
        intention = max(similarityVector, key=similarityVector.get)

        if similarityVector[intention] < 0.1:
            print('Sorry, I\'m not sure I understood.')
            continue

        if intention == 'bye':
            print('Goodbye!')
            return

        elif intention == 'name':
            proper_nouns = []
            included_bot_name = False
            for token in doc:
                # sentiment will be applied to all nouns
                if token.pos_ == 'PROPN':
                    if token.text.lower() == bot_name.lower():
                        included_bot_name = True
                    else:
                        proper_nouns.append(token.text)

            name = ""
            if len(proper_nouns) == 0:
                if included_bot_name:
                    name = bot_name
                else:
                    print('Sorry, I\'m not sure what you want me to call you.')
                    continue
            elif len(proper_nouns) > 1:
                print('Sorry, which of the following would you like me to use? ' + str(proper_nouns))
                continue
            name = proper_nouns[0]
            print('Okay, I\'ll call you ' + name + ' from now on.')
            save_user()
            load_user(name)
            user_model['name'] = name
            if state == 'no_name':
                last_state = 'no_name'
                state = 'gather_opinions'

        elif intention == 'getRecipe':
            if state == 'no_name':
                print('At least introduce yourself first.')
            elif state == 'gather_opinions':
                print('Hmm... I don\'t have enough details on what you like yet.')
            elif state == 'ready':
                print('Let me take a look...')
                ingredients = [key for key in user_model['opinions'].keys() if user_model['opinions'][key] > 0]
                noningredients = [key for key in user_model['opinions'].keys() if user_model['opinions'][key] < 0]
                recipes = get_recipes(ingredients, noningredients)
                print('I\'ve found some recipes you might like!')
                for recipe in recipes[0:4]:
                    print('This one is called ' + recipe['name'] + '. You can find the instructions to make it here: ' + recipe['href'])
                
                print('Thanks for talking to me! Goodbye!')
                return
            

        elif intention == 'opinion':
            # Use sentiment analysis to tell if it's a good or bad opinion, then update user model
            polarity = doc._.blob.polarity
            for token in doc:
                # sentiment will be applied to all nouns
                if token.pos_ == 'NOUN':
                    if token.text in user_model['opinions']:
                        user_model['opinions'][token.text] += polarity
                    else:
                        user_model['opinions'][token.text] = polarity

            if polarity < 0:
                print('Okay, I\'ll avoid those for now.')
            elif polarity > 0:
                print('I\'ll make sure to find recipes with that.')
            else:
                print('Hmm... I can\'t tell if you like that or not. Try using stronger language.')
            if state == 'gather_opinions' and len(user_model['opinions']) > 2:
                last_state = 'gather_opinions'
                state = 'ready'
        

if __name__ == '__main__':
    converse()
    save_user()
