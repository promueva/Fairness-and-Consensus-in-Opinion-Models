import random

def generate_random_word(G, l):
    return random.choices(G.alphabet, k=l)

def generate_kfair_word(G, l, k):
    if k < len(G.alphabet):
        raise Exception("the k window is smaller than amount of edges. There's no possible k-fair execution")
    word = []
    prob_delta = 1.0 / k
    letter_queue = [(letter, prob_delta) for letter in G.alphabet]
    random.shuffle(letter_queue)

    def choose_letter():
        while True:
            for i, letter in enumerate(letter_queue):
                r = random.random()
                if r < letter[1]:
                    letter_queue.pop(i)
                    for j in range(i, len(letter_queue)):
                        letter_queue[j] = (letter_queue[j][0], letter_queue[j][1]+prob_delta)
                    letter_queue.append((letter[0], prob_delta))
                    return letter[0]
                else:
                    letter_queue[i] = (letter[0], letter[1]+prob_delta)

    for i in range(l):
        word.append(choose_letter())

    return word

def check_kfairness(G, word, k):
    last_appearance = {letter: 0 for letter in G.alphabet}
    for letter in word:
        for l in G.alphabet:
            last_appearance[l] += 1
        last_appearance[letter] = 0
        if any([a > k for a in last_appearance.values()]):
            return False
    return True


