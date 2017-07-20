import codecs
import numpy as np
import gensim
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


model_wiki = gensim.models.Word2Vec.load("wiki.ru_lem.txt.model")
model_lurk = gensim.models.Word2Vec.load("lurkmore_lem.txt.model")

i = 0
with codecs.open('neighbours_wiki.txt', 'r', 'utf-8') as neighbour_file:
    for line in neighbour_file:
        i += 1
        word, neighbours_wiki = line.strip().split(' ', 1)
        print(word)
        coords_wiki = model_wiki.wv[word]
        print(coords_wiki)
        w2v_res_neighbour = model_wiki.most_similar(word)
        print(neighbours_wiki)
        word_wiki_list = [word]
        neighbours_wiki_list = neighbours_wiki.split(' ')
        for neighbour in neighbours_wiki_list:
            word_wiki_list.append(neighbour)
            wv_wiki = model_wiki.wv[neighbour]
            coords_wiki = np.vstack((coords_wiki, wv_wiki))

        model = TSNE(n_components=2, perplexity=100, early_exaggeration=1.0, n_iter=2000, method='exact',
                     random_state=0)
        np.set_printoptions(suppress=True)
        X = model.fit_transform(coords_wiki)
        plt.scatter(X[:, 0], X[:, 1])
        for label, x, y in zip(word_wiki_list, X[:, 0], X[:, 1]):
            plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
        plt.xlabel(word)
        plt.show()
        if i % 100 == 0:
            print(str(i) + " word vicinities plotted")
