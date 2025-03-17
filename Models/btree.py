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

        while not found and curr_node: #Desce ao longo da árvore até encontrar a chave, ou o nó se tornar nulo
            parent_node=curr_node
            found,curr_node,idx=curr_node.find(key)

        if found: #Se a chave foi encontrada, o nó atual é o nó em que a chave se encontra
            return found,curr_node,idx
        else: #Se a chave não foi encontrada, o nó atual é nulo, e o pai dele é a folha
            return found,parent_node,idx
    

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

    def btree_remove(self,key:int,node:Node=None,alredy_removed:bool=False):
        '''Desce até o nó em que a chave deve ser removida
        Args:
        key=chave a ser removida
        parent_idx=ín
        node=Raiz da subárvore em que a chave se encontra
        alredy_removed=Carrega a informação durante o desempilhamento da recursão se o processo de remoção foi finalizado
        '''
        # if not node: #Se um nó não é passado, a remoção inicia da raiz
        #     node=self._root

        # t=node.t

        # if node.leaf:
        #     idx=node.idx(key)
        #     if idx >=t or node.keys[idx]!=key: #Se a chave não existe na árvore
        #         return True
        #     else:
        #         node.

        # if alredy_removed:
        #     return True
        # # if
        
    
    def bsf_str(self):
        saida="-- ARVORE B \n"
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
            saida+=level+'\n'

        return saida

