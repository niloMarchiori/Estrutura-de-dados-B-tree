from Models.node import Node
from Models.btree import B_tree

from sys import argv

def input(input_dir):
    with open(input_dir,'r') as input:
        lines=input.readlines()

    t=int(lines.pop(0))
    btree=B_tree(t)
    n=int(lines.pop(0))

    saida=""
    for i in range(n):
        line=lines[i].split()
        if line[0]=="I":
            key=int(line[1].split(',')[0])
            val=int(line[2])
            btree.btree_insert(key,val)
        
        if line[0]=="B":
            key=int(line[1])
            found,node,idx=btree.btree_find(key)
            if found:
                saida+="O REGISTRO ESTA NA ARVORE!\n"
            else:
                saida+="O REGISTRO NAO ESTA NA ARVORE!\n"
        
        if line[0]=="R":
            key=int(line[1].split(','))
            val=int(line[2])
            btree.btree_insert(key,val)
    saida+=btree.bsf_str()
    return saida

def save_output(output_dir,saida):
    with open(output_dir, 'w') as doc:
        doc.write(saida)
        
def main():
    # input_dir=argv[1]
    input_dir='entrada.txt'
    # output_dir=argv[2]
    output_dir='saida.txt'
    saida=input(input_dir)
    save_output(output_dir,saida)

main()