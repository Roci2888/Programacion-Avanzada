package org.example;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.Scanner;

public class Paciente {
    Deque<Paciente> pacientes = new ArrayDeque<>();
    String nombre;

    public Paciente(String nombre) {
        this.nombre = nombre;
    }

    public void añadirPacienteNormal(){
        System.out.println("Ingresar Paciente normal");
        Scanner sc = new Scanner(System.in);
        String nombre= sc.nextLine();
        pacientes.addLast(new Paciente(nombre));
    }

    public void añadirPacientePrioritario(){
        System.out.println("Ingresar Paciente prioritario");
        Scanner sc = new Scanner(System.in);
        String nombre= sc.nextLine();
        pacientes.addFirst(new Paciente(nombre));
    }
    public void atenderPaciente(){
        pacientes.pollFirst();
    }
    public void cancelar_ultimo(){
        pacientes.pollLast();
    }
    public void mostrarPrimero(){
       pacientes.peek();
    }
    public void mostrarUltimo(){
        pacientes.peekLast();
    }
    public void SaberSiHayPacientes(){
        pacientes.isEmpty();
    }
    public void numeroDePacientes(){
        pacientes.size();
    }
}
