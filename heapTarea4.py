import time
import random
import heapq

def comparar_tiempos():
    # Generar datos de prueba
    datos = [random.randint(1, 1000) for _ in range(10000)]
    k = 10
    
    # Método con heap
    start = time.time()
    resultado_heap = heapq.nsmallest(k, datos)
    tiempo_heap = time.time() - start
    
    # Método con sorted
    start = time.time()
    resultado_sorted = sorted(datos)[:k]
    tiempo_sorted = time.time() - start
    
    print(f"Tiempo con heap: {tiempo_heap:.6f} segundos")
    print(f"Tiempo con sorted: {tiempo_sorted:.6f} segundos")
    
    if tiempo_heap > 0:
        ratio = tiempo_sorted / tiempo_heap
        if ratio > 1:
            print(f"Heap es {ratio:.2f}x más rápido")
        else:
            print(f"Sorted es {1/ratio:.2f}x más rápido")
    
    return resultado_heap, resultado_sorted

# Ejecutar comparación
comparar_tiempos()