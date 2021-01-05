from text_classification import text_multiclassification
from text_preprocessing import text_preprocessing

text = ["Terkadang aku hiris-hiris pergelangan tangan, berbekas, berparut tapi tiada siapa yang tahu, ada pun classmate bertanya apabila ternampak lengan baju aku terselak, aku katakan tiada apa, aku beri alasan yang aku lap cermin tingkap bilik buatkan lengan calar balar",
        "Dan waktu ini pun aku masih berperang dengan diri aku sendiri, kini aku sudah berkahwin, punyai seorang anak,Waktu sarat mengandung aku pernah menggantung diri, tapi masih juga takdir aku bernafas, kerana tepat pada waktu suami aku balik dan pecahkan pintu bilik untuk selamatkan aku",
        "Keluarga aku tak tahu aku punyai depresi yang sanggup mencederakan diri, hanya suami aku sahaja mengetahuinya",
        "Pernah juga waktu aku susah tidur malam, termenung sendiri di tingkap, merenung kebawah dan terdetik â€œkalau aku terjun ni, mesti lega kepala akuâ€",
        "Sewaktu aku terdetik itulah, tiba-tiba aku dengar suara ketawa datang dari phone aku"]

sym = text_multiclassification()
tp = text_preprocessing()

for i in text:
    temp = tp.data_preparation(i)
    print(temp)
    a,b = sym.get_symptom_BoW(temp)
    print(a)