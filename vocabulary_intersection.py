import codecs
import gensim
from tqdm import tqdm


# vicinity construction function
def vicinity_constructor(corpus, corpus_model, neighbour0, neighbour1, neighbour2):
    counter = 0
    corpus_neighbours_dict = {}
    for token in tqdm(common_vocabulary):
        neighbour1_list = []
        neighbour2_list = []
        counter += 1
        corpus_neighbours_list = []
        w2v_res_corpus = corpus_model.most_similar(token)
        for item in w2v_res_corpus:
            if item[1] > 0.5 and len(item[0]) > 3:
                # processing neighbours
                corpus_neighbours_list.append(item[0])
                neighbour1_list.append(item[0])
                w2v_res_neighbour = corpus_model.most_similar(item[0])
                for neighbour in w2v_res_neighbour:
                    if neighbour[1] > 0.5 and len(neighbour[0]) > 3:
                        # processing neighbours of neighbours, if they are not in the list already
                        if neighbour[0] not in corpus_neighbours_list and neighbour[0] != token:
                            corpus_neighbours_list.append(neighbour[0])
                            neighbour2_list.append(neighbour[0])
        corpus_neighbours_dict[token] = corpus_neighbours_list
        neighbour0.write(u' '.join(neighbour1_list) + u' '.join(neighbour2_list))
        neighbour0.write(u'\r\n')
        neighbour1.write(u' '.join(neighbour1_list))
        neighbour1.write(u'\r\n')
        neighbour2.write(u' '.join(neighbour2_list))
        neighbour2.write(u'\r\n')
    return corpus_neighbours_dict


model_wiki = gensim.models.Word2Vec.load("wiki.ru.text.model")
model_lurk = gensim.models.Word2Vec.load("lurkmore.text.model")

common_vocabulary = []
with codecs.open('common_vocabulary.txt', 'w', 'utf-8') as common:
    for word in model_wiki.wv.vocab:
        if word in model_lurk.wv.vocab and len(word) > 3:
            print(word)
            common_vocabulary.append(word)
            common.write(word)
            common.write(u'\r\n')

print('Words in total: ' + str(len(common_vocabulary)))
wiki0 = codecs.open('neighbours_wiki.txt', 'w', 'utf-8')
wiki1 = codecs.open('only_neighbours_wiki.txt', 'w', 'utf-8')
wiki2 = codecs.open('neighbours_2_wiki.txt', 'w', 'utf-8')
wiki_neighbours_dict = vicinity_constructor("wiki", model_wiki, wiki0, wiki1, wiki2)
wiki0.close()
wiki1.close()
wiki2.close()
lurk0 = codecs.open('neighbours_lurk.txt', 'w', 'utf-8')
lurk1 = codecs.open('only_neighbours_lurk.txt', 'w', 'utf-8')
lurk2 = codecs.open('neighbours_2_lurk.txt', 'w', 'utf-8')
lurk_neighbours_dict = vicinity_constructor("lurk", model_lurk, lurk0, lurk1, lurk2)
lurk0.close()
lurk1.close()
lurk2.close()
print(len(wiki_neighbours_dict))
print(len(lurk_neighbours_dict))

'''
# intersecting wiki and lurkmore vocabularies to check if one of them is empty
i = 0
intersection = {}
for item_wiki in tqdm(wiki_neighbours_dict.items()):
    i += 1
    for item_lurk in lurk_neighbours_dict.items():
        if item_wiki[0] == item_lurk[0]:
            if len(item_wiki[1]) != 0 and len(item_lurk[1]) != 0:
                set_wiki = set(item_wiki[1])
                set_lurk = set(item_lurk[1])
                intersection_set = set_wiki.intersection(set_lurk)
                intersection[item_wiki[0]] = len(intersection_set)


# constructing vocab
i = 0
with codecs.open('working_vocabulary.txt', 'w', 'utf-8') as voc:
    for key in tqdm(intersection):
        i += 1
        voc.write(key)
        voc.write(u'\r\n')


with codecs.open('neighbours.txt', 'w', 'utf-8') as outp:
    i = 0
    for item_wiki in tqdm(wiki_neighbours_dict.items()):
        for item_lurk in lurk_neighbours_dict.items():
            if item_wiki[0] == item_lurk[0] and item_wiki[0] in intersection:
                i += 1
                outp.write(item_wiki[0])
                outp.write(u'\r\n')
                outp.write(u'\r\n')
                outp.write('Wiki:\r\n')
                outp.write(' '.join(item_wiki[1]))
                outp.write(u'\r\n')
                outp.write('Lurk:\r\n')
                outp.write(' '.join(item_lurk[1]))
                outp.write(u'\r\n')
                outp.write(u'\r\n')
        if i % 200 == 0:
            print(str(i) + ' articles saved')

with codecs.open('neighbours_wiki.txt', 'w', 'utf-8') as outp:
    i = 0
    for item_wiki in tqdm(wiki_neighbours_dict.items()):
        if item_wiki[0] in intersection:
            i += 1
            #outp.write(item_wiki[0])
            outp.write(u' ')
            outp.write(' '.join(item_wiki[1]))
            outp.write(u'\r\n')
    print(i)

with codecs.open('neighbours_lurk.txt', 'w', 'utf-8') as outp:
    i = 0
    for item_lurk in tqdm(lurk_neighbours_dict.items()):
        if item_lurk[0] in intersection:
            i += 1
            #outp.write(item_lurk[0])
            outp.write(u' ')
            outp.write(' '.join(item_lurk[1]))
            outp.write(u'\r\n')
    print(i)'''
