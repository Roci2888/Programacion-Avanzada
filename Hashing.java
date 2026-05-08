package org.example;
import java.util.*;

public class Hashing {

    // Clase que representa un par (clave, valor) almacenado en la tabla hash
    static class Pair {
        String key;   // Clave del elemento
        int value;    // Valor asociado a la clave

        // Constructor para crear un nuevo par
        Pair(String key, int value) {
            this.key = key;
            this.value = value;
        }
    }

    // Clase que implementa la tabla hash con encadenamiento separado
    static class HashTableChaining {
        private List<List<Pair>> table;  // Tabla: array de listas para manejo de colisiones
        private int size;                // Tamaño de la tabla (número de buckets)
        private int count;               // Número total de elementos almacenados
        private int collisions;          // Contador de colisiones (RF6)
        private String hashStrategy;     // Estrategia de hash: "sum" o "polynomial"

        // Constructor: inicializa la tabla con listas vacías
        public HashTableChaining(int size, String hashStrategy) {
            this.size = size;
            this.hashStrategy = hashStrategy;
            this.count = 0;
            this.collisions = 0;
            this.table = new ArrayList<>();
            // Crear una lista enlazada vacía para cada bucket
            for (int i = 0; i < size; i++) {
                table.add(new LinkedList<>());
            }
        }

        // RF4: Función hash por suma de caracteres
        // Calcula el índice sumando los códigos Unicode de cada carácter y aplicando módulo
        private int hashSum(String key) {
            int sum = 0;
            for (int i = 0; i < key.length(); i++) {
                sum += key.charAt(i);  // Suma el valor Unicode del carácter
            }
            return Math.floorMod(sum, size);  // Módulo para asegurar índice dentro de la tabla
        }

        // RF5: Función hash polinomial con base 31
        // Distribuye mejor las claves ponderando la posición de los caracteres
        private int hashPolynomial(String key) {
            int h = 0;
            int base = 31;  // Base primo para mejor distribución
            for (int i = 0; i < key.length(); i++) {
                // h = (h * base + carácter) módulo tamaño
                h = Math.floorMod(h * base + key.charAt(i), size);
            }
            return h;
        }

        // Metodo interno que selecciona la función hash según la estrategia configurada
        private int hash(String key) {
            if (hashStrategy.equals("sum")) {
                return hashSum(key);
            } else if (hashStrategy.equals("polynomial")) {
                return hashPolynomial(key);
            }
            throw new IllegalArgumentException("Unknown hash strategy");
        }

        // RF1: Insertar un nuevo par o actualizar valor si la clave ya existe
        public void insert(String key, int value) {
            int idx = hash(key);                    // Calcular índice
            List<Pair> bucket = table.get(idx);     // Obtener el bucket correspondiente

            // Buscar si la clave ya existe para actualizar
            for (Pair p : bucket) {
                if (p.key.equals(key)) {
                    p.value = value;  // Actualizar valor existente
                    return;
                }
            }

            // RF6: Registrar colisión si el bucket ya contiene elementos (clave diferente)
            if (!bucket.isEmpty()) {
                collisions++;
            }

            // Insertar nuevo par al final del bucket
            bucket.add(new Pair(key, value));
            count++;  // Incrementar contador de elementos
        }

        // RF2: Buscar una clave y retornar su valor (null si no existe)
        public Integer search(String key) {
            int idx = hash(key);                    // Calcular índice
            for (Pair p : table.get(idx)) {         // Recorrer el bucket
                if (p.key.equals(key)) {
                    return p.value;                 // Clave encontrada
                }
            }
            return null;  // Clave no encontrada
        }

        // RF3: Eliminar una clave si existe (retorna true) o false si no existe
        public boolean delete(String key) {
            int idx = hash(key);                    // Calcular índice
            Iterator<Pair> iterator = table.get(idx).iterator();

            // Recorrer el bucket con iterador para poder eliminar durante la iteración
            while (iterator.hasNext()) {
                Pair p = iterator.next();
                if (p.key.equals(key)) {
                    iterator.remove();  // Eliminar elemento
                    count--;            // Decrementar contador
                    return true;        // Eliminación exitosa
                }
            }
            return false;  // Clave no encontrada
        }

