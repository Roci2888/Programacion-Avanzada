package org.example;

import java.util.*;


public class Main2 {
    public static void main(String[] args) {
        System.out.println("Valores de tiempo con letras");
        long n1 = System.nanoTime();
        System.out.println("a");
        long n2 = System.nanoTime();
        long r1 = n2 - n1;
        System.out.println(r1);

        System.out.println("a" + "a");
        long n3 = System.nanoTime();
        long r2 = n3 - n1;
        System.out.println(r2);

        System.out.println("a" + "a" + "a");
        long n4 = System.nanoTime();
        long r3 = n4 - n3;
        System.out.println(r3);

        System.out.println("a" + "a" + "a" + "a");
        long n5 = System.nanoTime();
        long r4 = n5 - n4;
        System.out.println(r4);

        System.out.println("a" + "a" + "a" + "a" + "a");
        long n6 = System.nanoTime();
        long r5 = n6 - n5;
        System.out.println(r5);

        System.out.println("a" + "a" + "a" + "a" + "a" + "a");
        long n7 = System.nanoTime();
        long r6 = n7 - n6;
        System.out.println(r6);

        System.out.println("Valores de tiempo con StringBuilder");
        StringBuilder sb = new StringBuilder("a");

        for (int i = 0; i < 6; i++) {
            long m= System.nanoTime();
            sb.append("a");
            long m1= System.nanoTime();
            long resta= m1-m;
            System.out.println(resta);
        }
    }



}
