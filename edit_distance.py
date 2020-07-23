from operator import itemgetter

class EditDistance:

    def __init__(self):
        self.cost = {'delete': 1, 'insert': 1, 'copy': 0, 'replace': 2, 'twiddle': 1}

    def edit_distance(self, x, y):

        m = len(x)
        n = len(y)

        # print 'edit distance tra -->', x, 'e', y

        c = [[0 for _ in range(n)] for _ in range(m)]
        op = [['' for _ in range(n)] for _ in range(m)]

        for i in range(m):
            c[i][0] = i * self.cost['delete']
            op[i][0] = 'delete'

        for j in range(n):
            c[0][j] = j * self.cost['insert']
            op[0][j] = 'insert' 

        for i in range(1, m):
            for j in range(1, n):
                c[i][j] = float('inf')
                if x[i] == y[j]:
                    c[i][j] = c[i-1][j-1] + self.cost['copy']
                    op[i][j] = 'copy'
                if x[i] != y[j] and c[i-1][j-1] + self.cost['replace'] < c[i][j]:
                    c[i][j] = c[i-1][j-1] + self.cost['replace']
                    op[i][j] = 'replace'
                if i >= 2 and j >= 2 and x[i] == y[j-1] and x[i-1] == y[j] and c[i-2][j-2] + self.cost['twiddle'] < c[i][j]:
                    c[i][j] = c[i-2][j-2] + self.cost['twiddle']
                    op[i][j] = 'twiddle'
                if c[i - 1][j] + self.cost['delete'] < c[i][j]:
                    c[i][j] = c[i-1][j] + self.cost['delete']
                    op[i][j] = 'delete'
                if c[i][j - 1] + self.cost['insert'] < c[i][j]:
                    c[i][j] = c[i][j-1] + self.cost['insert']
                    op[i][j] = 'insert'

        if x[0] == y[0]:
            op[0][0] = 'copy'
            c[0][0] += self.cost['copy']
        else:
            op[0][0] = 'replace'
            c[0][0] += self.cost['replace']

        return c, op

    def op_sequence(self, op, i, j, t):
        t.append(op[i][j])
        if i == 0 and j == 0:
            # print 'op -->', t[::-1]
            return self.calc_cost(t)
        if op[i][j] == 'copy' or op[i][j] == 'replace':
            u = i-1
            k = j-1
        elif op[i][j] == 'twiddle':
            u = i-2
            k = j-2
        elif op[i][j] == 'delete':
            u = i-1
            k = j
        else:
            u = i
            k = j-1
        return self.op_sequence(op, u, k, t)

    def calc_cost(self, t):
        c = 0
        for e in t:
            if e == 'delete':
                c += self.cost['delete']
            if e == 'insert':
                c += self.cost['insert']
            if e == 'copy':
                c += self.cost['copy']
            if e == 'replace':
                c += self.cost['replace']
            if e == 'twiddle':
                c += self.cost['twiddle']
        return c

if __name__ == '__main__':
    p1 = 'matteo'
    p2 = 'atteo'
    #
    m = len(p1)
    n = len(p2)
    #
    e = EditDistance()
    _, op = e.edit_distance(p1, p2)
    #
    costo = e.op_sequence(op, m-1, n-1, [])
    #
    # print 'costo -->', costo
    # e = EditDistance()
    # p1 = 'lavagna'
    # lista = []
    # with open('60000_parole_italiane.txt', 'r') as f:
    #     for line in f:
    #         p = line.rstrip()
    #         _, op = e.edit_distance(p1, p)
    #         costo = e.op_sequence(op, len(p1)-1, len(p)-1, [])
    #         if costo < 4:
    #             lista.append((p, costo))
    # print 'risultati (%s)' % len(lista), '-->', sorted(lista, key=itemgetter(1))
