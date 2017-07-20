import codecs
import nltk
import os
import re
from nltk.corpus import stopwords
from pymystem3 import Mystem


# set stem settings
m = Mystem()
stop_words = stopwords.words('russian')
stop_words.extend([u'что', u'это', u'так', u'вот', u'быть', u'как', u'в', u'к', u'на', u'который'])


with open('lurkmore_stem.txt', 'w') as outp:
    i = 0
    directory = '/home/dimitriuscensor/NLP_Lurkmore/texts'
    l = os.listdir(directory)
    for item in l:
        i += 1
        s = '/home/dimitriuscensor/NLP_Lurkmore/texts/'
        s += i
        file = codecs.open(s, 'r', 'utf-8')
        text_read = file.read().lower()
        sentences = text_read.split('.')
        for sentence in sentences:
            lem = ''
            regexp = re.compile(u'[^а-я]')
            sentence = re.sub(regexp, ' ', sentence)
            word_list = sentence.split(' ')
            for token in word_list:
                if token not in stop_words:
                    lem += token
                    lem += ' '
            lem_list = m.lemmatize(lem)
            outp.write(b' '.join(lem_list))
            outp.write(u'\r\n')
        if i % 1000 == 0:
            print("Saved " + str(i) + " articles")
print("Finished. Saved " + str(i) + " articles")
