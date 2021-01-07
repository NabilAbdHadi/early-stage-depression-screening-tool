import malaya as my
import string, re

text = ["Terkadang aku hiris-hiris pergelangan tangan, berbekas, berparut tapi tiada siapa yang tahu, ada pun classmate bertanya apabila ternampak lengan baju aku terselak, aku katakan tiada apa, aku beri alasan yang aku lap cermin tingkap bilik buatkan lengan calar balar",
        "Dan waktu ini pun aku masih berperang dengan diri aku sendiri, kini aku sudah berkahwin, punyai seorang anak,Waktu sarat mengandung aku pernah menggantung diri, tapi masih juga takdir aku bernafas, kerana tepat pada waktu suami aku balik dan pecahkan pintu bilik untuk selamatkan aku",
        "Keluarga aku tak tahu aku punyai depresi yang sanggup mencederakan diri, hanya suami aku sahaja mengetahuinya",
        "Pernah juga waktu aku susah tidur malam, termenung sendiri di tingkap, merenung kebawah dan terdetik â€œkalau aku terjun ni, mesti lega kepala akuâ€",
        "Sewaktu aku terdetik itulah, tiba-tiba aku dengar suara ketawa datang dari phone aku"]

corrector =  my.spell.probability()
preprocessing = my.preprocessing.preprocessing()
normalizing = my.normalize.normalizer(corrector)
stem_deep = my.stem.deep_model()
stem_sastrawi = my.stem.sastrawi()
stopword = open('modified stopword list.txt', 'r').read().split('\n')
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹", "0123456789")    #convert superscript to script
punctuation = string.punctuation
print()
for i in text :
        i = i.lower().translate(SUP)
        t = re.sub(r'[^\w\s]', ' ', i)
        p = " ".join(preprocessing.process(t))
        s1 = stem_deep.stem(p)
        s2 = stem_sastrawi.stem(p)
        print(s1)
        print(s2)
        print()
        
