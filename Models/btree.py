from Models.node import Node
from math import ceil

class B_tree():
    def __init__(self,t:int,node:Node=None):
        if t==0:
            raise "Não existe árvore de ordem 0"
        self._t=t       #Atributos t e head só devem ser alterados a partir 
        self._root=node #das funções, portanto não possuem setter

    def btree_find(self,key):
        '''Args:
            key: chave a ser procurada na árvore
        
        Return:
            found: booleano que informa se esse nó possui aquela chave
            node: ponteiro para o nó que possui/pode possuir a chave
            idx: índice em que a chave se encontra, ou deveria se encontrar caso existisse'''
        
        curr_node=self._root
        found=False

        while True:
            idx=curr_node.idx(key) #Índice que aceitaria a chave (ignorando condição n<=t-1)
            if curr_node.leaf and idx >= len(curr_node.keys): break
            if curr_node.leaf and curr_node.keys[idx]!=key:   break
            if idx >= len(curr_node.keys) or  curr_node.keys[idx]<key:
                curr_node=curr_node.pointers[idx]
            elif curr_node.keys[idx]>key:
                curr_node=curr_node.pointers[idx+1]
              
            elif curr_node.keys[idx]==key:
                found=True
                break
        return found,curr_node,idx
    

    def btree_insert(self,key,val):
        '''Insere a chave e informação associada na árvore
        A inserção ocorre na folha, se propagando para nós pais se necessário'''
       
        if self._root==None: #Se a árvore ainda está vazia
            self._root=Node(self._t,[key],data=[val])
        else:
            found,node,idx=self.btree_find(key) #Encontra a folha que a chave precisa estar

            if found: #A chave já existe, é necessário atualizar a informação apenas
                node.update_val(val,idx)
            else:    
                node.insert(key,val,idx) #Insere a chave nessa folha, e recursivamente para os pais dela

                #Se ao longo do processo for necessário, a função node.insert() criará uma nova raiz (máximo uma vez
                # por chamada da função), então a raiz dessa árvore é atualizada para o pai da raiz antiga
                if not(self._root.parent==None): 
                    self._root=self._root.parent

    
    def bsf_print(self):
        print("-- ARVORE B \n")


        fila=[self._root]
        
        while fila:
            level_nodes=len(fila)
            level=''
            for _ in range(level_nodes):
                curr_node=fila.pop(0)
                level+=curr_node.print_in_line()
                if curr_node.leaf:
                    continue
                for child in curr_node.pointers:
                    fila.append(child)
            print(level)

        return level

