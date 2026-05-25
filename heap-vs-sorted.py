import heapq
import time
import random

def comparar_heap_vs_sorted():
    # Generar datos de prueba
    datos = [random.randint(1, 10000) for _ in range(50000)]
    k = 10
    
    # Método con Heap
    start = time.time()
    resultado_heap = heapq.nsmallest(k, datos)
    tiempo_heap = time.time() - start
    
    # Método con Sorted
    start = time.time()
    resultado_sorted = sorted(datos)[:k]
    tiempo_sorted = time.time() - start
    
    print(f"Tiempo Heap: {tiempo_heap:.6f} seg")
    print(f"Tiempo Sorted: {tiempo_sorted:.6f} seg")
    print(f"Heap es {tiempo_sorted/tiempo_heap:.2f}x más rápido")
    
    return resultado_heap, resultado_sorted

comparar_heap_vs_sorted()