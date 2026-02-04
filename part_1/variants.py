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

I used scikit-learn for tf-idf and cosine calculation:
    pip install scikit-learn
"""
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer


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