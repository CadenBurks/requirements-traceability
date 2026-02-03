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
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Given requirements are read from the file
with open("./text_files/requirements-3nfr-60fr.txt", "r") as file:
    data = file.readlines()

# Requirements are cleaned and stored in a dictionary to prepare for pre-processing
info = {}
for line in data:
    parts = line.split(":", 1)
    parts[0] = parts[0].replace("(Operational)", "")
    parts[0] = parts[0].replace("(Usability)", "")
    parts[0] = parts[0].replace("(Security)", "")
    parts[0] = parts[0].strip()

    if len(parts) > 1:
        parts[1] = parts[1].rstrip("\n")
        parts[1] = parts[1].strip()
        info[parts[0]] = parts[1]

"""
PRE-PROCESSING
The 1st of the 3 variants will only use preprocessing
"""
def variant1(info: dict):
    result = {}
    text_list = []
    for id, text in info.items():
        result[id] = word_tokenize(text)
    for key in result:
        text_list.append(" ".join(result[key]))
    return text_list

def if_idf_cosine(info, variant_function, threshold):
    preprocessed = variant_function(info)
    vectorizer = TfidfVectorizer()

    matrix = vectorizer.fit_transform(preprocessed)

    similarity = cosine_similarity(matrix)
    print(similarity)

if_idf_cosine(info, variant1, 0)