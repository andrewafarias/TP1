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


def calculate_total_distance(route: List[int], dist_matrix: np.ndarray, tour: bool) -> float:
    total_distance = 0.0
    
    for i in range(len(route)-1):
        total_distance += dist_matrix[route[i], route[i+1]]
    
    if tour:
        total_distance += dist_matrix[route[-1], route[0]]
    
    return total_distance


def swap_positions(route: List[int], pos1: int, pos2: int) -> None:
    aux = route[pos1]
    route[pos1] = route[pos2]
    route[pos2] = aux


def remove_city_distances(
        route: List[int],
        pos: int,
        dist_matrix: np.ndarray,
        current_total_distance: float,
        tour: bool = True
        ) -> float:
    lastpos = len(route) - 1
    city = route[pos]

    # Calcula os deltas de uma remoção; de forma modular se for tour.
    if pos-1 >= 0:
        current_total_distance -= dist_matrix[route[pos-1], city]
    elif tour:
        current_total_distance -= dist_matrix[route[lastpos], city]

    if pos+1 <= lastpos:
        current_total_distance -= dist_matrix[city, route[pos+1]]
    elif tour:
        current_total_distance -= dist_matrix[city, route[0]]

    return current_total_distance


def add_city_distances(
        route: List[int],
        pos: int,
        dist_matrix: np.ndarray,
        current_total_distance: float,
        tour: bool = True
        ) -> float:
    lastpos = len(route) - 1
    city = route[pos]

    # Calcula os deltas de uma remoção; de forma modular se for tour.
    if pos-1 >= 0:
        current_total_distance += dist_matrix[route[pos-1], city]
    elif tour:
        current_total_distance += dist_matrix[route[lastpos], city]

    if pos+1 <= lastpos:
        current_total_distance += dist_matrix[city, route[pos+1]]
    elif tour:
        current_total_distance += dist_matrix[city, route[0]]

    return current_total_distance

def swap_cities(
        route: List[int],
        pos1: int,
        pos2: int,
        current_total_distance: Optional[float] = None,
        dist_matrix: Optional[np.ndarray] = None,
        tour: bool = True
        ) -> Optional[float]:
    """
    Faz a troca de duas cidades e retorna a nova distância da rota de forma ótima. \n

    Returns:
        float: retorna a nova distância total se `current_total_distance` foi provida. \n
        None: se `current_total_distance` foi provida \n

    Raises:
        ValueError: sse `current_total_distance` está definida então `dist_matrix` também deve estar.\n
    """
    
    if (current_total_distance is None) != (dist_matrix is None):
        raise ValueError('Erro: current_total_distance deve estar definida sse dist_matrix está definida')
    
    # Faz a inversão sem calcular distâncias
    if current_total_distance is None or dist_matrix is None:
        swap_positions(route, pos1, pos2)
        return None

    # Remove as cidades da rota e depois as adiciona nos lugares da inversão (contando os deltas em cada passo)
    # Obs: o erro que ocorre na fase de remoção no caso de posições adjacentes é compensado na fase de adição.
    new_total_distance = current_total_distance
    new_total_distance = remove_city_distances(route, pos1, dist_matrix, new_total_distance, tour)
    new_total_distance = remove_city_distances(route, pos2, dist_matrix, new_total_distance, tour)
    if abs(pos1 - pos2) == 1:
        new_total_distance -= dist_matrix[route[pos1], route[pos2]]

    swap_positions(route, pos1, pos2)

    new_total_distance = add_city_distances(route, pos1, dist_matrix, new_total_distance, tour)
    new_total_distance = add_city_distances(route, pos2, dist_matrix, new_total_distance, tour)

    return new_total_distance


if __name__ == '__main__':
    dist_matrix: np.ndarray = parse_to_distance_matrix('instancia.txt')
    for (i, ci) in enumerate(dist_matrix):
        print(f'Cidade {i}:', end=' ')
        for (j, cj) in enumerate(ci):
            print(f'(C{j} {cj:.2f})', end=' ')
        print()