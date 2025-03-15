from math import ceil

class Node():
    def __init__(self,t,keys:list=[],data:list=[],pointers:list=[],leaf:bool=True,parent=None):
        self._t=t #número máximo de filhos
        self._structure=[keys[:],     #Keys
                         data[:],     #Data
                         pointers[:]]   #Pointers
        self._n=0 #número atual de keys registradas nesse nó, não possui setter ou getter por ser
                  #um atributo que só é alterado a partir de outros métodos (protegido)
        self._leaf=leaf #informação booleana desse nó ser ou não folha

        self._parent=parent

        if keys:
            self._n=len(keys)
        if not pointers:
            self.pointers=[None for _ in range(self.n+1)]

    @property
    def t(self):
        '''Número máximo de filhos'''
        return self._t
    @property
    def n(self):
        '''Número atual de chaves registradas nesse nó'''
        return self._n
    
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

        self._n=len(keys)
    
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
        n=self._n
        if n>=t:
            raise f"Número de chaves excedeu o limite superior t={t}"
        if n<ceil(t/2)-1:
            raise f"Número de chaves é menor que o limite inferior t={ceil(t/2)-1}"
            
            
    def find(self,key:int):
        '''Args:
            key: chave a ser procurada no nó
        
        Return:
            found: booleano que informa se esse nó possui aquela chave
            node: ponteiro para o nó que possui/pode possuir a chave
            idx: o último índice de chaves visitado nesse nó cuja chave é menor que a procurada'''
        found=False
        for idx,curr_key in enumerate(self.keys):
            if curr_key==key: 
                found=True
                return found,self,idx #A chave se encontra, nesse nó, no índice idx
            if curr_key>key:  
                return found, self.pointers[idx],idx-1 #A chave não está nesse nó, podendo estar na subárvore da esquerda
        return found,self.pointers[idx+1],idx #A chave não está nesse nó, podendo estar na subárvore da direita
    
    def insert(self,key,val,idx,right_node=None):
        '''Atualiza a chave e o valor na posição idx, deslocando os elementos para a direita, sem alterar o tamanho da lista'''
        self.keys.append(None)
        
        self.keys.insert(idx,key)
        self.data.insert(idx,val)
        self.pointers.insert(idx+1,right_node)

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

        while self.n-1>ceil(t/2)-2:
            self.pointers.pop()
            self.keys.pop()
            self.data.pop()
            self._n-=1
       
        return right_node


