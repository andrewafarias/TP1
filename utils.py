import numpy as np
from scipy.spatial.distance import cdist
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

if __name__ == '__main__':
    dist_matrix: np.ndarray = parse_to_distance_matrix('instancia.txt')
    for (i, ci) in enumerate(dist_matrix):
        print(f'Cidade {i}:', end=' ')
        for (j, cj) in enumerate(ci):
            print(f'(C{j} {cj:.2f})', end=' ')
        print()
