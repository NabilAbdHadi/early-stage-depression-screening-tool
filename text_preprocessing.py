#import malaya as my
import json
from malaya import spell, preprocessing, normalize, stem, pos
import string
import re
import pandas as pd
import re
import database   

class TEXT_PREPROCESSING:
    """ initialize all models of malaya """
    def __init__(self):
        self.corrector = spell.probability()
        self.preprocessing = preprocessing.preprocessing()
        self.normalizing = normalize.normalizer(self.corrector)
        self.stemming = stem.sastrawi()
        self.stopword = open('modified stopword list.txt', 'r').read().split('\n')
        self.SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")    #convert superscript to script
        self.punctuation = string.punctuation

    """ basic of text preprocessing techniques """

    def tokenization(self, text):
        token =  list(text.split(" "))
        return [a for a in token if len(a) > 0]

    def selective_stopwords_removal(self, mylist):
        return [word for word in mylist if word not in self.stopword]

    def remove_punctuation(self,text):
        return re.sub(r'[^\w\s]', ' ', text) #text.translate(str.maketrans(' ', ' ', self.punctuation))

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

    """ 
    build functions using the combination of the malaya 
    Normalize Modules or/and basic of text analysis
    """

    def data_preparation(self, text):
        
        normal = self.normalizer(str(text).translate(self.SUP))
        preprocess = self.preprocessor(normal)
        non_punct = self.remove_punctuation(preprocess.lower())        
        token = self.tokenization(non_punct)
        no_stopword = self.selective_stopwords_removal(token)
        stemmed_word = self.my_stemmer(no_stopword)
        return stemmed_word


def export2CSV(sentences, csvFile = "Dataset/raw_sentences.csv", column=['Text']):
    df = pd.DataFrame(sentences,columns=column)
    df.to_csv(csvFile)

def export2JSON(text_dict):
    with open('Dataset/Data Training.json', encoding='utf8', mode='w') as json_file:
        json.dump(text_dict,json_file)

def export2Database(sql, record):
    db = database.FYP_MySQL()
    db.execute(sql,record)

def main():   
    my_ta = TEXT_PREPROCESSING()
    
    """ text preprocessing step  """
    raw_sentences = pd.read_csv("Data Training.csv", usecols=["raw text", "category"])
    
    """ Sql statement """
    sql_insert = """
                INSERT IGNORE INTO data_training 
                (`id`,`text`,`preprocessed`,`category`) 
                VALUES (%s, %s, %s, %s)
                """
    index = 0
    for s in raw_sentences.values:
        p = " ".join(my_ta.data_preparation(s[0]))
        if p != None or p != " ":
            export2Database(sql_insert, (index, s[0], p, s[1]))
            index +=1
        
def symptomPreprocessing():
    """
    data preparation for multiclass
    """
    my_ta = TEXT_PREPROCESSING()
    data = pd.read_csv('Symptom.csv')
    """
    0 : raw text
    1 : dep -   depressed mood
    2 : int - loss of interest/pleasure
    3 : wac - change in weight/appetite
    4 : cis - change in sleep - insomnia/hypersomnia
    5 : par - psychomotor agitation/retardation
    6 : fat - fatigue or loass of energy
    7 : gui - feeling guilt/worthless
    8 : con - concentration problem
    9 : sui - suicidal thought
    """
    sql_insert = """
                INSERT IGNORE INTO symptom 
                (`id`,`text`,`preprocessed`,`dep`,`int`,`wac`,`cis`,`par`,`fat`,`gui`,`con`,`sui`) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
    index = 0
    for s in data.values:
        record = [index, s[0].lower()," ".join(my_ta.data_preparation(s[0]))]+list(s[1:])
        export2Database(sql_insert, tuple(record))
        index+=1

if __name__ == '__main__':
    """ initialize database as my_db  and text analysis as my_ta"""
    main()
    #riskFactorPreprocessing()
    #symptomPreprocessing()
    #ta = TEXT_PREPROCESSING()
    #print(ta.data_preparation("Dia sering memarahi anak2 terutama anak no"))
    