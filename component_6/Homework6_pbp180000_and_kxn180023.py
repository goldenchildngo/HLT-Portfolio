import urllib
import math
import pickle
from urllib import request
from bs4 import BeautifulSoup
from nltk import word_tokenize
from nltk import sent_tokenize
from nltk.corpus import stopwords

# returns all urls found on a given webpage
def crawl(url, search, domain):
    html = request.urlopen(url).read().decode('utf8-sig') if url.endswith('.txt') else request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, features="html.parser")
    urls = []
    for link in soup.find_all('a'):
        link_str = link.get('href')
        if link_str and search.lower() in link_str.lower():
            if link_str.startswith('/url?q='):
                link_str = link_str[7:]
                print('MOD:', link_str)
            if '&' in link_str:
                i = link_str.find('&')
                link_str = link_str[:i]
            if link_str.startswith('http') and domain not in link_str:
                urls += [link.get('href')]
        
    return urls

# scrapes and returns text from a webpage
def scrape(url):
    try:
        html = request.urlopen(url).read().decode('utf8')# if url.endswith('.txt') else request.urlopen(url).read().decode('utf8')
        soup = BeautifulSoup(html, features="html.parser")

        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out

        # extract text
        text = []
        for paragraph in soup:
            text += [paragraph.get_text()]
        text = " ".join(text)

        return text
    except:
        return ""

# read cleaned txt files only
def read_cleaned_text(url):
    fname = url_to_fname(url) + '.clean'
    with open(fname, 'r', encoding='utf-8') as file:
        text = file.read()
        return text

# generate important terms sorted by tf-idf
def get_important_terms(document_urls):
    tf_dict = {}
    idf_dict = {}
    total_length = 0

    # tf
    for url in document_urls:
        document = read_cleaned_text(url)
        swords = stopwords.words('english')
        tokens = [t.lower() for t in word_tokenize(document) if t.isalpha() and t.lower() not in swords]
        for t in tokens:
            if t in tf_dict:
                tf_dict[t] += 1
            else:
                tf_dict[t] = 1
        
        total_length = total_length + len(tokens)

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / total_length

    # idf
    for url in document_urls:
        document = read_cleaned_text(url)
        swords = stopwords.words('english')
        tokens = [t.lower() for t in word_tokenize(document) if t.isalpha() and t.lower() not in swords]
        
        for t in set(tokens):
            if t in idf_dict:
                idf_dict[t] += 1
            else:
                idf_dict[t] = 1
        
    # normalize idf
    for t in idf_dict.keys():
        idf_dict[t] = math.log((len(document_urls) + 1) / (idf_dict[t] + 1))

    # tf-idf
    tf_idf = {}
    for t in tf_dict.keys():
        tf_idf[t] = tf_dict[t] * idf_dict[t]

    # sort by tf-idf and store first 30
    key_terms = list(reversed(sorted(tf_idf.items(), key=lambda kv:(kv[1],kv[0]))))[:30]
    return key_terms

# clean and remove whitespace from files and puts every sentence in a new line in a new clean textfile
def clean_text_file(fname):
    with open(fname, 'r', encoding='utf-8') as file:
        text = file.read()
        text = text.replace('\n', ' ')
        text = text.replace('\t', ' ')
        sentences = sent_tokenize(text)
        
        fname = fname + '.clean'
        with open(fname, 'w', encoding='utf-8') as file:
            for sentence in sentences:
                file.write(sentence + '\n')

# converts url to file name
def url_to_fname(url):
    url = url.replace(':', '_')
    url = url.replace('/', '_')
    url = url.replace('?', '_')
    url += ".txt"
    return url

# for every url, scrape text and save to new file
def scrape_all_to_file(urls):
    saved_urls = []
    for url in urls:
        fname = url_to_fname(url)
        text = scrape(url)
        if text:
            with open(fname, 'w', encoding='utf8') as file:
                file.write(text)
                saved_urls += [url]
    return saved_urls
        

if __name__ == '__main__':
    start_url = 'https://en.wikipedia.org/wiki/Halloween'
    start_text = scrape(start_url)
    urls = crawl(start_url, 'halloween', 'wikipedia')[:50]
    
    # print('Found ' + str(len(urls)) + ' urls')

    urls = scrape_all_to_file(urls)

    # print('Scraped ' + str(len(urls)))

    for url in urls:
        clean_text_file(url_to_fname(url))

    important_terms = get_important_terms(urls)

    #for term in important_terms:
    #    print(term)

    # build searchable knowledge base of facts from manually selected terms
    topTen = ['samhain', 'costumes', 'festival', 'halloween', 'illustration', 'church', 'saints', 'crafts', 'disney', 'pagan']

    finallist = []
    for val in important_terms:
        if val[0] in topTen:
            finallist.append(val)
        
    # make dictionary documents (url) -> sentences in document
    documents = []
    for url in urls:
        documents += [(url, sent_tokenize(read_cleaned_text(url)))]
    documents = dict(documents)


    knowledge_base = {}

    for val in finallist:
        word = val[0]
        for url in urls:
            sentences = documents[url]
            for sentence in sentences:
                if word in sentence.lower():
                    if word in knowledge_base:
                        knowledge_base[word] += [sentence]
                    else:
                        knowledge_base[word] = [sentence]
    
    # print('costumes: ')
    # for sentence in knowledge_base['costumes'][:5]:
    #     print('\t' + sentence)

    pickle.dump(knowledge_base, open('dictTopTen.p', 'wb'))