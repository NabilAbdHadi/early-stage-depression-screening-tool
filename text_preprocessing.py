#import malaya as my
from malaya import spell, preprocessing, normalize, stem, pos
import string
import re
import dataframe as df
import pandas as pd
import re
import glob
import nltk
from nltk.corpus import stopwords
from googletrans import Translator
class text_preprocessing:
    """ initialize all models of malaya """
    def __init__(self):
        self.corrector = spell.probability()
        self.preprocessing = preprocessing.preprocessing()
        self.normalizing = normalize.normalizer(self.corrector)
        self.stemming = stem.deep_model()
        self.posModule = pos.transformer(model = 'albert')

        try:
            nltk.download('stopwords')
        except:
            pass

        self.translator = Translator()
        self.stopword = stopwords.words('indonesian')
        self.SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")    #convert superscript to script
        self.punctuation = string.punctuation

    

    """ basic of text preprocessing techniques """

    def word_frequency(self, text):
        wordlist = self.remove_punctuation(text).split()
        word_freq = []
        for w in wordlist:
            if w not in word_freq:  
                word_freq.append([w, wordlist.count(w)])
        return word_freq

    def tokenization(self, text):
        token =  list(text.split(" "))
        return [a for a in token if len(a) > 0]

    def remove_stopwords(self, mylist):
        return [word for word in mylist if word not in self.stopword]

    def remove_punctuation(self,text):
        return text.translate(str.maketrans(' ', ' ', self.punctuation))

    def malay_translator(self, text):
        try:
            return self.translator.translate(text, src='en', dest='ms').text
        except:
            pass
    
    def my_translator(self, mylist):
        return [self.malay_translator(word) for word in mylist]



    """ simplify the malaya Normalize Module """

    def preprocessor(self, text):
        p = " ".join(self.preprocessing.process(text))
        op = re.sub(r"<[a-z]+>|</[a-z]+>","",p)
        return op

    def my_preprocessor(self,text):
        return [self.preprocessor(t) for t in text.split(" ")]

    def normalizer(self, text):
        return self.normalizing.normalize(text)['normalize']
    
    def my_normalizer(self, textArray):
        text = self.remove_punctuation(textArray)
        text = " ".join(text)
        return self.normalizer(text)

    def stemmer(self, text):
        return self.stemming.stem(text)

    def my_stemmer(self, mylist):
        return [self.stemmer(str(word)) for word in mylist]

    def pos_tagging(self, text):
        return self.posModule.predict(text)

    def my_posTagger(self,text):
        pos = []
        for t in self.pos_tagging(text):
            pos.append(t[1])
            
        return pos
            


    """ build functions using the combination of the malaya Normalize Modules or/and basic of text analysis"""


    def data_preparation(self, text):
        
        normal = self.normalizer(str(text).translate(self.SUP))
        preprocess = self.preprocessor(normal)
        non_punct = self.remove_punctuation(preprocess.lower())
        #pos = self.my_posTagger(non_punct)
        token = self.tokenization(non_punct)
        stemmed_word = self.my_stemmer(token)
        return stemmed_word

    
import database       

""" initialize database as my_db  and text analysis as my_ta"""



def sentences_segmentation(text):
    sentence = re.sub("\n","",text)
    sentences = sentence.split(".")
    return [s for s in sentences if s != None or s == " "]

def export2CSV(sentences, csvFile = "raw_sentences.csv", column=['Text']):
    df = pd.DataFrame(sentences,columns=column)
    df.to_csv(csvFile)

def access_database(folders):
    all_sentences = []
    for f in folders:
        my_table = mydb.fetchALL(table=f, attribute="text")
        for t in my_table:
            all_sentences += sentences_segmentation(t[0])
    return all_sentences

def main():   

    """ import text file """

    #folders = ['confession_saya','iium_confession', 'um_confession']
    #sentences = access_database(folders)
     
    """ export the csv """
    #export2CSV(sentences)
    
    """ text preprocessing step  """
    raw_sentences = pd.read_csv("Data Training.csv", usecols=["raw text", "category"])
    clean_sentences = []
    for s in raw_sentences.values:
        c = my_ta.data_preparation(s[0]) 
        #print(tuple(zip(c,p)))
        clean_sentences.append([s[0],c,s[1]])
        
    

    """ export the csv """
    #export2CSV(clean_sentences,csvFile="preprocessed.csv",column=['raw text','token text', 'category'])
    


    

if __name__ == '__main__':
    mydb = database.FYP_MySQL()
    my_ta = text_preprocessing()
    main()
    