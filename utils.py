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
        total_distance += dist_matrix[i, i+1]
    
    if tour:
        total_distance += dist_matrix[len(route)-1, 0]
    
    return total_distance

def route_inversion(
        route: List[int],
        pos1: int,
        pos2: int,
        current_total_distance: Optional[float] = None,
        dist_matrix: Optional[np.ndarray] = None,
        tour: bool = True
        ) -> Optional[float]:
    """
    Faz a inversão de duas cidades e retorna a nova distância da rota de forma ótima. \n

    Returns:
        float: retorna a nova distância total se `current_total_distance` foi provida. \n
        None: se `current_total_distance` foi provida \n

    Raises:
        NotImplemented: se for passada uma rota que não for um tour\n
        ValueError: sse `current_total_distance` está definida então `dist_matrix` também deve estar.\n
    """
    
    if not tour:
        raise NotImplemented('Erro: não foi implementado o cálculo' \
        ' para rotas que não são tours.')
    
    if (current_total_distance is None) != (dist_matrix is None):
        raise ValueError('Erro: current_total_distance deve estar definida sse dist_matrix está definida')
    
    lastpos = len(route)-1
    new_total_distance: Optional[float] = None

    def swap_cities():
        nonlocal pos1, pos2, route
        aux = route[pos1]
        route[pos1] = route[pos2]
        route[pos2] = aux
    
    def remove_city_distances(pos: int):
        nonlocal route, dist_matrix, new_total_distance, lastpos
        assert(new_total_distance is not None and dist_matrix is not None)
        
        # Calcula os deltas de uma remoção; de forma modular se for tour.
        if pos-1 >= 0:
            new_total_distance -= dist_matrix[pos-1, pos]
        elif tour:
            new_total_distance -= dist_matrix[lastpos, 0]
        
        if pos+1 <= lastpos:
            new_total_distance -= dist_matrix[pos, pos+1]
        elif tour:
            new_total_distance -= dist_matrix[pos, 0]
    
    def add_city_distances(pos: int):
        nonlocal route, dist_matrix, new_total_distance, lastpos
        assert(new_total_distance is not None and dist_matrix is not None)
        
        # Calcula os deltas de uma remoção; de forma modular se for tour.
        if pos-1 >= 0:
            new_total_distance += dist_matrix[pos-1, pos]
        elif tour:
            new_total_distance += dist_matrix[lastpos, 0]
        
        if pos+1 <= lastpos:
            new_total_distance += dist_matrix[pos, pos+1]
        elif tour:
            new_total_distance += dist_matrix[pos, 0]
    
    # Faz a inversão sem calcular distâncias
    if current_total_distance is None:
        swap_cities()
        return None

    # Remove as cidades da rota e depois as adiciona nos lugares da inversão (calculando os deltas)
    new_total_distance = current_total_distance
    remove_city_distances(pos1)
    remove_city_distances(pos2)

    swap_cities()

    add_city_distances(pos1)
    add_city_distances(pos2)


if __name__ == '__main__':
    dist_matrix: np.ndarray = parse_to_distance_matrix('instancia.txt')
    for (i, ci) in enumerate(dist_matrix):
        print(f'Cidade {i}:', end=' ')
        for (j, cj) in enumerate(ci):
            print(f'(C{j} {cj:.2f})', end=' ')
        print()