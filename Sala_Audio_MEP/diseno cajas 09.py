#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:23:05 2026

@author: meppadilla
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# ==========================================
# 1. PARAMETROS DEL GABINETE
# ==========================================
H_total = 1476.0         # Nueva Altura (1.47 metros - 82 capas)
W_front = 350.0          
W_back = 150.0           
D_total = 550.0          

# ==========================================
# 2. PARAMETROS DE LOS PARLANTES (6 Drivers)
# ==========================================
Y_subwoofer = 220.0
Y_woofer_bot = 520.0
Y_woofer_top = 770.0
Y_tweeter = 1175.0
MTM_spacing = 185.0
Y_mid_bot = Y_tweeter - MTM_spacing
Y_mid_top = Y_tweeter + MTM_spacing

drivers = [
    {'name': 'Subwoofer 12"', 'y': Y_subwoofer, 'od': 315.0, 'depth': 60.0, 'type': 'cone'},
    {'name': 'Mid-Bass 8" Bot', 'y': Y_woofer_bot, 'od': 225.0, 'depth': 40.0, 'type': 'cone'},
    {'name': 'Mid-Bass 8" Top', 'y': Y_woofer_top, 'od': 225.0, 'depth': 40.0, 'type': 'cone'},
    {'name': 'Mid-Range 2" Bot', 'y': Y_mid_bot, 'od': 130.0, 'depth': 15.0, 'type': 'cone'},
    {'name': 'Tweeter AMT', 'y': Y_tweeter, 'od': 98.0, 'depth': 5.0, 'type': 'amt'},
    {'name': 'Mid-Range 2" Top', 'y': Y_mid_top, 'od': 130.0, 'depth': 15.0, 'type': 'cone'}
]

# ==========================================
# 3. MATEMÁTICA LUTE SHAPE
# ==========================================
C_ext = W_front / 2.0; B_ext = 0.0
A_ext = (W_back / 2.0 - C_ext) / (D_total**2)
def profile_ext(x): return A_ext * (x**2) + B_ext * x + C_ext

# ==========================================
# 4. RENDERIZADO 3D
# ==========================================
def draw_cone_driver(ax, z_c, od, depth):
    R = od / 2.0
    theta = np.linspace(0, 2 * np.pi, 30)
    
    # Flange
    r_flange = np.linspace(R * 0.85, R, 3); R_f, T_f = np.meshgrid(r_flange, theta)
    ax.plot_surface(-2.0*np.ones_like(R_f), R_f * np.cos(T_f), z_c + R_f * np.sin(T_f), color='#222222', shade=True)
    
    # Cone
    r_cone = np.linspace(R * 0.2, R * 0.85, 10); R_c, T_c = np.meshgrid(r_cone, theta)
    X_c = -2.0 + (depth + 2.0) * (1 - (R_c - R*0.2) / (R*0.85 - R*0.2))
    ax.plot_surface(X_c, R_c * np.cos(T_c), z_c + R_c * np.sin(T_c), color='#111111', shade=True)
    
    # Dustcap
    r_dust = np.linspace(0, R * 0.2, 5); R_d, T_d = np.meshgrid(r_dust, theta)
    X_d = depth - (depth * 0.25) * np.cos((R_d / (R * 0.2)) * (np.pi / 2))
    ax.plot_surface(X_d, R_d * np.cos(T_d), z_c + R_d * np.sin(T_d), color='#1a1a1a', shade=True)

def draw_amt_tweeter(ax, z_c, od):
    R = od / 2.0
    theta = np.linspace(0, 2 * np.pi, 30)
    r_flange = np.linspace(R * 0.5, R, 3); R_f, T_f = np.meshgrid(r_flange, theta)
    ax.plot_surface(-2.0*np.ones_like(R_f), R_f * np.cos(T_f), z_c + R_f * np.sin(T_f), color='#222222', shade=True)
    
    y_rib = np.linspace(-R * 0.35, R * 0.35, 5)
    z_rib = np.linspace(z_c - R * 0.45, z_c + R * 0.45, 5)
    Y_r, Z_r = np.meshgrid(y_rib, z_rib)
    ax.plot_surface(5.0*np.ones_like(Y_r), Y_r, Z_r, color='#d4af37', shade=True)

def render_full_assembly():
    fig = plt.figure(figsize=(10, 14), facecolor='#121212')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#121212'); ax.axis('off')
    
    # Caja (Rojo Magico)
    x_vals = np.linspace(0, D_total, 25); z_vals = np.linspace(0, H_total, 35)
    X, Z = np.meshgrid(x_vals, z_vals); Y_ext = profile_ext(X)
    
    color_caja = '#b30000'
    ax.plot_surface(X, Y_ext, Z, color=color_caja, shade=True, alpha=0.9)
    ax.plot_surface(X, -Y_ext, Z, color=color_caja, shade=True, alpha=0.9)
    
    # Trasera
    Yb, Zb = np.meshgrid(np.linspace(-W_back/2.0, W_back/2.0, 5), z_vals)
    ax.plot_surface(np.full_like(Yb, D_total), Yb, Zb, color=color_caja, shade=True)
    
    # Tapas
    ax.plot_surface(X, Y_ext, np.full_like(X, H_total), color=color_caja, shade=True)
    ax.plot_surface(X, -Y_ext, np.full_like(X, H_total), color=color_caja, shade=True)
    
    # Baffle Frontal Transparente
    Yf, Zf = np.meshgrid(np.linspace(-W_front/2.0, W_front/2.0, 5), z_vals)
    ax.plot_surface(np.zeros_like(Yf), Yf, Zf, color='#050505', shade=True, alpha=0.7)

    # Parlantes
    for drv in drivers:
        if drv['type'] == 'cone': draw_cone_driver(ax, drv['y'], drv['od'], drv['depth'])
        elif drv['type'] == 'amt': draw_amt_tweeter(ax, drv['y'], drv['od'])

    # Configuración de Cámara
    max_range = np.array([D_total, W_front, H_total]).max() / 2.0
    mid_x, mid_y, mid_z = D_total / 2.0, 0, H_total / 2.0
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)
    
    ax.view_init(elev=15, azim=-125)
    fig.suptitle('Torre Translam: 6-Drivers (Arreglos W-W & M-T-M)', fontsize=16, color='white', fontweight='bold', y=0.9)
    plt.tight_layout(); plt.show()

if __name__ == '__main__':
    render_full_assembly()