        // Calcula el factor de carga: elementos / tamaño de tabla
        public double loadFactor() {
            return (double) count / size;
        }

        // Calcula la cantidad de buckets que contienen al menos un elemento
        public int usedBuckets() {
            int used = 0;
            for (List<Pair> bucket : table) {
                if (!bucket.isEmpty()) used++;
            }
            return used;
        }

        // Calcula el tamaño máximo de cualquier bucket (mayor concentración)
        public int maxBucketSize() {
            int max = 0;
            for (List<Pair> bucket : table) {
                max = Math.max(max, bucket.size());
            }
            return max;
        }

        // RF7: Genera reporte completo con todas las métricas solicitadas
        public void printReport(double elapsedSeconds) {
            System.out.println("strategy=" + hashStrategy
                    + ", size=" + size
                    + ", elements=" + count
                    + ", loadFactor=" + String.format("%.3f", loadFactor())
                    + ", collisions=" + collisions
                    + ", usedBuckets=" + usedBuckets()
                    + ", maxBucketSize=" + maxBucketSize()
                    + ", insertTimeSeconds=" + String.format("%.6f", elapsedSeconds));
        }
    }

    // Generador de claves aleatorias: strings de longitud fija con caracteres minúsculas
    static List<String> generateRandomKeys(int n, int length) {
        Random random = new Random(42);  // Semilla fija para resultados reproducibles
        List<String> keys = new ArrayList<>();
        String alphabet = "abcdefghijklmnopqrstuvwxyz";
        for (int i = 0; i < n; i++) {
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < length; j++) {
                // Selecciona un carácter aleatorio del alfabeto
                sb.append(alphabet.charAt(random.nextInt(alphabet.length())));
            }
            keys.add(sb.toString());
        }
        return keys;
    }

    // Generador de claves secuenciales: user0, user1, user2, ..., userN-1
    static List<String> generateSequentialKeys(int n) {
        List<String> keys = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            keys.add("user" + i);
        }
        return keys;
    }

    // Generador de claves agrupadas: todas con prefijo común "aaa"
    static List<String> generateClusteredKeys(int n) {
        List<String> keys = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            keys.add("aaa" + i);
        }
        return keys;
    }

    // Ejecuta un experimento completo para un tipo de datos y tamaño de tabla
    static void runExperiment(String datasetName, List<String> keys, int tableSize) {
        System.out.println("\nDataset: " + datasetName);

        // Prueba ambas estrategias de hash para comparar
        for (String strategy : Arrays.asList("sum", "polynomial")) {
            HashTableChaining ht = new HashTableChaining(tableSize, strategy);

            // Medir tiempo de inserción
            long start = System.nanoTime();
            for (int i = 0; i < keys.size(); i++) {
                ht.insert(keys.get(i), i);  // Inserta clave con valor i
            }
            long end = System.nanoTime();
            double elapsedSeconds = (end - start) / 1_000_000_000.0;

            ht.printReport(elapsedSeconds);  // Mostrar resultados
        }
    }

    // Metodo principal: ejecuta todos los experimentos requeridos
    public static void main(String[] args) {
        int n = 1000;              // Número de claves (obligatorio: 1000)
        int tableSize = 211;       // Tamaño primo recomendado (211, 503 o 1009)

        // Ejecuta experimentos con los tres tipos de datos obligatorios
        runExperiment("random", generateRandomKeys(n, 8), tableSize);      // Datos aleatorios
        runExperiment("sequential", generateSequentialKeys(n), tableSize);  // Datos secuenciales
        runExperiment("clustered", generateClusteredKeys(n), tableSize);    // Datos agrupados
    }
}