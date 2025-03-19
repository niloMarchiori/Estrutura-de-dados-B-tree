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
            #####################
            if key==540:
                pass
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
    def search_predecessor_sucessor(curr_node:Node,idx:int):
        '''Procura pela chave predecessora ou sucessora de uma chave, dando preferência à aquela contida em um nó x tal que n[x]>=ceil(t/2)
        Args:
            curr_node= nó cuja chave está sendo substituída
            idx= índice da chave que está sendo substituída
        return:
            left= booleano que informa se a nova chave está no filho da esquerda (predecessor) ou direita (sucessor)
            key= chave sucessora/predecessora
            val= informacao associada a chave sucessora/predecessora'''
        left=False

        #Encontra chave predecessora
        child=curr_node.pointers[idx]
        while not child.leaf:
            child=child.pointers[-1]
        pre_key=child.keys[-1]
        pre_val=child.data[-1]
        if child.n>=ceil(curr_node.t/2):#A chave pode ser removida dessa folha
            left=True
            return  left,pre_key,pre_val
        
        #Se a predecessora não puder ser removida, procura-se a sucessora
        child=curr_node.pointers[idx+1]
        while not child.leaf:
            child=child.pointers[0]
        pos_key=child.keys[0]
        pos_val=child.data[0]

        return left,pos_key,pos_val
    
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

        #Abaixo é feita a concatenação das listas pela direita, para melhorar o desempenho

        if parent.keys[idx]<brother.keys[0]: #É o irmão adjacente a direita]

            new_keys=child.keys + [godown_key] + brother.keys
            new_data=child.data + [godown_val] + brother.data
            new_pointer=child.pointers+brother.pointers
            
        else: #É o irmão adjacente da esquerda
            new_keys= brother.keys + [godown_key] + child.keys
            new_data=brother.data + [godown_val] + child.data
            new_pointer=brother.pointers+child.pointers
        parent.remove_key(idx) #O pai perde sua chave e um dos ponteiros

        #Um novo nó é criado com os dados oriundos da concatenação
        new_node=Node(parent.t,new_keys,new_data,new_pointer,brother.leaf,parent)
        parent.pointers[idx]=new_node

        if not new_node.leaf:
            for son in new_node.pointers:
                son.parent=new_node
            
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
                if brother.leaf: 
                    return True,brother            
        return False,brother
    
    
    def fix_subtree(self,curr_node:Node,problematic_node:Node,idx):
        can_redis,brother=B_tree.can_redistribute(curr_node,problematic_node,idx)

        ####################
        if curr_node.keys[idx]==621:
            pass

        if can_redis: 
            B_tree.redistribute(curr_node,problematic_node,brother,idx)
            ########################
            if len(curr_node.keys)+1!=len(curr_node.pointers):
                pass
            return curr_node.is_vallid()

        else:
            self.concatenate(curr_node,problematic_node,brother,idx)
            if not self._root.keys:
                new_root=self._root.pointers[0]
                self._root=new_root
                new_root.parent=None
            
            return curr_node.is_vallid()
        
    def btree_remove(self,key:int,curr_node:Node=None):
        '''Desce recursivamente até o nó em que a chave deve ser removida, enquanto desempilha as chamadas da função manipulação necessárias são feitas
        Args:
            key=chave a ser removida
            parent_idx=ín
            node=Raiz da subárvore em que a chave se encontra
        return:
            Booleano que indica no desempilhamento ainda existem manipulações a serem feitas, resultantes da remoção
        '''
        ########################
        if key==517:
            pass
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
                return curr_node.is_vallid()

            elif not curr_node.leaf: #A chave está sendo removida de um nó interno
                left,new_key,new_val=B_tree.search_predecessor_sucessor(curr_node,idx) #Procura pela chave predecessora ou sucessora
                curr_node.update(idx,new_key,new_val) #Substitui a chave

                if left:
                    subtree=curr_node.pointers[idx]
                else:
                    subtree=curr_node.pointers[idx+1]
                
                self.btree_remove(new_key,subtree) #Remove da folha a chave usada no nó atual
                if not subtree.is_vallid():
                    self.fix_subtree(curr_node,subtree,idx)
                return curr_node.is_vallid()

        
        elif not curr_node.leaf: #Chave não foi encontrado, mas ainda pode existir na subárvore com raiz em 'node'
            removed_finish=self.btree_remove(key,node)

            if idx==curr_node.n: #Significa que caso a chave estivesse nesse nó, ela seria a última chave
                idx-=1 #Recua o índice da chave, pois 'node' está a direita da última chave

            if removed_finish: #A remoção não propagou manipulações até essa chamada
                return True
            
            return self.fix_subtree(curr_node,node,idx)    
                
        elif curr_node.leaf: #Se não foi encontrado e o nó atual é uma folha, a chave não existe
            return True
        
        #Ao final do processo de remoção, confere se a raiz não está vazia
        while self._root.n==0:
            new_root=self._root
            self._root=new_root
            new_root.parent=None

    
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

