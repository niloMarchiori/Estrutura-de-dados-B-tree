from Models.node import Node
from Models.btree import B_tree

bt=B_tree(4)
for i in range(1,12):
    bt.btree_insert(i,1)
    print("----------------------------------------")
    bt.bsf_print()
    print("----------------------------------------")
bt.btree_insert(44,1)
print("----------------------------------------")
bt.bsf_print()
print("----------------------------------------")


