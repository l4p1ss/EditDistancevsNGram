from ngram import Ngram
from timeit import default_timer as timer
from edit_distance import EditDistance
from operator import itemgetter as get
import random
import numpy as np
import string


class Tests:

    def __init__(self):
        self.numberOfGrams = 2
        self.sogliaCosto = 3
        self.sogliaJaccard = 0.6

    def execute(self):
        self.exec_first()
        self.exec_second() 
        self.exec_third()
        self.exec_fourth()
        self.exec_fifth()

    # Prendo una parola a caso dal dizionario e vedo quanto tempo ci mette a trovarla con edit distance e con ngram
    def exec_first(self):
        with open('60000_parole_italiane.txt', 'r') as f:

            e = EditDistance()
            a = Ngram()

            lines = f.readlines()
            rand = random.randint(0, len(lines))
            word = lines[rand].rstrip()
            print 'random word -->', word

            # test edit distance
            start = timer()
            for line in lines:
                p = line.rstrip()
                if p == word:
                    break
                _, op = e.edit_distance(word, p)
                _ = e.op_sequence(op, len(word)-1, len(p)-1, [])
            end = timer()
            time_edit = end - start
            # print 'tempo trascorso edit distance -->', time_edit

            # test ngrams
            b = a.ngram(word, self.numberOfGrams)
            with open("%s_grams.txt" % self.numberOfGrams, 'r') as r:
                start = timer()
                for line in r:
                    s = line.split(' -> ')
                    p, g = s[0], s[1]
                    if p == word:
                        break
                    _ = a.jaccard(b, g)
                end = timer()
            time_ngram = end - start
            # print 'tempo trascorso ngrams -->', time_ngram

            return [word, time_edit, time_ngram]

    # per ogni parola di dimensione variabile vado a vedere quanto ci mette edit e ngram e quante parole vicine trova
    def exec_second(self, parole):

        e = EditDistance()
        a = Ngram()

        tempi = []
        n_vicine_trovate = []

        for parola in parole:
            with open('60000_parole_italiane.txt', 'r') as f:
                # print 'parola --> ', parola

                # edit distance
                # print '----- EDIT DISTANCE'
                e_results = []
                start = timer()
                for line in f:
                    p = line.rstrip()
                    _, op = e.edit_distance(parola, p)
                    costo = e.op_sequence(op, len(parola)-1, len(p)-1, [])
                    if costo < self.sogliaCosto:
                        e_results.append((p, costo))
                end = timer()

                time_edit = end - start
                n_edit = len(e_results)

                # print 'risultati (%s)' % n_edit,  '-->', sorted(e_results, key=get(1))
                # print 'tempo -->', time_edit

                # ngrams
                # print '----- NGRAMS'
                g_results = []
                b = a.ngram(parola, self.numberOfGrams)
                with open("%s_grams.txt" % self.numberOfGrams, 'r') as r:
                    start = timer()
                    for line in r:
                        s = line.split(' -> ')
                        p, g = s[0], s[1]
                        f = a.jaccard(b, g)
                        if f > self.sogliaJaccard:
                            g_results.append((p, f))
                    end = timer()

                time_gram = end - start
                n_gram = len(g_results)

                # print 'risultati (%s)' % n_gram, '-->', sorted(g_results, key=get(1), reverse=True)
                # print 'tempo -->', time_gram
                # print '\n'

                tempi.append([time_edit, time_gram])
                n_vicine_trovate.append([n_edit, n_gram])

        return [tempi, n_vicine_trovate]

    # Numero di risultati trovati al variare della soglia e del coefficiente di jaccard
    def exec_third(self):
        e = EditDistance()
        a = Ngram()

        costi = []
        coefficienti = []
        risultati_edit = []
        risultati_gram = []

        parola = raw_input("**** Inserisci parola --> ")

        # edit distance
        # print '----- EDIT DISTANCE'
        # costi: 1, 2, 3, 4, 5
        for c in range(1, 6):
            costi.append(c)
            with open('60000_parole_italiane.txt', 'r') as f:
                e_results = []
                for line in f:
                    p = line.rstrip()
                    _, op = e.edit_distance(parola, p)
                    costo = e.op_sequence(op, len(parola) - 1, len(p) - 1, [])
                    if costo < c:
                        e_results.append((p, costo))
                risultati_edit.append(len(e_results))
                # print 'ho trovato %s risultati per soglia costo %s' % (len(e_results), c), '-->', sorted(e_results, key=get(1))

        # ngram
        # print '----- NGRAM'
        b = a.ngram(parola, self.numberOfGrams)
        # coefficienti: 0.5, 0.6, 0.7, 0.8, 0.9
        for j in np.arange(0.5, 1.0, 0.1):
            coefficienti.append(j)
            with open("%s_grams.txt" % self.numberOfGrams, 'r') as f:
                g_results = []
                for line in f:
                    s = line.split(' -> ')
                    p, g = s[0], s[1]
                    f = a.jaccard(b, g)
                    if f > j:
                        g_results.append((p, f))
                risultati_gram.append(len(g_results))
                # print 'ho trovato %s risultati per jaccard maggiore di %s' % (len(g_results), j), '-->', sorted(g_results, key=get(1), reverse=True)

        return [costi, coefficienti, risultati_edit, risultati_gram]

    # Numero di risultati trovati al variare del numero di grammi, con soglia 0.6
    def exec_fourth(self):
        a = Ngram()

        risultati = []

        # parola = raw_input("**** Inserisci parola --> ")

        parole = []
        with open('60000_parole_italiane.txt', 'r') as f:
            lines = f.readlines()
            for i in range(3):
                rand = random.randint(0, len(lines))
                word = lines[rand].rstrip()
                while len(word) < 5:
                    rand = random.randint(0, len(lines))
                    word = lines[rand].rstrip()
                parole.append(word)


        # grammi: 2, 3, 4
        for parola in parole:
            subarray = []
            for n in range(2, 5):
                with open("%s_grams.txt" % n, 'r') as f:
                    b = a.ngram(parola, n)
                    g_results = []
                    for line in f:
                        s = line.split(' -> ')
                        p, g = s[0], s[1]
                        f = a.jaccard(b, g)
                        if f > self.sogliaJaccard:
                            g_results.append((p, f))
                    # print 'ho trovato %s risultati per %s grammi' % (len(g_results), n), '-->', sorted(g_results, key=get(1), reverse=True)
                    subarray.append(len(g_results))
            risultati.append(subarray)

        return [parole, risultati]

    # Risultati ricerca edit/ngram al variare della soglia/jaccard di una parola storpiata
    def exec_fifth(self):

        e = EditDistance()
        a = Ngram()

        originale = raw_input("**** Inserisci parola --> ")
        parola = self.storpia(originale)
        print '**** Parola storpiata -->', parola

        # edit distance
        print '----- EDIT DISTANCE'
        # costi: 1, 2, 3, 4, 5
        for c in range(1, 6):
            with open('60000_parole_italiane.txt', 'r') as f:
                e_results = []
                for line in f:
                    p = line.rstrip()
                    _, op = e.edit_distance(parola, p)
                    costo = e.op_sequence(op, len(parola) - 1, len(p) - 1, [])
                    if costo < c:
                        e_results.append((p, costo))
                if any(originale in a for a in e_results):
                    w = 'parola originale trovata!'
                else:
                    w = 'parola originale non trovata!'
                print w, '(soglia costo %s, %s risultati)' % (c, len(e_results)), '-->', sorted(e_results, key=get(1))

        # ngram
        print '----- NGRAM'
        b = a.ngram(parola, self.numberOfGrams)
        # coefficienti: 0.5, 0.6, 0.7, 0.8, 0.9
        for j in np.arange(0.5, 1.0, 0.1):
            with open("%s_grams.txt" % self.numberOfGrams, 'r') as f:
                g_results = []
                for line in f:
                    s = line.split(' -> ')
                    p, g = s[0], s[1]
                    f = a.jaccard(b, g)
                    if f > j:
                        g_results.append((p, f))
                if any(originale in a for a in g_results):
                    w = 'parola originale trovata!'
                else:
                    w = 'parola originale non trovata!'
                print w, '(jaccard %s, %s risultati)' % (j, len(g_results)), '-->', sorted(g_results, key=get(1), reverse=True)

    # Restituisce una parola storpiata
    def storpia(self, word):
        c = list(word)
        do = random.randint(0, 2)
        i = random.randint(0, len(c) - 1)
        if do == 0:
            # scambia due caratteri casuali
            j = i+1
            if j == len(c):
                j -= 2
            c[i], c[j] = c[j], c[i]
        if do == 1:
            # elimina un carattere casuale
            c[i] = ''
        if do == 2:
            # aggiunge un carattere casuale
            c[i] = '%s%s' % (c[i], random.choice(string.ascii_lowercase))

        return ''.join(c)

# if __name__ == '__main__':
#     parole = []
#     with open('60000_parole_italiane.txt', 'r') as f:
#         lines = f.readlines()
#         for i in range(5):
#             rand = random.randint(0, len(lines))
#             word = lines[rand].rstrip()
#             while len(word) < 5:
#                 rand = random.randint(0, len(lines))
#                 word = lines[rand].rstrip()
#             parole.append(word)
#     print parole
