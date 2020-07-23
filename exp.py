from tests import Tests
import matplotlib.pyplot as plt


# FIRST TEST
def start_test_one(t):
    for _ in range(10):
        print t.exec_first()


# SECOND TEST
def start_test_two(t):
    parole = ['a', 'ad', 'con', 'muro', 'zoppo', 'marito', 'sboccia', 'faticavo', 'penzolano']
    r = t.exec_second(parole)
    tempi, numeri = r[0], r[1]

    plt.figure()
    x = range(len(parole))
    plt.xticks(x, parole)
    plt.plot(x, tempi)
    plt.title('tempi')
    plt.xlabel('parola')
    plt.ylabel('secondi')
    plt.legend(['edit', 'ngram'], loc=2)
    plt.grid()

    plt.figure()
    plt.xticks(x, parole)
    plt.plot(x, numeri)
    plt.title('parole vicine trovate')
    plt.xlabel('parola')
    plt.ylabel('numero parole vicine trovate')
    plt.legend(['edit', 'ngram'], loc=2)
    plt.grid()

    plt.show()


def start_test_three(t):
    r = t.exec_third()
    costi, coefficienti, res1, res2 = r[0], r[1], r[2], r[3]

    plt.figure()
    plt.plot(costi, res1)
    plt.title('numero parole trovate al variare della soglia di costo')
    plt.xlabel('soglie costi edit distance')
    plt.ylabel('numero parole trovate')
    plt.grid()

    plt.figure()
    plt.plot(coefficienti, res2)
    plt.title('numero parole trovate al variare di jaccard')
    plt.xlabel('soglie coefficiente jaccard')
    plt.ylabel('numero parole trovate')
    plt.grid()


def start_test_four(t):
    r = t.exec_fourth()
    parole, res = r[0], r[1]

    print parole, res

    plt.figure()
    plt.plot([2, 3, 4], res)
    plt.title('numero parole trovate al variare dei grammi')
    plt.xlabel('grammi')
    plt.ylabel('numero parole trovate')
    plt.legend(parole)
    plt.grid()

def start_test_five(t):
    t.exec_fifth()

if __name__ == '__main__':

    t = Tests()
    start_test_one(t)
    start_test_two(t)
    start_test_three(t)
    start_test_four(t)
    start_test_five(t)

    plt.show()
