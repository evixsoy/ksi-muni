from heapq import heappop, heappush
from math import inf

#TODO udelat nejaky testy ale asi snad chill

def find_paths(n: int, edges: list[tuple[int, int, int]], queries: list[tuple[int, int, int]]) -> list[int]:
    paths = [[] for _ in range(n)]
    for start,end,distance in edges:
        paths[start].append((end,distance))
    
    #djikstra
    vysledek = []
    for start, end, max_path_length in queries:
        queue : list[tuple[int, int, int, int]] = [(start, 0, 0, inf)]
        visited = []
        temp_vysledky = []
        
        while queue:
            curr_node,distance,mesta,last_edge_length = heappop(queue)
            for temp_tuple in visited:
                if temp_tuple == (curr_node, distance):
                    continue
            visited.append((curr_node,distance))

            if curr_node == end:
                temp_vysledky.append(distance)

            if mesta <= max_path_length:
                for konc_vrchol, delka in paths[curr_node]:
                    if delka < last_edge_length and (mesta + 1) <= max_path_length:
                        heappush(queue,(konc_vrchol, distance + delka, mesta +1, delka))
            else:
                break
        try:
            vysledek.append(sorted(temp_vysledky)[0])
        except IndexError:
            vysledek.append(-1)
    return vysledek
                    



edges = [(0, 2, 10), (0, 1, 4), (1, 2, 3), (2, 1, 5), (1, 0, 6)] #(pocatecni vrchol, koncovy vrchol, delka hrany)   jednotlive propojeni mest mezi sebou
queries = [(0, 2, 1), (0, 2, 2), (2, 0, 3)] #(pocatecni vrchol,koncovy vrchol, maximalni pocet hran na ceste)   pozadavky losa losa
answers = find_paths(3, edges, queries)
print(answers)
# [10, 7, -1]   pocet hran na kazdou queries

edges = [(5, 1, 7), (1, 4, 6), (2, 0, 3), (3, 1, 4), (1, 2, 1), (2, 1, 9), (4, 1, 5), (5, 1, 2)]
queries = [(5, 1, 6), (3, 5, 160), (1, 3, 160)]
answers = find_paths(6, edges, queries)
print(answers)