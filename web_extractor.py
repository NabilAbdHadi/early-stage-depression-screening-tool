import requests
from bs4 import BeautifulSoup
import codecs
import pandas as pd
from nltk.tokenize import sent_tokenize

class web_extractor:
    
    """ function to extract title and content from the website  """
    def extractorCS(url,  w_title = 'entry-title', w_content ='entry-content'):         # this default is from "confession saya" website
        """ 1. find page """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        """ 2. find content """                                                           # whole content
        title = soup.find('h1', class_=w_title).text                                          # title
        contents = [text.text for text in soup.find('div', class_=w_content).select('p')]     # content
        content = "\n\n".join(contents[:-2])                                                         # convert content from list to large string
        return title, content

    def extractorIIUM(url):                                                             # this default is from "confession saya" website
        """ 1. find page """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        """ 2. find content """                                                           # whole content
        title = soup.find('h1', class_="page-title").text               #title
        content = soup.find(id="pryc-wp-acctp-original-content").text      # content
        return title, content  
    """ export file """
    def save2textfile(folder,title,content):
        file = codecs.open("E://StudyAtUM//Sem 9//FYP 2//prototype 2//Data doc//"+folder+"//"+str(title.replace(" ","_"))+".txt", "w+", "utf-8")
        file.write(content)   # might need to remove the range
        file.close()
    
    def save2csv(data):
        df = pd.DataFrame(data,columns=['Text'])
        df.to_csv("Data doc//Dataset.csv")


def main():

    """urls for extracting content from website """
    urls_cs = [             
        'https://confessionssaya.com/kemurungan-seorang-houseman/',
        'https://confessionssaya.com/bos-jadikan-aku-monster/',
        'https://confessionssaya.com/to-be-or-not-to-be/',
        'https://confessionssaya.com/ibu-berkerjaya-mdd/'
    ]

    url_iium = [
        'https://iiumc.com/realiti-mangsa-kemurungan/',
        'https://iiumc.com/rawatan-untuk-mengatasi-perasaan-kemurungan/',
        'https://iiumc.com/stigma-kemurungan-bisa-membunuh/',
        'https://iiumc.com/depresi-dan-kemurungan/',
        'https://iiumc.com/hafal-al-quran-tetapi-ada-kemurungan/',
        'https://iiumc.com/doktor-dan-kemurungan/',
        'https://iiumc.com/tanda-tanda-penyakit-kemurungan/',
        'https://iiumc.com/kemurungan-4/',
        'https://iiumc.com/si-pemaaf-dan-kemurungan/',
        'https://iiumc.com/kemurungan-dan-rasa-cemas-yang-tidak-dapat-dikawal/',
        'https://iiumc.com/kesungguhan-dan-kemurungan/',
        "https://iiumc.com/kemurungan-kerana-kerja/"
    ]
    dataset = ""

    """ combine the contents """
    for url in urls_cs:
        t,c = web_extractor.extractorCS(url)
        dataset+= " " + c

    for url in url_iium:
        t,c = web_extractor.extractorIIUM(url)
        dataset+= " " + c

    " make sure the dataset will be in straight line "
    dataset = dataset.replace("\n", " ")
    dataset = dataset.replace("\t", " ")

    " sentences segmentation "
    textList = sent_tokenize(dataset)

    " export to csv file"
    web_extractor.save2csv(textList)

if __name__ == "__main__":
    main()