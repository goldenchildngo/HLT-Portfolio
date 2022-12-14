# HLT-Portfolio
Portfolio for Human Language Technologies (CS 4395.001) assignments

## Assignment 0

Overview of NLP

[See document](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_0/Natural%20Language%20Processing%20Component%200.pdf)

## Assignment 1

Assignment 1 focuses on matching (probably manually entered) person data to the following format:
    first and last names must be capitalized, 
    middle initial is capitalized, use 'X' for middle initial if one is not provided
    id must consist of two letters followed by four numbers
    phone number must be in format XXX-XXX-XXXX

Assignment 1 can be executed by running python component_1.py <path_to_data>

Python is the most widely used language for text processing, which is one of the advantages to using it for text processing. It's popularity means that libraries for text processing are often written in Python, code examples for common problems are written in Python, and even this class uses Python. Python is capable of exposing C libraries to python code, allowing the developer the flexibility of a scripting language while letting fast native libraries do the heavy lifting. Unfortunately, this reliance on native libraries for large workloads can make language processing slow if a significant portion of the work is done in Python and the dataset is large.

In this assignment, I learned how to write effective comments for Python code, how to use regex in Python, and I refreshed my memory on Python syntax. I also used Pickle for the first time.

[See code](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_1/component_1.py)

## Assignment 2

Using NLTK to download and tokenize text, as well as demonstrating the differences between stemming text and lemmatizing it.

[See notebook](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_2/component_2.ipynb)

## Assignment 3

Use NLTK to process a large body of text into a set of lemmatized nouns. Find the 50 most frequent nouns, select one at random, and play a guessing game

[See notebook](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_3/component_3.ipynb)

## Assignment 4

Explore the uses and features of WordNet and SentiWordNet

[See notebook](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_4/component_4.ipynb)

## Assignment 5

Program 1 trains an n-gram model to identify what language (out of English, French, and Italian) on a given corpus of labled text and pickles it.
Program 2 unpickles the model and uses it to identify the language of unlabled sentences.

[See program files](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_5)

## Assignment 6

Program crawls all urls from a starter url and scrapes every page into files. The program then cleans the text in the files and outputs the cleaned text into new files. Finally, the program uses tf-idf to judge the importance of every word in the combined corpus. The top 30 are shown to the user as suggested key terms. The user then manually writes in the top 10 key terms. For each key term, every sentence containing that term from the corpus is added to a list. The key term and the list are then added to a dictionary that will form a knowledge base for a future chatbot. The dictionary is pickled.

[See code](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_6/Homework6_pbp180000_and_kxn180023.py)

[See report](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_6/Hmwk6_writeup_pbp180000__kxn180023.docx)

## Assignment 7

An investigation of sentence parsing methods.

[See report](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/component_7/Component_7.pdf)

## Author Attribution

Using NLP to predict the author of different works from the Federalist Papers.
[See report](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/author_attribution/author_attribution.ipynb)

## ACL Paper Summary
[See paper](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/ACL_Paper_Summary_pbp180000_and_kxn180023)

## Chatbot
[See project](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/chatbot)

## Text Classification
[See report](https://github.com/goldenchildngo/HLT-Portfolio/blob/main/text_classification_pbp180000_and_kxn180023.ipynb.pdf)