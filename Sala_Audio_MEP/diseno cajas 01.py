#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:42:22 2026

@author: meppadilla
"""

import numpy as np
import matplotlib.pyplot as plt

# ==========================================
# 1. PARAMETROS DE DISEÑO (Milímetros)
# ==========================================
H_total = 1100.0         # Altura total de la caja
t_mdf = 18.0             # Grosor de la lámina de MDF
W_front = 350.0          # Ancho del panel frontal (Baffle)
W_back = 150.0           # Ancho del panel trasero
D_total = 550.0          # Profundidad total de la caja
T_wall = 35.0            # Grosor aproximado de la pared (para el vaciado interno)

num_layers = int(round(H_total / t_mdf))

# ==========================================
# 2. DEFINICION DEL PERFIL EXTERIOR E INTERIOR
# ==========================================
# Usamos una ecuación polinómica para la curva "Lute Shape" (Gota)
C_ext = W_front / 2.0
B_ext = 0.0
A_ext = (W_back / 2.0 - C_ext) / (D_total**2)

def profile_ext(x):
    """Calcula el ancho exterior en función de la profundidad x"""
    return A_ext * (x**2) + B_ext * x + C_ext

def profile_int(x):
    """Calcula el ancho interior restando el grosor de la pared"""
    # Usamos np.maximum para evitar valores negativos
    return np.maximum(0, profile_ext(x) - T_wall)

# ==========================================
# 3. GENERACION DEL MODELO 3D (Caja Completa)
# ==========================================
def plot_3d_model():
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title('Modelo 3D - Gabinete Acústico (Estilo Magico)', fontsize=14, fontweight='bold')
    
    # Crear malla para las paredes laterales curvas
    x_vals = np.linspace(0, D_total, 50)
    z_vals = np.linspace(0, H_total, 50)
    X, Z = np.meshgrid(x_vals, z_vals)
    Y_ext = profile_ext(X)
    
    # Superficies laterales (color madera/naranja)
    ax.plot_surface(X, Y_ext, Z, color='coral', alpha=0.8, rstride=5, cstride=5)
    ax.plot_surface(X, -Y_ext, Z, color='coral', alpha=0.8, rstride=5, cstride=5)
    
    # Panel Frontal (Baffle Negro)
    Y_front = np.linspace(-C_ext, C_ext, 10)
    Yf, Zf = np.meshgrid(Y_front, z_vals)
    Xf = np.zeros_like(Yf)
    ax.plot_surface(Xf, Yf, Zf, color='black', alpha=0.9)
    
    # Panel Trasero
    Y_back = np.linspace(-W_back/2.0, W_back/2.0, 10)
    Yb, Zb = np.meshgrid(Y_back, z_vals)
    Xb = np.full_like(Yb, D_total)
    ax.plot_surface(Xb, Yb, Zb, color='coral', alpha=0.8)
    
    # Tapa Superior
    ax.plot_surface(X, Y_ext, np.full_like(X, H_total), color='coral', alpha=0.5)
    ax.plot_surface(X, -Y_ext, np.full_like(X, H_total), color='coral', alpha=0.5)

    # Configuraciones de vista
    ax.set_xlabel('Profundidad (X) mm')
    ax.set_ylabel('Ancho (Y) mm')
    ax.set_zlabel('Altura (Z) mm')
    
    # Truco para forzar aspecto isométrico en matplotlib 3D
    max_range = np.array([D_total, W_front, H_total]).max() / 2.0
    mid_x = D_total / 2.0
    mid_y = 0
    mid_z = H_total / 2.0
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.view_init(elev=20, azim=-45)

# ==========================================
# 4. GENERACION DE PLANOS 2D (Plantillas de Corte)
# ==========================================
def plot_standard_ring():
    plt.figure(figsize=(7, 9))
    plt.title(f'Plantilla 2D: Anillo Estándar de Volumen\\n(Espesor MDF: {t_mdf}mm)', fontsize=12, fontweight='bold')
    
    x_ext = np.linspace(0, D_total, 200)
    y_e = profile_ext(x_ext)
    
    # Dibujar contorno exterior
    plt.plot(x_ext, y_e, 'k-', linewidth=3, label='Corte Exterior')
    plt.plot(x_ext, -y_e, 'k-', linewidth=3)
    plt.plot([0, 0], [-C_ext, C_ext], 'k-', linewidth=3) # Frente
    plt.plot([D_total, D_total], [-W_back/2.0, W_back/2.0], 'k-', linewidth=3) # Fondo
    
    # Dibujar contorno interior (vaciado)
    x_int = np.linspace(T_wall, D_total - T_wall, 200)
    y_i = profile_int(x_int)
    plt.plot(x_int, y_i, 'b--', linewidth=2, label='Vaciado Interior')
    plt.plot(x_int, -y_i, 'b--', linewidth=2)
    plt.plot([T_wall, T_wall], [-profile_int(T_wall), profile_int(T_wall)], 'b--', linewidth=2)
    plt.plot([D_total-T_wall, D_total-T_wall], [-profile_int(D_total-T_wall), profile_int(D_total-T_wall)], 'b--', linewidth=2)
    
    plt.axis('equal')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.xlabel('Profundidad (mm)')
    plt.ylabel('Ancho (mm)')

def plot_bracing_ring():
    plt.figure(figsize=(7, 9))
    plt.title('Plantilla 2D: Anillo de Refuerzo Estructural (Bracing)', fontsize=12, fontweight='bold')
    
    x_ext = np.linspace(0, D_total, 200)
    y_e = profile_ext(x_ext)
    
    # Dibujar contorno exterior
    plt.plot(x_ext, y_e, 'k-', linewidth=3, label='Corte Exterior')
    plt.plot(x_ext, -y_e, 'k-', linewidth=3)
    plt.plot([0, 0], [-C_ext, C_ext], 'k-', linewidth=3) 
    plt.plot([D_total, D_total], [-W_back/2.0, W_back/2.0], 'k-', linewidth=3)
    
    # Parámetros del puente de refuerzo
    brace_center = D_total / 2.0
    brace_w = T_wall / 2.0
    
    # Vaciado 1 (Cámara Frontal)
    x_int1 = np.linspace(T_wall, brace_center - brace_w, 100)
    plt.plot(x_int1, profile_int(x_int1), 'b--', linewidth=2, label='Vaciado Interior')
    plt.plot(x_int1, -profile_int(x_int1), 'b--', linewidth=2)
    plt.plot([T_wall, T_wall], [-profile_int(T_wall), profile_int(T_wall)], 'b--', linewidth=2)
    plt.plot([brace_center - brace_w, brace_center - brace_w], 
             [-profile_int(brace_center - brace_w), profile_int(brace_center - brace_w)], 'b--', linewidth=2)
    
    # Vaciado 2 (Cámara Trasera)
    x_int2 = np.linspace(brace_center + brace_w, D_total - T_wall, 100)
    plt.plot(x_int2, profile_int(x_int2), 'b--', linewidth=2)
    plt.plot(x_int2, -profile_int(x_int2), 'b--', linewidth=2)
    plt.plot([brace_center + brace_w, brace_center + brace_w], 
             [-profile_int(brace_center + brace_w), profile_int(brace_center + brace_w)], 'b--', linewidth=2)
    plt.plot([D_total-T_wall, D_total-T_wall], 
             [-profile_int(D_total-T_wall), profile_int(D_total-T_wall)], 'b--', linewidth=2)
    
    # Rellenar visualmente la madera (Opcional, para mayor claridad)
    plt.fill_between(x_ext, y_e, -y_e, color='#deb887', alpha=0.3, label='Madera (MDF)')
    plt.fill_between(x_int1, profile_int(x_int1), -profile_int(x_int1), color='white', alpha=1.0)
    plt.fill_between(x_int2, profile_int(x_int2), -profile_int(x_int2), color='white', alpha=1.0)

    plt.axis('equal')
    plt.grid(True, linestyle=':', alpha=0.6)
    plt.legend(loc='upper right')
    plt.xlabel('Profundidad (mm)')
    plt.ylabel('Ancho (mm)')

# ==========================================
# 5. EJECUCION DE LOS GRAFICOS
# ==========================================
if __name__ == '__main__':
    print("Iniciando simulador Translam...")
    print(f"Altura calculada: {num_layers} capas de MDF de {t_mdf}mm.")
    
    # Llamamos a las funciones que generan las 3 ventanas de gráficos
    plot_3d_model()
    plot_standard_ring()
    plot_bracing_ring()
    
    # Muestra todas las ventanas en Spyder
    plt.show()
    print("Cálculos y renderizados finalizados con éxito.")