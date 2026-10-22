#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:57:58 2026

@author: meppadilla
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# 1. PARAMETROS DEL GABINETE (Milímetros)
# ==========================================
H_total = 1100.0         # Altura total
W_front = 350.0          # Ancho del Baffle Frontal
W_back = 150.0           # Ancho del Panel Trasero
D_total = 550.0          # Profundidad total de la caja

# ==========================================
# 2. PARAMETROS DE LOS PARLANTES (Posiciones y Tamaños)
# ==========================================
# Posiciones Y (Altura desde el suelo)
Y_subwoofer = 200.0
Y_woofer = 500.0
Y_mid_bot = 730.0
Y_tweeter = 850.0
Y_mid_top = 970.0

# Configuraciones de los drivers: (Nombre, Y_center, OuterDiameter, Profundidad_Cono)
drivers = [
    {'name': 'Subwoofer 12"', 'y': Y_subwoofer, 'od': 315.0, 'depth': 60.0, 'type': 'cone'},
    {'name': 'Mid-Bass 8"',   'y': Y_woofer,    'od': 225.0, 'depth': 40.0, 'type': 'cone'},
    {'name': 'Mid-Range 2" (Inf)', 'y': Y_mid_bot, 'od': 130.0, 'depth': 15.0, 'type': 'cone'},
    {'name': 'Tweeter AMT',   'y': Y_tweeter,   'od': 98.0,  'depth': 5.0,  'type': 'amt'},
    {'name': 'Mid-Range 2" (Sup)', 'y': Y_mid_top, 'od': 130.0, 'depth': 15.0, 'type': 'cone'}
]

# ==========================================
# 3. MATEMÁTICA DEL PERFIL (Lute Shape)
# ==========================================
C_ext = W_front / 2.0
B_ext = 0.0
A_ext = (W_back / 2.0 - C_ext) / (D_total**2)

def profile_ext(x):
    """Ecuación parabólica para las paredes laterales curvas"""
    return A_ext * (x**2) + B_ext * x + C_ext

# ==========================================
# 4. FUNCIONES DE RENDERIZADO DE PARLANTES
# ==========================================
def draw_cone_driver(ax, z_c, od, depth):
    """Dibuja un parlante de cono 3D (Brida, Cono y Tapa polvo)"""
    R = od / 2.0
    theta = np.linspace(0, 2 * np.pi, 40)
    
    # 1. Brida exterior (Flange)
    r_flange = np.linspace(R * 0.85, R, 5)
    R_f, T_f = np.meshgrid(r_flange, theta)
    Y_f = R_f * np.cos(T_f)
    Z_f = z_c + R_f * np.sin(T_f)
    X_f = np.zeros_like(R_f) - 2.0 # Ligeramente por delante del baffle
    ax.plot_surface(X_f, Y_f, Z_f, color='#222222', shade=True, alpha=1.0)
    
    # 2. Cono (Se hunde hacia el interior del gabinete)
    r_cone = np.linspace(R * 0.2, R * 0.85, 15)
    R_c, T_c = np.meshgrid(r_cone, theta)
    Y_c = R_c * np.cos(T_c)
    Z_c = z_c + R_c * np.sin(T_c)
    # Interpolar profundidad: de X=-2 (borde) a X=depth (centro)
    X_c = -2.0 + (depth + 2.0) * (1 - (R_c - R*0.2) / (R*0.85 - R*0.2))
    ax.plot_surface(X_c, Y_c, Z_c, color='#111111', shade=True, alpha=0.95)
    
    # 3. Tapa polvo (Dustcap central)
    r_dust = np.linspace(0, R * 0.2, 8)
    R_d, T_d = np.meshgrid(r_dust, theta)
    Y_d = R_d * np.cos(T_d)
    Z_d = z_c + R_d * np.sin(T_d)
    # Forma de cúpula
    X_d = depth - (depth * 0.25) * np.cos((R_d / (R * 0.2)) * (np.pi / 2))
    ax.plot_surface(X_d, Y_d, Z_d, color='#1a1a1a', shade=True, alpha=1.0)

