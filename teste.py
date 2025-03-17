from Models.node import Node
from Models.btree import B_tree
from sys import stdin
import sys
from io import StringIO


entrada= '''10
20
30
40
15
25
35
12
22
16
45
36
34

45

34

40

36

25

35
'''

sys.stdin=StringIO(entrada)

btree=B_tree(4)
while True:
    line=input()
    try:
        i=int(line)
        btree.btree_insert(i,1)
        print(btree.bsf_str())
    except:
        i=int(input())
        btree.btree_remove(i)
        print(btree.bsf_str())