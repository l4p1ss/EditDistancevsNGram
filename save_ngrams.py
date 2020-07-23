from ngram import Ngram


# Funzione usata per generare un file %n_grams.txt contenente gli n_grammi da una lista di parole
def do(n):
    with open('60000_parole_italiane.txt', 'r') as f:
        with open("%s_grams.txt" % n, 'w+') as r:
            for line in f:
                p = line.rstrip()
                g = Ngram().ngram(p, n)
                r.write("%s -> %s\n" % (p, g))

if __name__ == '__main__':
    for i in range(2, 5):
        do(i)
 
