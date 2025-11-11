from heapq import heappop, heappush
from math import inf
import random
import time

def find_last(tuple):
    return tuple[-1]
    
def find_paths(n: int, edges: list[tuple[int, int, int]], queries: list[tuple[int, int, int]]) -> list[int]:
    paths = [[] for _ in range(n)]
    for start,end,distance in edges:
        paths[start].append((end,distance))
    
    #sort paths
    for index in range(len(paths)):
        paths[index] = sorted(paths[index], key = find_last)

    #djikstra
    vysledek = []
    for start, end, max_path_length in queries:
        queue : list[tuple[int, int, int, int]] = [(start, 0, 0, inf)]
        visited = set()
        temp_vysledky = []
        
        while queue:
            curr_node,distance,mesta,last_edge_length = heappop(queue)
            if (curr_node, mesta) in visited:
                continue
            visited.add((curr_node,mesta))

            if curr_node == end:
                temp_vysledky.append(distance)
            
            if mesta <= max_path_length:
                for konc_vrchol, delka in paths[curr_node]:
                    if delka >= last_edge_length :
                        break
                    if delka < last_edge_length and (mesta + 1) <= max_path_length:
                        heappush(queue,(konc_vrchol, distance + delka, mesta +1, delka))
        if temp_vysledky:
            vysledek.append(min(temp_vysledky))
        else:
            vysledek.append(-1)
    return vysledek


def generate_test(sada_num: int, n: int, m: int, q: int):
    """Generuje testovací data podle parametrů ze sady"""
    # Generujeme hrany (edges)
    edges = []
    for i in range(m):
        start = random.randint(0, n-1)
        end = random.randint(0, n-1)
        while end == start:
            end = random.randint(0, n-1)
        distance = random.randint(1, 100000)
        edges.append((start, end, distance))
    
    # Generujeme queries
    queries = []
    for i in range(q):
        start = random.randint(0, n-1)
        end = random.randint(0, n-1)
        max_path = random.randint(1, n)
        queries.append((start, end, max_path))
    
    return edges, queries


def find_paths_slow_correct(n: int, edges: list[tuple[int, int, int]], queries: list[tuple[int, int, int]]) -> list[int]:
    """Pomalá, ale správná verze pro kontrolu - používá BFS s kontrolou všech cest"""
    from collections import deque
    
    paths = [[] for _ in range(n)]
    for start, end, distance in edges:
        paths[start].append((end, distance))
    
    results = []
    for start_node, end_node, max_cities in queries:
        # BFS - hledáme všechny možné cesty
        queue = deque([(start_node, 0, 0, float('inf'))])  # (current, distance, cities, last_edge)
        best_distance = float('inf')
        
        while queue:
            curr, dist, cities, last_edge = queue.popleft()
            
            if curr == end_node:
                best_distance = min(best_distance, dist)
                continue
            
            if cities >= max_cities:
                continue
            
            for next_node, edge_len in paths[curr]:
                if edge_len < last_edge:
                    queue.append((next_node, dist + edge_len, cities + 1, edge_len))
        
        results.append(best_distance if best_distance != float('inf') else -1)
    
    return results


def run_test_suite():
    """Spustí všechny testovací sady podle tabulky hodnocení"""
    # Definice testovacích sad podle tabulky
    test_sady = [
        {"sada": 1, "body": 1, "n": 8, "m": 20, "q": 10},
        {"sada": 2, "body": 1, "n": 16, "m": 50, "q": 10},
        {"sada": 3, "body": 1, "n": 25, "m": 200, "q": 10},
        {"sada": 4, "body": 1, "n": 25, "m": 200, "q": 5000},
        {"sada": 5, "body": 1, "n": 50, "m": 250, "q": 10},
        {"sada": 6, "body": 1, "n": 50, "m": 250, "q": 5000},
        {"sada": 7, "body": 1, "n": 100, "m": 1000, "q": 10},
        {"sada": 8, "body": 2, "n": 100, "m": 1000, "q": 5000},
    ]
    
    celkovy_cas = 0
    celkove_body = 0
    
    print("=" * 80)
    print("SPOUŠTĚNÍ TESTŮ PODLE HODNOCENÍ")
    print("=" * 80)
    
    for test_info in test_sady:
        sada = test_info["sada"]
        body = test_info["body"]
        n = test_info["n"]
        m = test_info["m"]
        q = test_info["q"]
        
        print(f"\nSADA {sada} (max {body} {'bod' if body == 1 else 'body'})")
        print(f"Parametry: n={n}, m={m}, q={q}")
        print("-" * 80)
        
        # Generujeme test
        edges, queries = generate_test(sada, n, m, q)
        
        # Pro malé sady (1-3, 5, 7) kontrolujeme správnost
        check_correctness = sada in [1, 2, 3, 5, 7]
        
        if check_correctness:
            print("Kontrola správnosti...")
            correct_result = find_paths_slow_correct(n, edges, queries)
        
        # Měříme čas tvého algoritmu
        start_time = time.time()
        result = find_paths(n, edges, queries)
        end_time = time.time()
        
        cas = end_time - start_time
        celkovy_cas += cas
        
        # Kontrola správnosti výsledků
        correctness_ok = True
        if check_correctness:
            if result == correct_result:
                print("✓ Výsledky jsou SPRÁVNÉ")
            else:
                print("✗ CHYBA: Výsledky jsou ŠPATNÉ!")
                correctness_ok = False
                # Najdeme první rozdíl
                for i, (r, c) in enumerate(zip(result, correct_result)):
                    if r != c:
                        print(f"  První rozdíl na indexu {i}: tvůj={r}, správně={c}")
                        print(f"  Query: start={queries[i][0]}, end={queries[i][1]}, max_cities={queries[i][2]}")
                        break
        
        # Kontrola časového limitu (10-15 sekund)
        time_ok = False
        if cas < 10:
            status = "✓ PASSED (čas)"
            time_ok = True
        elif cas < 15:
            status = "⚠ WARNING (blízko limitu)"
            time_ok = True
        else:
            status = "✗ FAILED (časový limit)"
        
        # Body se přidělují jen pokud je vše OK
        if time_ok and correctness_ok:
            celkove_body += body
        
        print(f"Čas: {cas:.3f}s {status}")
        print(f"Počet výsledků: {len(result)}")
        print(f"Ukázka prvních 5 výsledků: {result[:5]}")
    
    print("\n" + "=" * 80)
    print(f"CELKOVÝ ČAS: {celkovy_cas:.3f}s")
    print(f"ZÍSKANÉ BODY: {celkove_body} / 9")
    print("=" * 80)


if __name__ == "__main__":
    run_test_suite()