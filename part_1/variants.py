"""
Docstring for requirements_part1
I used the nltk library for preprocessing using Python 3.11.0:
    pip install nltk
    python
    import nltk
    nltk.download('punkt')
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('punkt_tab')
    nltk.download('averaged_perceptron_tagger_eng')

I used scikit-learn for tf-idf and cosine calculation:
    pip install scikit-learn

Websites/Documents used:
- https://www.nltk.org/howto.html
- https://www.nltk.org/api/nltk.tag.pos_tag.html
- https://www.nltk.org/api/nltk.stem.wordnet.html#nltk.stem.wordnet.WordNetLemmatizer
- https://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python

"""
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag


def get_wordnet_pos(tag):
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    return wordnet.NOUN

"""
PRE-PROCESSING
The 1st of the 3 variants will only use tokenization
"""
def variant1(info: dict):
    result = {}
    key_list = []
    text_list = []

    for id, text in info.items():
        result[id] = word_tokenize(text)
    
    for key in result:
        key_list.append(key)
        text_list.append(" ".join(result[key]))
    
    return key_list, text_list

"""
PRE-PROCESSING
The 2nd of the 3 variants will use tokenization and remove stop words
"""
def variant2(info: dict):
    result = {}
    key_list = []
    text_list = []
    stop_words = set(stopwords.words("english"))

    for id, text in info.items():
        tokenized = word_tokenize(text.lower())
        result[id] = [word for word in tokenized if word not in stop_words]
    
    for key in result:
        key_list.append(key)
        text_list.append(" ".join(result[key]))
    
    return key_list, text_list

"""
PRE-PROCESSING
The 3rd of the 3 variants will use tokenization, remove stop words and punctuation, and lemmatizes based on Parts-of-Speech tags
"""
def variant3(info: dict):
    result = {}
    key_list = []
    text_list = []

    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    for id, text in info.items():
        tokens = word_tokenize(text.lower())
        tagged = pos_tag(tokens)

        lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) 
                      for word, tag in tagged if word.isalpha() 
                      and word not in stop_words]

        result[id] = lemmatized

    for key in result:
        key_list.append(key)
        text_list.append(" ".join(result[key]))

    return key_list, text_list
