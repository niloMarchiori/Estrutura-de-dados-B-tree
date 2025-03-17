import graphviz

def plot_tree():
    tree = graphviz.Digraph(format='png')
    
    # Adicionando nós (vértices)
    tree.node('1', 'Raiz')
    tree.node('BZ', 'Filho 1')
    tree.node('CZ', 'Filho 2')
    tree.node('DZ', 'Neto 1')
    tree.node('Ez', 'Neto 2')
    
    # Adicionando arestas (conexões entre os nós)
    tree.edge('1', 'BZ')
    tree.edge('1', 'CZ')
    tree.edge('BZ', 'DZ')
    tree.edge('BZ', 'Ez')
    
    # Renderizar e salvar a árvore como imagem
    tree.render('tree', format='png', cleanup=True)
    print("Imagem gerada: tree.png")

if __name__ == "__main__":
    plot_tree()
