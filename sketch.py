from typing import List
import numpy as np

Route = List[int]

class Frog:
    def __init__(self, dist_matrix: np.ndarray, route: Route, ) -> None:
        self.route = route

    def calculate_distance(self, dist_matrix: np.ndarray):
        pass

def main():
    m: int # O número de memeplexes
    n: int # O número de sapos por memeplexes



