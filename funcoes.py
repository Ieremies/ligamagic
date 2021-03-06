import objetos
import craw
import compra
import os
import csv

qualid = ["n/a", "M  ", "NM ", "SP ", "MP ", "HP ", "D  "]

def ler_deck():
    print("Fazendo o download dos preços...")
    lista = compra.compra()
    deck = open('deck.txt', 'r')
    aux = []
    for atual in deck:
        if atual.split() != []:
            lixo, nome = craw.pegar_nome(atual)
            aux.append(nome)
    deck.close()
    aux.sort()
    for atual in aux:
        craw.gerar_lista_de_ofertas_carta(atual, lista)
    return lista

def calcular(lista_comp):
    compra = []
    qtd = 0
    while not lista_comp.lista_de_cartas == []:
        if len(lista_comp.lista_de_cartas) == 1:
            qtd += 1
            if qtd == 2:
                print("\n\nInfelizmente a carta", lista_comp.lista_de_cartas[0].nome, "deve ser retirada do deck para que possamos calcular\n")
                raise ValueError
                break

        pont = lista_comp.calcula()
        maior_valor = 0
        loja = ''

        for key in pont.keys():
            if pont[key][0] >= maior_valor:
                maior_valor = pont[key][0]
                aux = pont[key][1]
                loja = key
        compra.append(loja)
        for i in aux:
            for j in lista_comp.lista_de_cartas:
                if i == j.nome:
                    lista_comp.lista_de_cartas.remove(j)
                    break
    return compra

def imprimir(lista_impr, frete):
    lista_impr.sort()
    valor_total = 0
    print('\n\n\n' + "Loja", " "*22, "Carta", ' '*28, 'Edição', ' '*21, 'Qualidade', ' '* 5, 'Diferença', ' '*4, "Preço", '\n')
    for i in lista_impr:
        print(i[0], ' '*(27 - len(i[0])), end='')
        print(i[1], ' '*(34 - len(i[1])), end='')
        print(i[2], ' '*(28 - len(i[2])), end='')
        print(qualid[i[3]], ' '*12, end='')
        print('%2.2f' %i[4], ' '*10, end ='')
        print('%2.2f' %i[5] )
        valor_total += i[5]

    lojas = 1
    for i in range(len(lista_impr)-1):
        if lista_impr[i][0] != lista_impr[i+1][0]:
            lojas += 1

    print()
    print(' '*106, 'valor total: R$ %2.2f' %valor_total)
    print(' '*106, '  com frete: R$ %2.2f' %(valor_total+(lojas*frete)))

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def salvar(lista, frete):
    valor_total=0
    with open("resultado.csv", "w", newline='') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["Loja ", "Carta ", 'Edição ','Qualidade ', 'Diferença ', "Preço "])

        for i in lista:
            writer.writerow([i[0], i[1], i[2], qualid[i[3]], '%2.2f' %i[4], '%2.2f' %i[5]])
            valor_total += i[5]
