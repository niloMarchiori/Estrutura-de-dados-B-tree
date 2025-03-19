from Models.node import Node
from Models.btree import B_tree
from random import randint



btree=B_tree(3)
count=0
operacoes=''
with open('teste.txt','w') as doc:
    doc.write('')


while True:
    i=randint(0,1000)
    o=randint(1,10)
    with open('teste.txt','a') as doc:
        doc.write(f"{o}:{i} \n")
    print(f"{o}:{i} \n")
    if o>3:
        btree.btree_insert(i,1)
    else:
        btree.btree_remove(key=i)
    count+=1
    print(btree.bsf_str())
    if count==20:
        input()
    

