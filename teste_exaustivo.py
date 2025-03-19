from Models.node import Node
from Models.btree import B_tree
from random import randint



btree=B_tree(15)
count=0
operacoes=''
with open('teste.txt','w') as doc:
    doc.write('')


gab={}
while True:
    i=randint(0,1000)
    o=randint(1,30)
    with open('teste.txt','a') as doc:
        doc.write(f"{o}:{i} \n")
    # print(f"{o}:{i} \n")
    if o>17:
        btree.btree_insert(i,i)
        gab[i]=True
    elif o>7:
        btree.btree_remove(key=i)
        gab[i]=False
        
    else:
        found,node,idx=btree.btree_find(i)
        hard_found=False
        if i in gab.keys():
            hard_found=gab[i]
        print(found == hard_found)
        if found!=hard_found:
            print("DEU RUIM")
            input()
    count+=1
    # print(btree.bsf_str())
    if count==1000:
        count=0
        # input()
    

