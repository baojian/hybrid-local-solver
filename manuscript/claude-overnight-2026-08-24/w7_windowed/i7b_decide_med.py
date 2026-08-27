import sys, json
sys.path.insert(0, '/home/claude/work/overnight/w7_windowed')
from i7b_decide import decide
from i6b_class3 import petersen, cycle, rook, cocktail, circulant, hypercube
res = []
for name, adj, q in [
        ('Pet q=1/10', petersen(), '1/10'),
        ('Pet q=1/4', petersen(), '1/4'),
        ('Pet q=1/3(eq)', petersen(), '1/3'),
        ('C10 q=1/20', cycle(10), '1/20'),
        ('Rook3 q=1/10', rook(3), '1/10'),
        ('Cock3 q=1/4', cocktail(3), '1/4'),
        ('C12 q=1/20', cycle(12), '1/20'),
        ('Circ12(1,2) q=1/10', circulant(12, (1, 2)), '1/10'),
]:
    res.append(decide(name, adj, q))
json.dump(res, open('i7b_decide_med.json', 'w'), indent=1, default=str)
