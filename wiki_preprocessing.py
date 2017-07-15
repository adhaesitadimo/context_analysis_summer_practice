import six
from nltk.corpus import stopwords
from gensim.corpora import WikiCorpus
from pymystem3 import Mystem

m = Mystem()
stop_words = stopwords.words('russian')
stop_words.extend([u'что', u'это', u'так', u'вот', u'быть', u'как', u'в', u'к', u'на', u'который'])

with open('wiki_rus_stem.txt', 'w') as outp:
    i = 0
    wiki = WikiCorpus('ruwiki-20170520-pages-articles.xml.bz2')
    print('corpus created')
    for text in wiki.get_texts():
        i = i + 1
        lem_list = []
        if six.PY3:
            lem = b' '.join(text).decode('utf-8')
            lem_list = m.lemmatize(lem)
            outp.write(b' '.join(lem_list))
            outp.write(u'\r\n')
        else:
            lem = " ".join(text)
            lem_list = m.lemmatize(lem)
            outp.write(" ".join(lem_list))
            outp.write(u"\r\n")
        if i % 1000 == 0:
            print("Saved " + str(i) + " articles")
print("Finished. Saved " + str(i) + " articles")