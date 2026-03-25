package org.example;

import java.util.*;
import java.util.Random;

//TIP To <b>Run</b> code, press <shortcut actionId="Run"/> or
// click the <icon src="AllIcons.Actions.Execute"/> icon in the gutter.
public class Main {
    public static void main(String[] args) {
        System.out.println("Valores de tiempo con numeros");
        long n1= System.nanoTime();
        for (int i = 0; i < 10; i++) {
        }
        long n2 = System.nanoTime();
        long resta1= n2-n1;
        System.out.println(resta1);

        for (int i = 0; i < 100; i++) {
        }
        long n3 = System.nanoTime();
        long resta2= n3-n2;
        System.out.println(resta2);

        for (int i = 0; i < 1000; i++) {
        }
        long n4 = System.nanoTime();
        long resta3= n4-n3;
        System.out.println(resta3);

        for (int i = 0; i < 10000; i++) {
        }
        long n5 = System.nanoTime();
        long resta4= n5-n4;
        System.out.println(resta4);

        for (int i = 0; i < 100000; i++) {
        }
        long n6 = System.nanoTime();
        long resta5= n6-n5;
        System.out.println(resta5);

        for (int i = 0; i < 10000000; i++) {
        }
        long n7 = System.nanoTime();
        long resta6= n7-n6;
        System.out.println(resta6);

        // HASH
        System.out.println("Valores de tiempo con hashmaps");
        HashMap<Integer, String> ciudades = new HashMap<Integer, String>();
        ciudades.put(10, "Madrid");
        ciudades.put(100, "Barcelona");
        ciudades.put(1000, "Valencia");
        ciudades.put(10000, "Lisboa");
        ciudades.put(100000, "Quito");
        ciudades.put(1000000, "Santiago");

        for (Map.Entry<Integer, String> entry : ciudades.entrySet()) {
            long m= System.nanoTime();
            System.out.println(ciudades.get(10));
            long m1= System.nanoTime();
            long r1= m1-m;
            System.out.println(r1);
            System.out.println(ciudades.get(100));
            long m2= System.nanoTime();
            long r2= m2-m1;
            System.out.println(r2);
            System.out.println(ciudades.get(1000));
            long m3= System.nanoTime();
            long r3= m3-m2;
            System.out.println(r3);
            System.out.println(ciudades.get(10000));
            long m4= System.nanoTime();
            long r4= m4-m3;
            System.out.println(r4);
            System.out.println(ciudades.get(100000));
            long m5= System.nanoTime();
            long r5= m5-m4;
            System.out.println(r5);
            System.out.println(ciudades.get(1000000));
            long m6= System.nanoTime();
            long r6= m6-m5;
            System.out.println(r6);
        }
    }
}