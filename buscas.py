from classes import *
from collections import deque as fila


def breadth_first(origem: Cidade, destino: Cidade):
    """
    Parte da origem, e realiza busca em largura até chegar no destino.

    :return: Trilha
    """
    visitados = set()
    trilhas = {origem: Trilha(origem)}
    fifo = fila()

    fifo.append(origem)

    while len(fifo):
        atual = fifo.popleft()
        print("visitando ", atual)

        if atual == destino:
            break

        if atual not in visitados:
            visitados.add(atual)

        trilha_atual = trilhas[atual]

        for vizinho_com_custo in atual.vizinhos_com_custo:
            vizinho = vizinho_com_custo[1]
            if vizinho in visitados or vizinho in fifo:
                continue

            fifo.append(vizinho)
            visitados.add(vizinho)
            nova_trilha = Trilha(vizinho, trilha_atual, vizinho_com_custo[0] + trilha_atual.custo)
            trilhas[vizinho] = nova_trilha

    return trilhas.get(destino)


def greedy_best_first(origem: Cidade, destino: Cidade):
    """
    Parte da origem, e realiza greedy best first search até chegar no destino.

    :return: Trilha
    """
    visitados = set()
    trilhas = {origem: Trilha(origem)}
    fifo = fila()

    fifo.append(origem)

    while len(fifo):
        atual = fifo.popleft()
        print("visitando ", atual)

        if atual == destino:
            break

        if atual not in visitados:
            visitados.add(atual)

        visitados.add(atual)
        trilha_atual = trilhas[atual]

        """
        A única diferença deste para a busca em largura é que ordenamos os vizinhos pela distância
        até o destino. Assim, sempre vamos preferir ir para o próximo vizinho que parece estar mais
        próximo do destino
        """
        vizinhos_ordenados = sorted(atual.vizinhos_com_custo, key=lambda x: x[1].distancia_estimada(destino))
        for vizinho_com_custo in vizinhos_ordenados:
            vizinho = vizinho_com_custo[1]
            if vizinho in visitados or vizinho in fifo:
                continue

            fifo.append(vizinho)
            visitados.add(vizinho)
            nova_trilha = Trilha(vizinho, trilha_atual, vizinho_com_custo[0] + trilha_atual.custo)
            trilhas[vizinho] = nova_trilha

    return trilhas.get(destino)


def depth_limited(origem, destino, limite=0):
    """
    Depth Limited Search (DLS): busca em profundidade (depth-first search, DFS)
    com limite de profundidade. Se limite = 0, torna-se DFS.

    :return: Trilha
    """
    visitados = set()
    custo_acumulado = {origem: 0}

    def visitar(cidade: Cidade, trilha: Trilha = None, nivel=1):
        """Parte recursiva da busca em profundidade. É definida aqui para
        poder ter acesso ao destino, a visitados e a custo_acumulado.
        Se nivel for igual a limite, a busca é interrompida
        """

        print("visitando ", cidade)

        # Serve apenas pra permitir que o usuário não precise passar uma trilha no começo
        if trilha is None:
            trilha = Trilha(cidade)

        """ Condições de parada
        Se encontramos o destino
        Se já visitamos a cidade
        Se alcançamos o limite de profundidade
        """
        if cidade == destino:
            return trilha
        if cidade in visitados:
            return None
        if nivel >= limite and limite:
            return None

        visitados.add(cidade)

        """
        Atualizamos o custo acumulado até cada vizinho: calculamos o novo custo.
        Se o novo custo for menor que o custo atual, atualizamos o custo
        """
        custo_atual = custo_acumulado[cidade]
        for vizinho in cidade.vizinhos_com_custo:
            novo_custo = custo_atual + vizinho[0]
            if vizinho[1] not in custo_acumulado or novo_custo < custo_acumulado[vizinho[1]]:
                custo_acumulado[vizinho[1]] = novo_custo

        """
        Para cada vizinho (primeiro o da direita, último o da esquerda), aumente
        a profundidade. Se um dos filhos levou ao destino, os filhos seguintes são ignorados
        """

        for vizinho in cidade.vizinhos:
            resultado = visitar(vizinho, Trilha(vizinho, trilha, custo_acumulado[vizinho]), nivel+1)
            if resultado:
                return resultado
        return None

    return visitar(origem)


