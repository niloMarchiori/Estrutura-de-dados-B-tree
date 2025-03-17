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
            parent_node=curr_node #Parente guarda o último nó visitado, na última iteração ele será a folha que deveria possuir a chave
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
                node.update(val=val,idx=idx)
            else:    
                node.insert(key,val,idx) #Insere a chave nessa folha, e recursivamente para os pais dela

                #Se ao longo do processo for necessário, a função node.insert() criará uma nova raiz (máximo uma vez
                # por chamada da função), então a raiz dessa árvore é atualizada para o pai da raiz antiga
                if not(self._root.parent==None): 
                    self._root=self._root.parent
    @staticmethod
    def btree_inter_node(self,curr_node:Node,idx:int):
        '''Remove uma key interna da da B-tree
        Args:
            curr_node= nó cuja chave está sendo substituída
            idx= índice da chave que está sendo substituída
        return:
            bool= booleano que informa se o sucessor/predecessor pode ser usado sem quebrar a validade das folhas
            key= chave sucessora/predecessora
            val= informacao associada a chave sucessora/predecessora'''
    
        #Encontra chave predecessora
        child=curr_node.pointers[idx]
        while not child.leaf:
            child=child.pointer[-1]

        pre_key=child.keys[-1]
        pre_val=child.data[-1]
        if child.n>=ceil(self._t/2):#A chave pode ser removida dessa folha
            child.remove_key(-1)
            return  True,pre_key,pre_val
        
        #Se a predecessora não puder ser removida, procura-se a sucessora
        child=curr_node.pointers[idx+1]
        while not child.leaf:
            child=child.pointer[0]

        pos_key=child.keys[0]
        pos_val=child.data[0]
        if child.n>=ceil(self._t/2):#A chave pode ser removida dessa folha
            child.remove_key(0)
            return  True,pos_key,pos_val

        return False, None,None
    

    @staticmethod
    def get_brothers(parent:Node,child:Node,idx):
        brothers=[]
        if parent.pointers[idx+1]!=child:
            brothers.append(parent.pointers[idx+1])
        if parent.pointers[idx]!=child:
            brothers.append(parent.pointers[idx])
        return brothers
        

    @staticmethod
    def concatenate(parent:Node,child:Node,brother:Node,idx:int):
        '''Efetua a redistribuição 
        Args:
            parent: Pai que cede a chave
            child=Filho com número de chaves problemáticas
            brother=irmão adjacente ao nó problemático
            idx=Índice da chave que divide os dois nós
            '''
        godown_key=parent.keys[idx]
        godown_val=parent.data[idx]


        if parent.keys[idx]<brother.keys[0]: #É o irmão adjacente a direita]
            parent.remove_key(idx)
            child.insert(godown_key,godown_val,child.n,brother.pointers[0])
            j=child.n
            for i in range(brother.n):
                key=brother.keys[i]
                val=brother.data[i]
                right_node=brother.pointers[i+1]
                child.insert(key,val,j+i,right_node)
            parent.pointers[idx]=child
            if not brother.leaf:
                for son in child.pointers:
                    son.parent=child
            
        else: #É o irmão adjacente da esquerda
            parent.remove_key(idx)
            brother.insert(godown_key,godown_val,brother.n,child.pointers[0])
            j=brother.n
            for i in range(child.n):
                key=child.keys[i]
                val=child.data[i]
                right_node=child.pointers[i+1]
                brother.insert(key,val,j+i,right_node)
            parent.pointers[idx]=brother
            if not brother.leaf:
                for son in brother.pointers:
                    son.parent=brother
            
    @staticmethod
    def redistribute(parent:Node,child:Node,brother:Node,idx:int):
        '''Efetua a concatenação 
        Args:
            parent: Pai que cede a chave
            child=Filho com número de chaves problemáticas
            brother=irmão adjacente ao nó problemático
            idx=Índice da chave que divide os dois nós
            '''
        godown_key=parent.keys[idx]
        godown_val=parent.data[idx]

        if parent.keys[idx]<brother.keys[0]: #É o irmão adjacente a direita
            goup_key=brother.keys[0]
            goup_val=brother.data[0]
            brother.remove_key(0)
            child.insert(godown_key,godown_val,child.n)
        else: #É o irmão adjacente da esquerda
            goup_key=brother.keys[-1]
            goup_val=brother.data[-1]
            brother.remove_key(-1)
            child.insert(godown_key,godown_val,0)

        parent.update(idx=idx,key=goup_key,val=goup_val)

    @staticmethod
    def can_redistribute(parent:Node,child:Node,idx:int):
        brothers=B_tree.get_brothers(parent,child,idx)

        for brother in brothers:
            if brother.n>=ceil(parent.t/2):
                return True,brother            
        return False,brother
            


    def btree_remove(self,key:int,curr_node:Node=None):
        '''Desce recursivamente até o nó em que a chave deve ser removida
        Args:
            key=chave a ser removida
            parent_idx=ín
            node=Raiz da subárvore em que a chave se encontra
        return:
            Booleano que indica no desempilhamento ainda existem manipulações a serem feitas, resultantes da remoção
        '''
        removed_finish=False

        if not curr_node: #Se um nó não é passado, a remoção inicia da raiz
            curr_node=self._root

        t=self._t
        #Encontra o nó filho que possui a chave, ou a raiz da subárvore que pode possuí-la
        found,node,idx=curr_node.find(key) 

        if found: #Se ele foi encontrado, node=curr_node
            if curr_node.parent==None and curr_node.leaf: #A árvore possui apenas a raiz
                curr_node.remove_key(idx)
                return True

            elif curr_node.leaf:
                curr_node.remove_key(idx)
                return curr_node.is_vallid() #Informa se a remoção terminou ou se propagou modificações

            elif not curr_node.leaf: #A chave está sendo removida de um nó interno
                possible,goup_key,goup_val=self.btree_inter_node(curr_node,idx)

                if possible: #Uma chave predecessora ou sucessora foi encontrada
                    curr_node.update(idx,goup_key,goup_val)
                    return True
                else:
                    return False
        
        elif not curr_node.leaf: #Chave foi encontrado, mas ainda pode existir na subárvore com raiz em 'node'
            removed_finish=self.btree_remove(key,node)

            if idx==curr_node.n: #Significa que caso a chave estivesse nesse nó, ela seria a última chave
                idx-=1 #Recua o índice da chave, pois 'node' está a direita da última chave

            if removed_finish: #A remoção não propagou manipulações até essa chamada
                return True
            
            can_redis,brother=B_tree.can_redistribute(curr_node,node,idx)
            if can_redis:    
                B_tree.redistribute(curr_node,node,brother,idx)
                return curr_node.is_vallid()

            else:
                self.concatenate(curr_node,node,brother,idx)
                if not self._root.keys:
                    new_root=self._root.pointers[0]
                    self._root=new_root
                    new_root.parente=None
                return curr_node.is_vallid()
            
        elif curr_node.leaf: #Se não foi encontrado e o nó atual é uma folha, a chave não existe
            return True
        
    def bsf_str(self):
        saida="-- ARVORE B \n"
        fila=[self._root]
        
        while fila:
            level_nodes=len(fila)
            level=''
            for _ in range(level_nodes):
                curr_node=fila.pop(0)
                level+=curr_node.print_in_line()+" "
                if curr_node.leaf:
                    continue
                for child in curr_node.pointers:
                    fila.append(child)
            saida+=level+'\n'

        return saida

