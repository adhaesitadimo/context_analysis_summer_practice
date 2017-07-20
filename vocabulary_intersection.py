import codecs
import gensim


# vicinity construction function
def vicinity_constructor(corpus, corpus_model):
    counter = 0
    corpus_neighbours_dict = {}
    for token in common_vocabulary:
        counter += 1
        corpus_neighbours_list = []
        w2v_res_corpus = corpus_model.most_similar(token)
        for item in w2v_res_corpus:
            if item[1] > 0.7:
                # processing neighbours
                corpus_neighbours_list.append(item[0])
                w2v_res_neighbour = corpus_model.most_similar(item[0])
                for neighbour in w2v_res_neighbour:
                    if neighbour[1] > 0.7:
                        # processing neighbours of neighbours, if they are not in the list already
                        if neighbour[0] not in corpus_neighbours_list and neighbour[0] != token:
                            corpus_neighbours_list.append(neighbour[0])
        corpus_neighbours_dict[token] = corpus_neighbours_list
        if counter % 200 == 0:
            print(str(counter) + " " + corpus + " vicinities completed")
    return corpus_neighbours_dict


model_wiki = gensim.models.Word2Vec.load("wiki.ru_lem.txt.model")
model_lurk = gensim.models.Word2Vec.load("lurkmore_lem.txt.model")

common_vocabulary = []
for word in model_wiki.wv.vocab:
    if word in model_lurk.wv.vocab:
        print(word)
        common_vocabulary.append(word)

print('Words in total: ' + str(len(common_vocabulary)) )

wiki_neighbours_dict = vicinity_constructor("wiki", model_wiki)
lurk_neighbours_dict = vicinity_constructor("lurk", model_lurk)

# intersecting wiki and lurkmore vocabularies to check if one of them is empty
i = 0
intersection = {}
for item_wiki in wiki_neighbours_dict.items():
    i += 1
    for item_lurk in lurk_neighbours_dict.items():
        if item_wiki[0] == item_lurk[0]:
            if len(item_wiki[1]) != 0 and len(item_lurk[1]) != 0:
                set_wiki = set(item_wiki[1])
                set_lurk = set(item_lurk[1])
                intersection_set = set_wiki.intersection(set_lurk)
                intersection[item_wiki[0]] = len(intersection_set)
    if i % 200 == 0:
        print(str(i) + " words intersected")

# constructing vocab
i = 0
with codecs.open('working_vocabulary.txt', 'w', 'utf-8') as voc:
    for key in intersection:
        i += 1
        voc.write(key)
        voc.write(u'\r\n')
        if i % 200 == 0:
            print(str(i) + " words in vocabulary")


with codecs.open('neighbours.txt', 'w', 'utf-8') as outp:
    i = 0
    for item_wiki in wiki_neighbours_dict.items():
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
    for item_wiki in wiki_neighbours_dict.items():
        if item_wiki[0] in intersection:
            i += 1
            outp.write(item_wiki[0])
            outp.write(u' ')
            outp.write(' '.join(item_wiki[1]))
            outp.write(u'\r\n')
        if i % 200 == 0:
            print(str(i) + ' wiki articles saved')

with codecs.open('neighbours_lurk.txt', 'w', 'utf-8') as outp:
    i = 0
    for item_lurk in lurk_neighbours_dict.items():
        if item_lurk[0] in intersection:
            i += 1
            outp.write(item_lurk[0])
            outp.write(u' ')
            outp.write(' '.join(item_lurk[1]))
            outp.write(u'\r\n')
        if i % 200 == 0:
            print(str(i) + ' lurk wiki articles saved')