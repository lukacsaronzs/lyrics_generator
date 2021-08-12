import os
import random
from graph import Graph, Vertex
import re
import string


def get_words_from_text(text_path):
    with open(text_path, 'rb') as file:
        text = file.read().decode("utf-8")

        text = re.sub(r'\[(.+)\]', ' ', text)

        text = ' '.join(text.split())
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()

    words = words[:1000]

    return words


def make_graph(words):
    g = Graph()
    prev_word = None
    # for each word
    for word in words:
        # check that word is in graph, and if not then add it
        word_vertex = g.get_vertex(word)

        # if there was a previous word, then add an edge if does not exist
        # if exists, increment weight by 1
        if prev_word:  # prev word should be a Vertex
            # check if edge exists from previous word to current word
            prev_word.increment_edge(word_vertex)

        prev_word = word_vertex

    g.generate_probability_mappings()

    return g


def compose(graph, words, length=50):
    composition = []
    word = graph.get_vertex(random.choice(words))
    for _ in range(length):
        composition.append(word.value)
        word = graph.get_next_word(word)

    return composition


def main():
    words = []

    artist = 'linkin_park'
    for song in os.listdir('./songs/{}'.format(artist)):
        if song == '.DS_Store':
            continue
        words.extend(get_words_from_text(
            'songs/{artist}/{song}'.format(artist=artist, song=song)))

    graph = make_graph(words)
    composition = compose(graph, words, 200)
    print(' '.join(composition))


if __name__ == '__main__':
    main()
