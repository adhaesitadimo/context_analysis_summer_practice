import codecs
import gensim
from tqdm import tqdm


def build_approximity(word, neighbours, neighbours2, file, vocab, it):
    #file.write(word)
    word_neighbours = neighbours[it].split()
    #print(word_neighbours)
    word_2_neighbours = neighbours2[it].split()
    #print(word_2_neighbours)
    for token in vocab:
        if token in word_neighbours:
            file.write(' 2')
        elif token in word_2_neighbours:
            file.write(' 1')
        else:
            file.write(' 0')
    file.write(u'\r\n')

if __name__ == "__main__":
    with codecs.open('common_vocabulary.txt', 'r', 'utf-8') as inp:
        vocabulary = []
        for line in inp:
            elem = line.strip()
            vocabulary.append(elem)
        print('Vocabulary has been built')
    print(len(vocabulary))
    with codecs.open('only_neighbours_wiki.txt', 'r', 'utf-8') as inp1:
        neighbours_list = []
        for line in inp1:
            elem = line.strip()
            neighbours_list.append(elem)
        print('Neighbours list has been built')
    print(len(neighbours_list))
    with codecs.open('neighbours_2_wiki.txt', 'r', 'utf-8') as inp2:
        neighbours_2_list = []
        for line in inp2:
            elem = line.strip()
            neighbours_2_list.append(elem)
        print('Neighbours of neighbours list has been built')
    print(len(neighbours_2_list))
    with codecs.open('matrix_numbers_wiki.txt', 'w', 'utf-8') as outp:
        i = 0
        for item in tqdm(vocabulary):
            build_approximity(item, neighbours_list, neighbours_2_list, outp, vocabulary, i)
            i += 1
