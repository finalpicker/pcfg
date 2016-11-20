__author__ = "TuWei"

import sys
from collections import defaultdict

def inside(parses, d1, d2, words, b, s, p, n):
    for i in range(0, n):
        for j in range(0, n-i):
            k = j + i
            parse = parses[(j, k)]
            beta = b[(j, k)]
            if j == k:
                lefts = [x for x in d2[words[j]]]
                left = lefts[0]
                parse.append(left)
                beta[left] = d1[left][words[j]]
                s[(j, k)][left] = beta[left]
            else:
                for d in range(j, k):
                    for left in parses[(j, d)]:
                        for right in parses[(d + 1, k)]:
                            lefts = [x for x in d2[' '.join((left, right))]]
                            for parent in lefts:
                                parse.append(parent)
                                beta[parent] += d1[parent][' '.join((left, right))] * b[(j, d)][left] * b[(d + 1, k)][right]
                                prob = d1[parent][' '.join((left, right))] * s[(j, d)][left] * s[(d + 1, k)][right]
                                if prob > s[(j, k)][parent]:
                                    s[(j, k)][parent] = prob
                                    p[(j, k)][parent] = (d, left, right)

def outside(parses, d1, d2, a, b, n):
    whole = (0, n - 1)
    for s in parses[whole]:
        a[whole][s] = 1.0
    for i in range(n-1, -1, -1):
        for j in range(0, n - i):
            k = j + i
            parse = parses[(j, k)]
            alpha = a[(j, k)]
            for left in parse:
                for d in range(k + 1, n):
                    for right in parses[(k + 1, d)]:
                        lefts = [x for x in d2[' '.join((left, right))]]
                        for parent in lefts:
                            if left != right:
                                alpha[left] += a[(j, d)][parent] * d1[parent][' '.join((left, right))] * b[(k + 1, d)][right]
            for right in parse:
                for d in range(0, j):
                    for left in parses[(d, j - 1)]:
                        lefts = [x for x in d2[' '.join((left, right))]]
                        for parent in lefts:
                            alpha[right] += a[(d, k)][parent] * d1[parent][' '.join((left, right))] * b[(d, j - 1)][left]

def tree(words, p, m, l, r):
    if l == r:
        return '(' + m + ' '+ words[l]+')'
    d,left,right=p[(l, r)][m]
    l1=tree(words, p, left, l, d)
    r1=tree(words, p, right, d + 1, r)
    return '(' + m + l1 + r1 + ')'


def main():
    d1=defaultdict(lambda: defaultdict(float))
    d2=defaultdict(lambda: defaultdict(float))
    a=defaultdict(lambda: defaultdict(float))
    b=defaultdict(lambda: defaultdict(float))
    s=defaultdict(lambda: defaultdict(float))
    p=defaultdict(lambda: defaultdict(float))

    infile = open(sys.argv[1], 'r')
    lines = infile.readlines()
    for line in lines:
        l,r,prob = tuple(line.split(" # "))
        d1[l][r] = float(prob)
        d2[r][l] = float(prob)
    infile.close()

    sentence = "A boy with a telescope saw a girl"
    words = sentence.lower().split(' ')
    length = len(words)

    parses = defaultdict(list)
    inside(parses,d1,d2,words,b,s,p,length)
    outside(parses,d1,d2,a,b,length)

    output = open(sys.argv[2],'w')
    output.write(tree(words,p,'S',0,length-1) + '\n')
    output.write(str(s[(0,length-1)]['S']) + '\n')
    results = []
    for i in parses:
        for j in parses[i]:
            if a[i][j]:
                results.append(str(j)+' # '+str(i[0]+1)+' # '+str(i[1]+1)+' # '+str(b[i][j])+' # '+str(a[i][j]))
    results.sort()
    for result in results:
        output.write(result+'\n')
    output.close()

if __name__ == '__main__':
    main()

