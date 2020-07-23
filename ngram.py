from operator import itemgetter
import ast


class Ngram:

    def __init__(self):
        self.soglia = 0.6

    def ngram(self, p, n):
        if len(p) < n:
            # ERRORE: Lunghezza parola troppo piccola
            return []
        t = [_ for _ in p]
        k = []
        for i in range(len(t) - n + 1):
            k.append(''.join(t[i:i + n]))
        return k

    def jaccard(self, ng1, ng2):
        ng2 = ast.literal_eval(ng2)

        common = [a for a in ng1 if a in ng2]
        unique = [b for b in ng1 if b not in common] + [c for c in ng2 if c not in common]

        common_length = len(common)
        union_length = common_length + len(unique)

        if union_length == 0:
            return 0

        return common_length / float(union_length)

if __name__ == '__main__': 
    a = Ngram()
    b = a.ngram('algoritmi', 2)
    print b
    # lista = []
    #
    # with open("2_grams.txt", 'r') as r:
    #     for line in r:
    #         s = line.split(' -> ')
    #         p, g = s[0], s[1].rstrip()
    #         f = a.jaccard(b, g)
    #         print p, f
    #         if f >= 0.6:
    #             lista.append((p, f))
    # print 'risultati (%s)' % len(lista), '-->', sorted(lista, key=itemgetter(1), reverse=True)
