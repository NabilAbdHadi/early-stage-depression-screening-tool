import requests
from bs4 import BeautifulSoup
import codecs

class web_extractor:
    
    

    """ function to extract title and content from the website  """
    def extractorCS(url,  w_title = 'entry-title', w_content ='entry-content'):       # this default is from "confession saya" website
        """ 1. find page """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        """ 2. find content """                                                           # whole content
        title = soup.find('h1', class_=w_title).text                                          # title
        contents = [text.text for text in soup.find('div', class_=w_content).select('p')]     # content
        content = "\n\n".join(contents[:-2])                                                         # convert content from list to large string
        return title, content


    def extractorIIUM(url):       # this default is from "confession saya" website
        """ 1. find page """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        """ 2. find content """                                                           # whole content
        title = soup.find('h1', class_="page-title").text               #title
        content = soup.find(id="pryc-wp-acctp-original-content").text      # content
        return title, content
    

    """ save into text file """
    def save2textfile(folder,title,content):
        file = codecs.open("E://StudyAtUM//Sem 9//FYP 2//"+folder+"//"+str(title.replace(" ","_"))+".txt", "w+", "utf-8")
        file.write(content)   # might need to remove the range
        file.close()


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
        'https://iiumc.com/kesungguhan-dan-kemurungan/'
    ]


    """ execution code """
    for url in urls_cs:
        t,c = web_extractor.extractorCS(url)
        web_extractor.save2textfile("confession saya", t,c)

    for url in url_iium:
        t,c = web_extractor.extractorIIUM(url)
        web_extractor.save2textfile("IIUM Confession", t,c)

if __name__ == "__main__":
    t,c = web_extractor.extractorIIUM("https://iiumc.com/depression-with-suicidal-thoughts/")
    web_extractor.save2textfile("IIUM Confession", t,c)