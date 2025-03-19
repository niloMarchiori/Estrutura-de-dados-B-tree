from Models.node import Node
from Models.btree import B_tree
from random import randint

btree=B_tree(3)
count=0
operacoes=''
with open('teste.txt','r') as doc:
    entrada=doc.readlines()

count=0
for line in entrada:
    print(line)
    o,i=map(int,line.split(':'))
    if o>3:
        btree.btree_insert(i,1)
    else:
        btree.btree_remove(key=i)
    # print(btree.bsf_str())


