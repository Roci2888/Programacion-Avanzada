import heapq

# Ejercicio 2.1: k-ésimo número más grande
def kth_largest(nums, k):
    # Usar nlargest y tomar el último
    if k > len(nums) or k <= 0:
        return None
    return heapq.nlargest(k, nums)[-1]

# Ejercicio 2.2: Mezclar k listas ordenadas
def merge_k_lists(lists):
    result = []
    heap = []
    
    # Inicializar heap con el primer elemento de cada lista
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    while heap:
        val, list_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        
        # Si hay más elementos en esta lista, agregar el siguiente
        if elem_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, elem_idx + 1))
    
    return result

# Ejercicio 2.3: k puntos más cercanos al origen
def k_closest_points(points, k):
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

# Pruebas
print("Ejercicio 2.1:", kth_largest([3,2,1,5,6,4], 2))  # 5
print("Ejercicio 2.2:", merge_k_lists([[1,4,5],[1,3,4],[2,6]]))  # [1,1,2,3,4,4,5,6]
print("Ejercicio 2.3:", k_closest_points([(1,2), (0,0), (3,4)], 2))  # [(0,0), (1,2)]