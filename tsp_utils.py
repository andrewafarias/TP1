from scipy.spatial.distance import cdist
from typing import List, Optional
import numpy as np
import sys

def parse_to_distance_matrix(filepath: str) -> np.ndarray:
    try:
        # Cria uma matrix nx2, cada linha uma coordenada de cidade. skiprows=1 pula primeira linha do arquivo
        cities: np.ndarray = np.loadtxt(filepath, skiprows=1, dtype=float) 
        dist_matrix: np.ndarray = cdist(cities, cities, metric='euclidean')
        return dist_matrix
    except FileNotFoundError:
        print(f'Erro: o arquivo {filepath} não foi encontrado.')
        sys.exit(1)
    except Exception as e:
        print(f'Erro desconhecido: {e}')
        sys.exit(1)


def calculate_total_distance(route: List[int], dist_matrix: np.ndarray, tour: bool = True) -> float:
    """
    Calcula a distância total de uma rota. O(n).
    """
    total_distance = 0.0
    
    for i in range(len(route)-1):
        total_distance += dist_matrix[route[i], route[i+1]]
    
    if tour:
        total_distance += dist_matrix[route[-1], route[0]]
    
    return total_distance


def swap_positions(route: List[int], pos1: int, pos2: int) -> None:
    """
    Troca duas cidades de posição.
    """
    aux = route[pos1]
    route[pos1] = route[pos2]
    route[pos2] = aux


def neighbors_distances(
        route: List[int],
        pos: int,
        dist_matrix: np.ndarray,
        ignore_edge: int = 0,
        tour: bool = True
        ) -> float:
    """
    Retorna a soma das distâncias para as cidades vizinhas.\n
    Considera o caso em que a rota representa um tour (i.e. route[0] é vizinha de route[n-1]).

    Args:
        ignore_edge: se < 0 ignora aresta a esquerda; se > 0 ignora a aresta a direita.
    """
    lastpos = len(route) - 1
    city = route[pos]
    delta = 0.0
    # Calcula a distância para a vizinha a esquerda se não estiver sendo ignorada.
    if not (ignore_edge < 0):
        if pos-1 >= 0:
            delta += dist_matrix[route[pos-1], city]
        elif tour:
            delta += dist_matrix[route[lastpos], city]
    
    # Calcula a distância para a vizinha a direita se não estiver sendo ignorada.
    if not (ignore_edge > 0):
        if pos+1 <= lastpos:
            delta += dist_matrix[city, route[pos+1]]
        elif tour:
            delta += dist_matrix[city, route[0]]

    return delta

def are_adjacent(route: List[int], pos1: int, pos2:int, tour: bool = True) -> int:
    """
    Returns:
    0 se não forem adjacentes \n
    -1 se pos2 estiver a esquerda de pos1 \n
    1 se pos2 estiver a direita de pos1 \n
    """
    ret = 0
    dif = pos2 - pos1
    
    if(abs(dif) == 1):
        ret = dif
    elif pos1 == 0 and pos2 == len(route)-1:
        ret = -1
    elif pos1 == len(route)-1 and pos2 == 0:
        ret = 1

    return ret


def swap_cities(
        route: List[int],
        pos1: int,
        pos2: int,
        current_total_distance: Optional[float] = None,
        dist_matrix: Optional[np.ndarray] = None,
        tour: bool = True
        ) -> Optional[float]:
    """
    Faz a troca de duas cidades e retorna a nova distância da rota em O(1). \n

    Returns:
        float: retorna a nova distância total se `current_total_distance` foi provida. \n
        None: se `current_total_distance` não foi provida \n

    Raises:
        ValueError: sse `current_total_distance` está definida então `dist_matrix` também deve estar.\n
    """
    
    if (current_total_distance is None) != (dist_matrix is None):
        raise ValueError('Erro: current_total_distance deve estar definida sse dist_matrix está definida')

    # Em um tour com apenas duas cidades, a troca não altera a distância total.
    if tour and len(route) <= 2 and current_total_distance is not None:
        swap_positions(route, pos1, pos2)
        return current_total_distance

    # Faz a inversão sem calcular distâncias
    if current_total_distance is None or dist_matrix is None:
        swap_positions(route, pos1, pos2)
        return None

    # === Remove as cidades da rota e depois as adiciona nos lugares da resultantes da troca (contando os deltas em cada passo) ===

    new_total_distance = current_total_distance
    pos1_adjacency_direction = are_adjacent(route, pos1, pos2) #Se pos2 é vizinho de pos1 então retorna para que direção é

    # Se forem vizinhos, ignora a aresta compartilhada uma vez
    new_total_distance += -(neighbors_distances(route, pos1, dist_matrix, pos1_adjacency_direction, tour))
    new_total_distance += -(neighbors_distances(route, pos2, dist_matrix, 0, tour))

    swap_positions(route, pos1, pos2)
    
    # Se forem vizinhos, ignroa a aresta compartilhada uma vez.    
    new_total_distance += neighbors_distances(route, pos1, dist_matrix, pos1_adjacency_direction, tour)
    new_total_distance += neighbors_distances(route, pos2, dist_matrix, 0, tour)

    return new_total_distance


if __name__ == '__main__':
    dist_matrix: np.ndarray = parse_to_distance_matrix('instancia.txt')
    for (i, ci) in enumerate(dist_matrix):
        print(f'Cidade {i}:', end=' ')
        for (j, cj) in enumerate(ci):
            print(f'(C{j} {cj:.2f})', end=' ')
        print()

    print('====================\n')
    
    print('Gerando rota de tamanho 4...')
    
    n: int = len(dist_matrix)
    permutation: List[int] = np.random.permutation(n).tolist()
    route: List[int] = [0, 1, 2, 3]

    print("Rota:", route)
    distance: float = calculate_total_distance(route, dist_matrix)
    print(f"Distância: {distance:.2f}")

    print("Trocando 1a cidade com 2a cidade...")
    
    new_distance = swap_cities(route, 0, 1, distance, dist_matrix)

    print("Nova rota:", route)
    print(f"Nova distância: {new_distance:.2f}")
    print(f"{calculate_total_distance(route, dist_matrix):.2f}")



