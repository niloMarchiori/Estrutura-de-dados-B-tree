from Models.node import Node
from math import ceil

class B_tree():
    def __init__(self,t:int,node:Node=None):
        self._t=t       #Atributos t e head só devem ser alterados a partir 
        self._head=node #das funções, portanto não possuem setter
        if not node:
            self._head=Node(t=t)

    def find(self,key):
        node=self._head
        found,node,idx=node.find(key)
        while not found and node:
            found,node,idx=node.find(key)
        return found, node, idx
    
    @staticmethod
    def split_child(parent_node:Node,idx_child:int,child:Node):
        t=parent_node.t
        middel_key=child.keys[ceil(t/2)-1]
        middel_data=child.keys[ceil(t/2)-1]
        right_child=child.split()
        parent_node.insert(middel_key,middel_data,idx_child,right_node=right_child)
    
    @staticmethod
    def insert_nonfull(node:Node,key,val):
        found,node,idx=node.find(key)
        if found:
            node.data[idx]=val
        elif node.leaf:
            node.insert(key,val,idx)
        else:
            

        

    def insert(self,key,val):
        t=self.t
        curr_node=self._head
        if curr_node.n==t-1:
            new_head=Node(t)
            new_head.pointers[0]=curr_node
            curr_node.parent=new_head
            B_tree.split_child(new_head,0,curr_node)
            B_tree.insert_nonfull(new_head,key)
        else:
            B_tree.insert_nonfull(curr_node,key)
            
