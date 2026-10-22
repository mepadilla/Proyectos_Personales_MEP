#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 13:24:21 2026

@author: meppadilla
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ==========================================
# 1. PARAMETROS DEL BAFLE FRONT (Milímetros)
# ==========================================
W_baffle = 350.0   # Ancho del panel frontal
H_baffle = 1350.0  # NUEVA Altura total de la torre para acomodar 6 drivers

X_center = W_baffle / 2.0 

# ==========================================
# 2. ESPECIFICACIONES DE TRANSDUCTORES
# ==========================================
drivers_specs = {
    'Subwoofer 12" (UM12-22)': (315.0, 285.0),
    'Mid-Bass 8" (RS225-8)': (225.0, 185.0),
    'Mid-Range 2" (RS52FN-8)': (130.0, 105.0),
    'Tweeter AMT (AMT1-4)': (98.0, 75.0)
}

# ==========================================
# 3. CÁLCULO DE POSICIONES (Eje Y)
# ==========================================
Y_subwoofer = 220.0

# Arreglo Dual Mid-Bass
Y_woofer_bot = 520.0
Y_woofer_top = 760.0

# Arreglo MTM (Elevado ligeramente a la altura del oído en sofás modernos)
Y_tweeter = 1070.0  
MTM_spacing = 120.0 
Y_mid_top = Y_tweeter + MTM_spacing
Y_mid_bot = Y_tweeter - MTM_spacing

# Lista de 6 parlantes
layout = [
    {'name': 'Subwoofer 12" (UM12-22)', 'y': Y_subwoofer},
    {'name': 'Mid-Bass 8" (Bot)', 'y': Y_woofer_bot, 'spec_key': 'Mid-Bass 8" (RS225-8)'},
    {'name': 'Mid-Bass 8" (Top)', 'y': Y_woofer_top, 'spec_key': 'Mid-Bass 8" (RS225-8)'},
    {'name': 'Mid-Range 2" (Bot)', 'y': Y_mid_bot, 'spec_key': 'Mid-Range 2" (RS52FN-8)'},
    {'name': 'Tweeter AMT (AMT1-4)', 'y': Y_tweeter, 'spec_key': 'Tweeter AMT (AMT1-4)'},
    {'name': 'Mid-Range 2" (Top)', 'y': Y_mid_top, 'spec_key': 'Mid-Range 2" (RS52FN-8)'}
]

# ==========================================
# 4. MOTOR DE DIBUJO (Technical Blueprint)
# ==========================================
def draw_blueprint():
    fig, ax = plt.subplots(figsize=(6, 14))
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f4f8')
    
    baffle = patches.Rectangle((0, 0), W_baffle, H_baffle, 
                               linewidth=3, edgecolor='#1f2937', facecolor='#e5e7eb', zorder=1)
    ax.add_patch(baffle)
    ax.plot([X_center, X_center], [-50, H_baffle + 50], color='red', linestyle='dashdot', alpha=0.6, zorder=2)

    for driver in layout:
        name_display = driver['name']
        spec_key = driver.get('spec_key', name_display)
        y_pos = driver['y']
        od, cutout = drivers_specs[spec_key]
        
        outer = patches.Circle((X_center, y_pos), od / 2.0, linewidth=2, edgecolor='#374151', facecolor='#9ca3af', zorder=3)
        inner = patches.Circle((X_center, y_pos), cutout / 2.0, linewidth=1, edgecolor='#111827', facecolor='#4b5563', zorder=4)
        dot = patches.Circle((X_center, y_pos), 3, color='red', zorder=5)
        
        ax.add_patch(outer); ax.add_patch(inner); ax.add_patch(dot)
        
        ax.text(X_center + (od/2.0) + 15, y_pos, f"{name_display}\nC: {y_pos} mm", 
                va='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

    cota_x = -40
    for i in range(len(layout) - 1):
        y1, y2 = layout[i]['y'], layout[i+1]['y']
        ax.annotate('', xy=(cota_x, y2), xytext=(cota_x, y1), arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
        ax.text(cota_x - 10, (y1 + y2) / 2, f"{abs(y2 - y1):.1f} mm", rotation=90, ha='right', va='center', fontsize=8, color='blue')
        ax.plot([cota_x, X_center], [y1, y1], color='blue', linestyle=':', alpha=0.5)
        ax.plot([cota_x, X_center], [y2, y2], color='blue', linestyle=':', alpha=0.5)

    ax.annotate('', xy=(0, -20), xytext=(W_baffle, -20), arrowprops=dict(arrowstyle='<->'))
    ax.text(X_center, -35, f"Ancho: {W_baffle} mm", ha='center')
    ax.annotate('', xy=(W_baffle + 40, 0), xytext=(W_baffle + 40, H_baffle), arrowprops=dict(arrowstyle='<->'))
    ax.text(W_baffle + 55, H_baffle / 2, f"Altura Total: {H_baffle} mm", va='center', rotation=-90)

    ax.set_xlim(-100, W_baffle + 200); ax.set_ylim(-100, H_baffle + 100)
    ax.axis('off')
    plt.title("Plano CAD: Baffle Frontal de 6 Drivers (W-W / MTM)", fontweight='bold', pad=20)
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    draw_blueprint()