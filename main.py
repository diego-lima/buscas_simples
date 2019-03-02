from buscas import *
import os

"""
Comandos do interpretador de arquivo
"""
CIDADE = 'cidade'
ESTRADA = 'estrada'
ESTIMATIVA = 'estimativa'


def is_numeric(s):
    """
    Verifica se a string passada é um valor numérico
    """
    try:
        float(s)
        return True
    except (ValueError, TypeError):
        return False


class LeitorInput:
    """
    Serve para ler um arquivo que contém os nomes das cidades, as estradas
    e a estimativa de cada cidade até o destino. Essa classe vai ler o arquivo
    e gerar as cidades, as estradas e informar as estimativas para poder jogar
    nos algoritmos de busca.
    """
    input = None
    cidades = None
    estradas = None
    estimativas = None

    def __init__(self, dados):
        self.cidades = list()
        self.estradas = list()
        self.estimativas = dict()

        if not os.path.isfile(dados):
            print("cade o arquivo?")
            return
        f = open(dados)
        self.input = f.read()
        f.close()
        self.input = [x for x in self.input.split('\n') if x]

        for linha in self.input:
            comando, *tokens = linha.split(' ')
            if comando == CIDADE:
                self.cidades.append(Cidade(tokens[0]))

            elif comando == ESTRADA:
                origem = self.find(tokens[0])
                destino = self.find(tokens[1])
                custo = tokens[-1]
                custo = 0 if not is_numeric(custo) else float(custo)

                if all([origem, destino]):
                    self.estradas.append(Estrada(origem, destino, custo))

            elif comando == ESTIMATIVA:
                cidade = self.find(tokens[0])
                custo = tokens[-1]
                custo = 0 if not is_numeric(custo) else float(custo)

                if cidade:
                    self.estimativas[cidade] = custo
                    cidade.estimativa_fornecida = custo

    def find(self, nome: str):
        for cidade in self.cidades:
            if cidade.nome == nome:
                return cidade

        raise Exception("Cidade não encontrada: %s" % nome)

    @property
    def destino(self):
        for cidade in self.estimativas:
            if self.estimativas[cidade] == 0:
                return cidade

        raise Exception("Configure a cidade destino com estimativa 0!")


if __name__ == "__main__":
    arquivo = "grafo.txt"

    leitor = LeitorInput(arquivo)

    inicio = leitor.find('arad')

    print("---\n--- BREADTH-FIRST SEARCH\n---")
    retorno = breadth_first(inicio, leitor.destino)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- ITERATIVE DEEPENING SEARCH\n---")
    retorno = iterative_deepening(inicio, leitor.destino)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- GREEDY BEST FIRST SEARCH\n---")
    retorno = greedy_best_first(inicio, leitor.destino)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- A-STAR (A*)\n---")
    retorno = astar(inicio, leitor.destino)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- DIJKSTRA\n---")
    retorno = dijkstra(inicio, leitor.cidades)
    print("%s (custo %.0f)" % (retorno[leitor.destino], retorno[leitor.destino].custo))
