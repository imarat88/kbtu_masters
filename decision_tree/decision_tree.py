import csv
import pandas as pd
import math
import json

target = ''

def build_tree(df2, level):
    if len(df2.columns) == 0:
        return None
    global  target
    d = dict()
    p = 0
    cCount = 0
    maxc = df2.columns[0]
    minEntropy = 1000000
    sbest = set()
    s = set()
    for c in df2.columns:
        c = c.strip()
        if (c != target) or len(df2.columns) == 1:
            cCount = len(df2[c])
            s = set(df2[c])
            cEntropy = 0
            for i in s:
                pCount = len(df2[df2[c] == i])
                s2 = set(df2[df2[c] == i][target])
                pEntropy = 0
                p = pCount / cCount
                for j in s2:
                    dff = df2[(df2[c] == i) & (df2[target] == j)]
                    elCount = len(dff)
                    pEntropy = pEntropy - (elCount / pCount) * math.log2((elCount / pCount))
                cEntropy = cEntropy + p * pEntropy
            if minEntropy>cEntropy:
                minEntropy = cEntropy
                maxc = c
                sbest = s
    d[maxc] = {}
    if len(sbest)>0:
        for i in sbest:
            d[maxc][i] = {}
            df = df2[df2[maxc] == i]
            del(df[maxc])
            d[maxc][i] = build_tree(df, level+1)
            if d[maxc][i] is None:
                d = i
        if isinstance(d,dict):
            if len(d[maxc].keys()) <= 1 and level>0:
                d = d[maxc][i]
            elif level>0:
                st = set([d[maxc][k] for k in d[maxc].keys()])
                if len(st) == 1 and level>0:
                    d = d[maxc][i]
    else:
        d = list(df2)
    return d

def main():
    global target
    df = pd.read_csv('decision_tree.csv', delimiter=';', quotechar='"')
    df2 = df.ix[:, df.columns !='ID']
    target = df.columns[-1]
    d = build_tree(df2, 0)
    return d

if __name__ == '__main__':
    tree = main()
    with open('decision_tree.json', 'w') as fp:
        json.dump(tree, fp)
    print(tree)