def draw_amt_tweeter(ax, z_c, od):
    """Dibuja el Tweeter AMT (Brida circular, cinta rectangular dorada)"""
    R = od / 2.0
    theta = np.linspace(0, 2 * np.pi, 40)
    
    # Brida exterior circular
    r_flange = np.linspace(R * 0.5, R, 5)
    R_f, T_f = np.meshgrid(r_flange, theta)
    Y_f = R_f * np.cos(T_f)
    Z_f = z_c + R_f * np.sin(T_f)
    X_f = np.zeros_like(R_f) - 2.0
    ax.plot_surface(X_f, Y_f, Z_f, color='#222222', shade=True)
    
    # Cinta AMT (Rectángulo central profundo)
    y_rib = np.linspace(-R * 0.35, R * 0.35, 10)
    z_rib = np.linspace(z_c - R * 0.45, z_c + R * 0.45, 10)
    Y_r, Z_r = np.meshgrid(y_rib, z_rib)
    X_r = np.zeros_like(Y_r) + 5.0 # Hundido
    ax.plot_surface(X_r, Y_r, Z_r, color='#d4af37', shade=True) # Color dorado kapton

# ==========================================
# 5. CONSTRUCCIÓN DE LA ESCENA PRINCIPAL
# ==========================================
def render_full_assembly():
    fig = plt.figure(figsize=(10, 12), facecolor='#121212') # Fondo oscuro estilo estudio
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#121212')
    
    # Quitar los ejes y grillas estándar para una vista limpia
    ax.axis('off')
    
    # 5.1 DIBUJAR EL GABINETE (Pintura Roja "Magico S-Series")
    x_vals = np.linspace(0, D_total, 30)
    z_vals = np.linspace(0, H_total, 30)
    X, Z = np.meshgrid(x_vals, z_vals)
    Y_ext = profile_ext(X)
    
    color_caja = '#b30000' # Rojo escarlata profundo
    
    # Paredes laterales curvas
    ax.plot_surface(X, Y_ext, Z, color=color_caja, shade=True, alpha=0.9)
    ax.plot_surface(X, -Y_ext, Z, color=color_caja, shade=True, alpha=0.9)
    
    # Panel trasero
    Y_back_mesh = np.linspace(-W_back/2.0, W_back/2.0, 10)
    Yb, Zb = np.meshgrid(Y_back_mesh, z_vals)
    Xb = np.full_like(Yb, D_total)
    ax.plot_surface(Xb, Yb, Zb, color=color_caja, shade=True)
    
    # Tapa Superior
    ax.plot_surface(X, Y_ext, np.full_like(X, H_total), color=color_caja, shade=True)
    ax.plot_surface(X, -Y_ext, np.full_like(X, H_total), color=color_caja, shade=True)
    
    # 5.2 DIBUJAR EL BAFFLE FRONTAL (Aluminio Anodizado Negro)
    # Hacemos el baffle ligeramente transparente para que los conos puedan "hundirse" en la caja visualmente sin glitchear
    Y_front_mesh = np.linspace(-W_front/2.0, W_front/2.0, 10)
    Yf, Zf = np.meshgrid(Y_front_mesh, z_vals)
    Xf = np.zeros_like(Yf)
    ax.plot_surface(Xf, Yf, Zf, color='#050505', shade=True, alpha=0.7)

    # 5.3 INTEGRAR LOS PARLANTES
    for drv in drivers:
        if drv['type'] == 'cone':
            draw_cone_driver(ax, drv['y'], drv['od'], drv['depth'])
        elif drv['type'] == 'amt':
            draw_amt_tweeter(ax, drv['y'], drv['od'])

    # ==========================================
    # 6. CONFIGURACION DE CÁMARA E ILUMINACIÓN
    # ==========================================
    # Truco para forzar una proporción geométrica 1:1:1 en matplotlib 3D
    max_range = np.array([D_total, W_front, H_total]).max() / 2.0
    mid_x = D_total / 2.0
    mid_y = 0
    mid_z = H_total / 2.0
    
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    # Ángulo de vista dramático (Vista isométrica frontal 3/4)
    ax.view_init(elev=15, azim=-125)
    
    fig.suptitle('Renderizado 3D: Torre Translam 4-Vías (Arreglo D\'Appolito)', fontsize=16, color='white', fontweight='bold', y=0.9)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    print("Iniciando motor de renderizado 3D...")
    print("Generando malla estructural Translam...")
    print("Mapeando transductores Dayton Audio...")
    render_full_assembly()
    print("Renderizado completo. (Gira la imagen con el ratón).")