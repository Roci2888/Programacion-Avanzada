import heapq

def top_k_products(products, k):
    # products es lista de tuplas (nombre, puntaje)
    # Usar nlargest para obtener los k con mayor puntaje
    top = heapq.nlargest(k, products, key=lambda x: x[1])
    # Devolver solo los nombres
    return [product[0] for product in top]

# Ejemplo
productos = [("Laptop", 95), ("Mouse", 80), ("Teclado", 85)]
print("Top productos:", top_k_products(productos, 2))  # ['Laptop', 'Teclado']