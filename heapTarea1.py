import heapq
from collections import Counter

# Problema 1: K números más pequeños
def k_smallest_numbers(arr, k):
    if k <= 0:
        return []
    return heapq.nsmallest(k, arr)

# Problema 2: K elementos más frecuentes
def k_most_frequent(arr, k):
    if k <= 0:
        return []
    
    # Contar frecuencias
    freq = Counter(arr)
    
    # Usar heap para encontrar los k más frecuentes
    # heapq.nlargest usa heap internamente
    return heapq.nlargest(k, freq.keys(), key=freq.get)

# Ejemplos
print("Problema 1:", k_smallest_numbers([4, 2, 7, 1, 9, 3], 3))  # [1, 2, 3]
print("Problema 2:", k_most_frequent([1, 1, 1, 2, 2, 3], 2))    # [1, 2]