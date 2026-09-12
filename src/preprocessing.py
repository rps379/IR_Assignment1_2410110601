import re
from nltk import word_tokenize
from nltk.corpus import stopwords

from nltk.stem import PorterStemmer

stemmer=PorterStemmer()

stop_words = set(stopwords.words('english'))


def preprocess(text):
    text=text.lower() #convert all to lowercase

    text=re.sub(r"[^a-z0-9\s]", "", text)  #remove punctuations from text

    tokens=word_tokenize(text)  #split into tokens

    tokens=[word for word in tokens if word not in stop_words]  #remove common words

    tokens=[stemmer.stem(word) for word in tokens]  #stemm the tokens

    return tokens

if __name__ == "__main__":
    text = "Men's Cotton Crew Neck T-Shirt - Black. Made from 100% cotton!"

    result = preprocess(text)

    print(result)