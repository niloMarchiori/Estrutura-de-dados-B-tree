class Teste():
    def __init__(self,lista):
        self._lista=lista
        self._n=1
    @property
    def lista(self):
        return self._lista
    @property
    def n(self):
        return self._n
    
    @lista.setter
    def lista(self,lista):
        self.lista=lista

    @n.setter
    def n(self,n):
        self._n=n

    def __str__(self):
        saida=""
        for i in self.lista:
            saida+=str(i)+" "
        return saida
    
    def teste_estatico(Teste,i):
        return Teste.lista[i]
    
lista=[1,2,3,4,5]
teste=Teste(lista)
teste.n+=1
print(teste.n)