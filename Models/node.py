from math import ceil

class Node():
    def __init__(self,t,keys=[],data=[],pointers=[],leaf=True,parent=None):
        self._t=t #número máximo de filhos
        self._structure=[[None for _  in range(t-1)],     #Keys
                         [None for _  in range(t-1)],     #Data
                         [None for _  in range(t)]]   #Pointers
        self._n=0 #número atual de keys registradas nesse nó, não possui setter ou getter por ser
                  #um atributo que só é alterado a partir de outros métodos (protegido)
        self._leaf=leaf #informação booleana desse nó ser ou não folha

        self._parent=parent

        if keys:
            self.keys=keys
            self._n=len(keys)

        if data:
            self.data=data

        if pointers:
            self.pointers=pointers
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
            bool: informa se esse nó possui aquela chave
            pointer: ponteiro para o nó que possui/pode possuir a chave
            idx: o último índice de chaves visitado nesse nó cuja chave é menor que a procurada'''
        
        for idx,curr_key in enumerate(self.keys):
            if curr_key==key: 
                return True,self,idx-1 #A chave se encontra, nesse nó, no índice i
            if curr_key>key:  
                return False, self.pointers[idx],idx-1 #A chave não está nesse nó, podendo estar no filho da esquerda ou abaixo dele
        return False,self.pointers[idx+1],idx #A chave não está nesse nó, podendo estar no filho da direita ou abaixo dele
    
    def insert(self,key,val,idx,left_node=None,right_node=None):
        '''Atualiza a chave e o valor na posição idx e também o apontamento esquerdo e direito dessa chave'''
        self.keys[idx]=key
        self.data[idx]=val
        self.pointers[idx]=left_node
        self.pointers[idx+1]=right_node

    def split(self):
        '''Divide o nó atual em dois nós, cada um com metade das chaves
        
        retuurn:
            left_node: nó resultante da primeira metade da divisão das chaves
            right_node: nó resultante da segunda metade da divisão das chaves'''

        t=self.t
        keys=self.keys
        data=self.data
        pointers=self.pointers

        left_node=Node(t=t,keys=keys[:ceil(t/2)-1],data=data[:ceil(t/2)-1],pointers=pointers[:ceil(t/2)-1],parent=self.parent)
        right_node=Node(t=t,keys=keys[ceil(t/2):],data=data[ceil(t/2):],pointers=pointers[ceil(t/2):],parent=self.parent)
        
        del self
        return left_node,right_node


