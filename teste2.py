from Models.node import Node
from math import ceil
def split(self:Node):
        '''Divide o nó atual em dois nós, criando um novo nó e modificando o atual, 
        cada um com metade dos elementos
        
        return:
            right_node: nó resultante da segunda metade da divisão das chaves'''

        t=self.t
        keys=self.keys
        data=self.data
        pointers=self.pointers
        right_node=Node(t,keys[ceil(t/2):],data[ceil(t/2):],pointers[ceil(t/2):],self.leaf,self.parent)
    
        while self.n-1>ceil(t/2)-2:
            self.pointers.pop()
            self.keys.pop()
            self.data.pop()
       
        return right_node