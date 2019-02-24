from typing import Union
import heapq


class FilaPrioridade:
    """
    Essa classe serve apenas para encapsular a implementação nativa python heapq.
    Isso porque a heapq é implementada de um jeito muito tosco.
    """
    heap = None

    def __init__(self, heap: list):
        # Vamos copiar o input para não mexer nele
        self.heap = list()
        self.heap.extend(heap)
        heapq.heapify(self.heap)

    def add(self, item):
        heapq.heappush(self.heap, item)

    def pop(self):
        if len(self.heap):
            return heapq.heappop(self.heap)
        else:
            return None

"""
Tipos de implementação. Se MANHATTAN, as estimativas (heurística) são feitas
com base nas coordenadas das cidades. Se ARQUIVO, as estimativas não são calculadas,
então devem ser fornecidas pelo problema.
"""
MANHATTAN = 'manhattan'
ARQUIVO = 'arquivo'


class Cidade:
    """
    Essa classe corresponde ao nó do grafo.
    Ela conhece seus vizinhos através de suas estradas
    E conhece a distância a cada um deles, também através das estradas
    """
    # coordenadas cartesianas
    coordenadas = None
    # estradas para cidades vizinhas
    estradas = None
    # identificador unico
    nome = None
    # Se vamos calcular estimativas (distancia manhattan) ou apenas consultar
    # de dados fornecidos
    implementacao = None
    # Estimativa informada pelo problema
    estimativa_fornecida = None

    def __init__(self, nome: str, coordenadas: Union[list, tuple] = (0, 0), implementacao: str = ARQUIVO):
        self.nome = nome
        self.coordenadas = coordenadas
        self.implementacao = implementacao
        self.estimativa_fornecida = 0

        self.estradas = list()

    def conectar(self, estrada: 'Estrada'):
        """Serve para ser chamada na criação de uma estrada.
        Ao criar a estrada, o nó é informado da existência dessa nova estrada"""
        self.estradas.append(estrada)

    def distancia_estimada(self, vizinho: 'Cidade'):
        """Distância Manhattan entre as duas cidades"""
        return abs(self.coordenadas[0] - vizinho.coordenadas[0]) + abs(self.coordenadas[1] - vizinho.coordenadas[1])

    def estimativa(self, vizinho: 'Cidade'):
        """Retorna a estimativa de distância entre esta cidade e o vizinho.
        Se implementacao = 'manhattan', retornamos a distancia manhattan.
        Se nao, vamos consultar o dado fornecido (aceitamos a estimativa dado no problema)
        """
        if self.implementacao == MANHATTAN:
            return self.distancia_estimada(vizinho)
        else:
            return self.estimativa_fornecida

    @property
    def vizinhos(self):
        """
        Retorna a lista de cidades vizinhas.
        """
        return list(map(lambda estrada: estrada.vizinho(self), self.estradas))

    @property
    def vizinhos_com_custo(self):
        """
        Retorna a lista de cidades vizinhas com custo até elas no formato
        [ [custo0, vizinho0], [custo1, vizinho1], ... ]
        """
        return list(map(lambda estrada: [estrada.comprimento, estrada.vizinho(self)], self.estradas))

    def vizinhos_com_estimativa(self, destino: 'Cidade'):
        """
        Retorna a lista de cidades vizinhas com estimativa
        até o destino associada no formato
        [ [estimativa0, vizinho0], [estimativa1, vizinho1], ... ]
        """
        return list(map(lambda vizinho: [vizinho.estimativa(destino), vizinho], self.vizinhos))

    def __repr__(self):
        """Serve para aparecer o nome da cidade quando tentar printar"""
        return self.nome

    def __hash__(self):
        """Serve para que a cidade possa ser usada como chave de dicionário ou de conjunto(set)."""
        return hash(self.nome)

    def __eq__(self, other):
        """Serve para poder fazer comparação de igualdade da cidade com outra cidade, ou com uma string."""
        if isinstance(other, str):
            return other == self.nome
        elif isinstance(other, Cidade):
            return other.nome == self.nome


class Estrada:
    """Essa classe corresponde à aresta do grafo.
    Ela conecta duas cidades, e tem um comprimento(custo)."""
    # identificador unico
    nome = None
    # cidades de origem e destino
    origem = None
    destino = None
    # custo
    comprimento = None

    def __init__(self, origem: Cidade, destino: Cidade, comprimento: Union[int, float] = 0, nome=None):
        self.origem = origem
        self.destino = destino
        self.comprimento = comprimento
        self.nome = nome

        origem.conectar(self)
        destino.conectar(self)

    def vizinho(self, cidade):
        """
        Retorna o vizinho da cidade passada.
        Se uma estrada conecta natal a mossoró, se você passar Natal, eu retorno mossoró
        Se você passar mossoró, eu retorno natal.
        """

        return self.origem if self.origem.nome != cidade.nome else self.destino

    def __repr__(self):
        """Serve para poder printar a estrada, mostrando a origem, o destino, o nome (se tiver) e o comprimento"""
        nome = "" if not self.nome else " (%s)" % self.nome
        return "%s <-> %s%s: %.0fkm" % (self.origem, self.destino, nome, self.comprimento)


class Trilha:
    """Essa classe serve para podermos lembrar do caminho percorrido durante as buscas.
    Um objeto Trilha sempre lembra do passo anterior, e lembra do custo acumulado até o ponto atual."""
    # trilha
    anterior = None
    # cidade
    cidade = None
    # custo acumulado
    custo = None

    def __init__(self, cidade: Cidade, anterior: 'Trilha' = None, custo: Union[int, float] = 0):
        self.cidade = cidade
        self.anterior = anterior
        self.custo = custo

    def __repr__(self):
        """Serve para podermos printar a trilha. É feito recursivamente: começamos
        do ponto atual, e vamos printando até chegar na origem."""
        if self.anterior:
            return "%s -> %s" % (self.anterior, self.cidade)
        return str(self.cidade)


if __name__ == "__main__":
    A = Cidade('natal', (0, 0))
    B = Cidade('mossoro', (0, 10))
    
    print("Cidade:", A)
    print("Estrada:", Estrada(A, B, 10, "BR101"))
    print("Vizinhos de natal:", A.vizinhos)
    print(A == 'natal')
    print(A == 'mossoro')
    print(A == A)
    print(A == B)
