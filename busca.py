# coding: utf-8
from collections import deque as fila
from math import sqrt
from typing import Union


class Cidade:
    """
    Corresponde ao nó ou vértice.
    """
    # Tupla de posição
    coordenadas = None
    # String
    nome = None
    # Lista de Estradas
    estradas = None

    def __init__(self, nome: str, coordenadas: Union[list, tuple]):
        self.nome = nome
        self.coordenadas = []
        self.coordenadas.extend(coordenadas)
        self.estradas = []

    def conectar(self, estrada: 'Estrada'):
        self.estradas.append(estrada)

    @property
    def vizinhos(self):
        # outro pega a outra ponta da estrada.
        outro = lambda x: x.origem if x.origem.nome != self.nome else x.destino
        return list(map(outro, self.estradas))

    @property
    def vizinhos_ordenados(self):
        """
        Retorna os vizinhos em ordem crescente de distância euclidiana
        """
        # distancia = sqrt ( (x1-x2)^2 + (y1-y2)^2 )
        distancia = lambda x: sqrt( (x.coordenadas[0] - self.coordenadas[0])**2 + (x.coordenadas[1] - self.coordenadas[1])**2 )
        # outro pega a outra ponta da estrada.
        outro = lambda x: x.origem if x.origem.nome != self.nome else x.destino

        vizinhos = list(map(outro, self.estradas))

        return sorted(vizinhos, key=distancia)

    def __repr__(self):
        return self.nome


class Estrada:
    """
    Corresponde à aresta.
    """
    # Cidades origem e destino
    origem = None
    destino = None
    # String
    nome = None
    # Numerico
    comprimento = None

    def __init__(self, origem: Cidade, destino: Cidade, comprimento: float, nome=''):
        self.origem = origem
        self.destino = destino
        self.nome = nome
        self.comprimento = comprimento

        origem.conectar(self)
        destino.conectar(self)

    def __repr__(self):
        return "%s <-> %s: %.0f" % (self.origem, self.destino, self.comprimento)


def bfs(origem: Cidade, destino: Cidade):
    """
    Parte da origem, e realiza busca em largura até chegar no destino.
    """
    visitados = set()
    # Pares guarda o melhor vértice para se chegar naquele ponto:
    # {A: melhor vértice para se chegar em A, B: melhor vértice para se chegar em B, ...}
    pares = dict()
    fifo = fila()

    fifo.append(origem)

    while len(fifo):
        atual = fifo.popleft()
        visitados.add(atual.nome)
        for vizinho in atual.vizinhos:
            if vizinho.nome in visitados:
                continue
            else:
                fifo.append(vizinho)
                visitados.add(vizinho.nome)
                pares[vizinho.nome] = atual.nome

                if vizinho.nome == destino.nome:
                    # Chegamos ao destino: não vamos visitar mais ninguém
                    fifo.clear()
                    break

    """Para pegar o trajeto, a partir do destino, até o inicio
    """
    trajeto = []
    chave = destino.nome
    while chave in pares:
        trajeto.append(chave)
        chave = pares[chave]
    trajeto.append(origem.nome)

    print("Trajetória de %s até %s:" % (origem, destino))
    print(" -> ".join(trajeto[::-1]))

def best_first(origem: Cidade, destino: Cidade):
    """
    Parte da origem, e realiza best-first search (uma busca informada) até chegar no destino.
    A heurística é calcular a distância euclidiana entre as cidades.
    """
    visitados = set()
    # Pares guarda o melhor vértice para se chegar naquele ponto:
    # {A: melhor vértice para se chegar em A, B: melhor vértice para se chegar em B, ...}
    pares = dict()
    fifo = fila()

    fifo.append(origem)

    while len(fifo):
        atual = fifo.popleft()
        visitados.add(atual.nome)
        # a unica diferença da outra função é a linha seguinte:
        for vizinho in atual.vizinhos_ordenados:
            if vizinho.nome in visitados:
                continue
            else:
                fifo.append(vizinho)
                visitados.add(vizinho.nome)
                pares[vizinho.nome] = atual.nome

                if vizinho.nome == destino.nome:
                    # Chegamos ao destino: não vamos visitar mais ninguém
                    fifo.clear()
                    break

    """Para pegar o trajeto, a partir do destino, até o inicio
    """
    trajeto = []
    chave = destino.nome
    while chave in pares:
        trajeto.append(chave)
        chave = pares[chave]
    trajeto.append(origem.nome)

    print("Trajetória de %s até %s:" % (origem, destino))
    print(" -> ".join(trajeto[::-1]))


A = Cidade('A', (10, 10))       # C -- D
B = Cidade('B', (25, 10))       # | \   |
C = Cidade('C', (10, 20))       # |   \  |
D = Cidade('D', (20, 20))       # A -----B

Estrada(A, B, 12)
Estrada(A, C, 11)
Estrada(B, C, 7)
Estrada(B, D, 8)
Estrada(C, D, 10)

bfs(A, D)
best_first(A, D)
