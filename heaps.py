import heapq
from collections import Counter
import random
import time


def k_smallest(nums, k):
    if k <= 0:
        return []
    return heapq.nsmallest(k, nums)

numeros = [4, 2, 7, 1, 9, 3, 8, 5]
k = 3
resultado = k_smallest(numeros, k)
print(f"Los {k} números más pequeños: {resultado}")                                    

def k_most_frequent(nums, k):
    if k <= 0:
        return []
 
    frecuencias = Counter(nums)

    return heapq.nlargest(k, frecuencias.keys(), key=frecuencias.get)

numeros = [1, 1, 1, 2, 2, 3]
k = 2
resultado = k_most_frequent(numeros, k)
print(f"Los {k} elementos más frecuentes: {resultado}")                                                
from collections import Counter

def kth_largest(nums, k):
    return heapq.nlargest(k, nums)[-1]

def merge_k_lists(lists):
    return list(heapq.merge(*lists))

def k_closest_points(points, k):
    return heapq.nsmallest(k, points, key=lambda p: p[0]**2 + p[1]**2)

print(f"kth_largest([3,2,1,5,6,4], 2) = {kth_largest([3,2,1,5,6,4], 2)}")  # 5

print(f"merge_k_lists([[1,4,5],[1,3,4],[2,6]]) = {merge_k_lists([[1,4,5],[1,3,4],[2,6]])}")

print(f"k_closest_points([(1,2),(0,0),(3,4)], 2) = {k_closest_points([(1,2),(0,0),(3,4)], 2)}")

def top_k_products(products, k):
    # products es lista de tuplas (nombre, puntaje)
    # Usar nlargest para obtener los k con mayor puntaje
    top = heapq.nlargest(k, products, key=lambda x: x[1])
    # Devolver solo los nombres
    return [product[0] for product in top]

# Ejemplo
productos = [("Laptop", 95), ("Mouse", 80), ("Teclado", 85)]
print("Top productos:", top_k_products(productos, 2))  # ['Laptop', 'Teclado']
      # ========== MEDICIÓN ==========
def medir(func, *args):
    start = time.perf_counter()
    result = func(*args)
    return time.perf_counter() - start

# Datos de prueba

datos_grandes = [random.randint(1, 100000) for _ in range(100000)]
listas_ordenadas = [sorted([random.randint(1, 1000) for _ in range(1000)]) for _ in range(50)]
puntos = [(random.randint(-1000, 1000), random.randint(-1000, 1000)) for _ in range(50000)]
productos = [(f"P{i}", random.randint(1, 100)) for i in range(50000)]

print("=" * 60)
print("MEDICIONES DE TIEMPO (Heap)")
print("=" * 60)

print(f"\n1. K números más pequeños (n=100000, k=10): {medir(k_smallest, datos_grandes, 10)*1000:.3f} ms")
print(f"2. K más frecuentes (n=100000, k=5): {medir(k_most_frequent, datos_grandes, 5)*1000:.3f} ms")
print(f"3. K-ésimo más grande (n=100000, k=10): {medir(kth_largest, datos_grandes, 10)*1000:.3f} ms")
print(f"4. Mezclar listas (50 listas x 1000 elems): {medir(merge_k_lists, listas_ordenadas)*1000:.3f} ms")
print(f"5. Puntos cercanos (n=50000, k=10): {medir(k_closest_points, puntos, 10)*1000:.3f} ms")
print(f"6. Top productos (n=50000, k=10): {medir(top_k_products, productos, 10)*1000:.3f} ms")

print("\n" + "=" * 60)