def iterative_deepening(origem, destino, limite=100):
    """
    Realiza Depth Limited Search com limites cada vez maiores, até chegar na resposta.
    """
    for d in range(1, limite + 1):
        print("Tentando com profundidade máxima de ", d)
        resultado = depth_limited(origem, destino, d)
        if resultado:
            return resultado


def astar(origem, destino):
    """
    Realiza busca de uma trilha entre origem e destino considerando o caminho
    percorrido e a heurística, que é a estimativa de distância até o destino

    :return: Trilha
    """
    visitados = set()
    custo_acumulado = {origem: 0}

    def visitar(cidade: Cidade, trilha: Trilha = None):
        """Parte recursiva da busca em profundidade. É definida aqui para
        poder ter acesso ao destino, a visitados e a custo_acumulado.
        """

        print("visitando ", cidade)

        # Serve apenas pra permitir que o usuário não precise passar uma trilha no começo
        if trilha is None:
            trilha = Trilha(cidade)

        """ Condições de parada
        Se encontramos o destino
        Se já visitamos a cidade
        """
        if cidade == destino:
            return trilha
        if cidade in visitados:
            return None

        visitados.add(cidade)

        """
        Atualizamos o custo acumulado até cada vizinho: calculamos o novo custo.
        Se o novo custo for menor que o custo atual, atualizamos o custo
        """
        custo_atual = custo_acumulado[cidade]
        for vizinho in cidade.vizinhos_com_custo:
            novo_custo = custo_atual + vizinho[0]
            if vizinho[1] not in custo_acumulado or novo_custo < custo_acumulado[vizinho[1]]:
                custo_acumulado[vizinho[1]] = novo_custo

        """
        Montamos a fila de prioridade, onde a primeira é aquela que tem o menor custo total
        e o custo total é o custo até a cidade + a estimativa do que falta até o destino
        """
        fila_prioridade = cidade.vizinhos_com_estimativa(destino)
        for c in fila_prioridade:
            c[0] = c[0] + custo_acumulado[c[1]]

        fila_prioridade = FilaPrioridade(fila_prioridade)

        """
        Para cada vizinho (em ordem de prioridade, ou seja, melhores candidatos primeiro)
        Se um dos filhos levou ao destino, os filhos seguintes são ignorados
        """
        while fila_prioridade:
            vizinho = fila_prioridade.pop()

            if not vizinho:
                break
            else:
                vizinho = vizinho[1]

            if vizinho in visitados:
                continue

            resultado = visitar(vizinho, Trilha(vizinho, trilha, custo_acumulado[vizinho]))

            if resultado:
                return resultado
        return None

    return visitar(origem)
    

if __name__ == "__main__":
    A = Cidade('A', (0, 0), implementacao="manhattan")    # C -- D
    B = Cidade('B', (0, 15), implementacao="manhattan")   # | \   |
    C = Cidade('C', (10, 0), implementacao="manhattan")   # |   \  |
    D = Cidade('D', (10, 10), implementacao="manhattan")  # A -----B

    distancias = {
        "ab": 17,
        "ac": 12,
        "bc": 1,
        "bd": 13,
        "cd": 11
    }
    Estrada(A, B, distancias["ab"])
    Estrada(A, C, distancias["ac"])
    Estrada(B, C, distancias["bc"])
    Estrada(B, D, distancias["bd"])
    Estrada(C, D, distancias["cd"])

    print("\n---\nentre parênteses, temos: (custo estimado, custo real)")
    print("Mapa:")
    print("             (10,%d)" % distancias["cd"])
    print("        C-------------D")
    print("        | |           |")
    print("        |   |         |")
    print("        |     |        |")
    print("(10,%d) |       |       | (11, %d)" % (distancias["ac"], distancias["bd"]))
    print("        | (18,%d) |      |" % distancias["bc"])
    print("        |           |    |")
    print("        |             |  |")
    print("        A----------------B")
    print("             (15,%d)" % distancias["ab"])
    print("\nBuscando um caminho entre %s e %s\n" % (A, D))

    print("---\n--- BREADTH-FIRST SEARCH\n---")
    retorno = breadth_first(A, D)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- ITERATIVE DEEPENING SEARCH\n---")
    retorno = iterative_deepening(A, D)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- GREEDY BEST FIRST SEARCH\n---")
    retorno = greedy_best_first(A, D)
    print("%s (custo %.0f)" % (retorno, retorno.custo))

    print("---\n--- A-STAR (A*)\n---")
    retorno = astar(A, D)
    print("%s (custo %.0f)" % (retorno, retorno.custo))
