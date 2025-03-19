from math import ceil

class Node():
    def __init__(self,t,keys:list=[],data:list=[],pointers:list=[],leaf:bool=True,parent=None):
        self._t=t #número máximo de filhos
        self._structure=[keys[:],     #Keys
                         data[:],     #Data
                         pointers[:]]   #Pointers
        self._leaf=leaf #informação booleana desse nó ser ou não folha

        self._parent=parent

        if not pointers:
            self.pointers=[None for _ in range(self.n+1)]

    @property
    def t(self):
        '''Número máximo de filhos'''
        return self._t
    @property
    def n(self):
        '''Número atual de chaves registradas nesse nó'''
        return len(self.keys)
    
    @property
    def parent(self):
        '''Nó pai desse nó'''
        return self._parent
    
    @property
    def leaf(self):
        return self._leaf

    @property
    def keys(self):
        '''Chaves contidas nesse nó'''
        return self._structure[0]
    
    @property
    def data(self):
        '''Informações associadas as chaves desse nó'''
        return self._structure[1]
    @property
    def pointers(self):
        '''Ponteiros par ao qual esse nó aponta'''
        return self._structure[2]
    
    @keys.setter
    def keys(self,keys:list):
        '''Sobreescreve as chaves, por cópia de uma lista de chaves'''
        self._structure[0]=keys[:]
    
    @data.setter
    def data(self,data:list):
        '''Sobreescreve as informações, por cópia de uma lista de inforamações'''
        self._structure[1]=data[:]
        
            
    @pointers.setter
    def pointers(self,pointers:list):
        '''Sobreescreve os ponteiros filhos, por cópia de uma lista de ponteiros'''
        self._structure[2]=pointers[:]
        
    @parent.setter
    def parent(self,parent_node):
        '''Define o nó pai do nó atual para 'parent_node' '''
        self._parent=parent_node

    def is_vallid(self):
        t=self.t
        n=self.n
        if n>=t or n<ceil(t/2)-1:return False
        return True
            
            
    def find(self,key:int):
        '''Args:
            key: chave a ser procurada no nó
        
        Return:
            found: booleano que informa se esse nó possui aquela chave
            node: ponteiro para o nó que possui/pode possuir a chave
            idx: índice em que a chave se encontra, ou deveria se encontrar caso existisse'''
        found=False
        idx=0
        for idx,curr_key in enumerate(self.keys):
            if curr_key==key: 
                found=True
                return found,self,idx #A chave se encontra, nesse nó, no índice idx
            if curr_key>key:  #A chave não está nesse nó
                if self.leaf: #A chave deveria estar nessa folha
                    return found, self, idx 
                return found, self.pointers[idx],idx #A chave pode estar na subárvore da esquerda
            
        if self.leaf: #A chave deveria estar na última chave dessa folha
                return found, self,idx+1 
        return found,self.pointers[idx+1],idx+1 #A chave não está nesse nó, podendo estar na subárvore da direita
    
    def idx(self,key):
        '''Ecnontra o indice em que uma chave deveria se encontrar no nó (ignorando condição idx<=t-1)'''
        idx=0
        for idx,curr_key in enumerate(self.keys):
            if curr_key>=key:     
                return idx 
        return idx+1 


    def update(self,idx,key=None,val=None,left_node=None,right_node=None):
            if not key is None:
                self.keys[idx]=key

            if not val is None:
                self.data[idx]=val
                
            if right_node: 
                self.pointers[idx+1]=right_node

            if left_node: 
                self.pointers[idx]=left_node

    def insert(self,key:int,val,idx:int=None,right_node=None):
        '''Insere a chave e valor na posição idx, ou atualiza a informação caso a chave já exista. Caso o nó  esteja cheio, divide e repassa a inserção para o nó pai

        Args: 
        key=chave a ser inserida
        val=informação associadaa á aquela chave
        idx=índdice em que a chave devev ser inserida
        right_node=nó que ficará a direita da chave inserida
        '''

        if idx==None:#Se o índice de inserção não é passado, ele é encontrado
            idx=self.idx(key)
    
         
        self.keys.insert(idx,key)
        self.data.insert(idx,val)
        self.pointers.insert(idx+1,right_node)

        t=self.t
        if self.n>t-1: #O nó ultrapassou o limite de elementos

            middle_key=self.keys[ceil(t/2)-1] #Chave que vai subir
            middle_data=self.data[ceil(t/2)-1] #Informação que vai subir
            new_node=self.split() #Novo filho que ficará a direita da chave que subir
            parent=self.parent

            if parent==None: #O nó atual é a raiz
                new_root=Node(t,keys=[middle_key],data=[middle_data],leaf=False)
                new_root.pointers[0]=self
                new_root.pointers[1]=new_node

                self.parent=new_root
                new_node.parent=new_root
    
            else:
                parent.insert(middle_key,middle_data,right_node=new_node)



    def split(self):
        '''Divide o nó atual em dois nós, criando um novo nó e modificando o atual, 
        cada um com metade dos elementos
        
        return:
            right_node: nó resultante da segunda metade da divisão das chaves'''

        t=self.t
        keys=self.keys
        data=self.data
        pointers=self.pointers
        right_node=Node(t,keys[ceil(t/2):],data[ceil(t/2):],pointers[ceil(t/2):],self.leaf,self.parent)
        
        if not right_node.leaf: 
            for child in right_node.pointers:
                child.parent=right_node

        while self.n-1>ceil(t/2)-2:
            self.pointers.pop()
            self.keys.pop()
            self.data.pop()
       
        return right_node
    
    def find(self,key):
        '''Args:
            Key= Chave a ser encontrada nesse nó
        Return:
            found: booleano que informa se esse nó possui aquela chave
            node: ponteiro para raiz da subárvore que pode possuir a chave
            idx: índice em que a chave se encontra, ou deveria se encontrar nesse nó'''
        
        found=False
        node=self
        idx=self.idx(key)
        if idx >= len(node.keys) or  node.keys[idx]>key:
            node=node.pointers[idx]
            return found,node,idx

        elif node.keys[idx]<key:
            node=node.pointers[idx+1]
            return found,node,idx
            
        elif node.keys[idx]==key:
            found=True
            return found,node,idx

    def remove_key(self,idx):
        '''Remove a idx-ésima chave'''
        self.keys.pop(idx)
        self.data.pop(idx)
        self.pointers.pop(idx+1)

    def print_in_line(self):
        out="["
        for key in self.keys:
            out+=f"key: {key}, "
        out+="]"
        return out