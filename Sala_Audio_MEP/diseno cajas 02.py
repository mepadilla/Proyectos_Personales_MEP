#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 12:53:32 2026

@author: meppadilla
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# ==========================================
# 1. PARAMETROS DEL BAFLE FRONT (Milímetros)
# ==========================================
W_baffle = 350.0   # Ancho del panel frontal
H_baffle = 1100.0  # Altura total de la torre

# Coordenada X central para todos los parlantes
X_center = W_baffle / 2.0 

# ==========================================
# 2. ESPECIFICACIONES DE TRANSDUCTORES (Dayton Audio)
# ==========================================
# Formato: 'Nombre': (Diámetro Exterior OD, Diámetro Corte Cutout)
drivers_specs = {
    'Subwoofer 12" (UM12-22)': (315.0, 285.0),
    'Mid-Bass 8" (RS225-8)': (225.0, 185.0),
    'Mid-Range 2" (RS52FN-8)': (130.0, 105.0),
    'Tweeter AMT (AMT1-4)': (98.0, 75.0)   # Dimensiones aproximadas de la brida
}

# ==========================================
# 3. CÁLCULO DE POSICIONES (Coordenada Y del centro)
# ==========================================
# Altura del oído promedio sentado: ~850mm - 950mm
Y_tweeter = 850.0  

# MTM - Distancia mínima posible entre Medio y Tweeter
# Radio Tweeter (49) + Radio Medio (65) = 114mm mínimo. Usamos 120mm por seguridad de fresado.
MTM_spacing = 120.0 
Y_mid_top = Y_tweeter + MTM_spacing
Y_mid_bot = Y_tweeter - MTM_spacing

# Woofer 8" - Separado del arreglo MTM para no interferir mecánicamente
# Radio Medio (65) + Radio Woofer (112.5) = 177.5mm mínimo.
Y_woofer = 500.0

# Subwoofer 12" - Lo más bajo posible pero dejando espacio estructural
Y_subwoofer = 200.0

# Lista ordenada de parlantes a dibujar (desde abajo hacia arriba)
layout = [
    {'name': 'Subwoofer 12" (UM12-22)', 'y': Y_subwoofer, 'type': 'sub'},
    {'name': 'Mid-Bass 8" (RS225-8)', 'y': Y_woofer, 'type': 'woofer'},
    {'name': 'Mid-Range 2" (RS52FN-8)', 'y': Y_mid_bot, 'type': 'mid_bot'},
    {'name': 'Tweeter AMT (AMT1-4)', 'y': Y_tweeter, 'type': 'tweeter'},
    {'name': 'Mid-Range 2" (RS52FN-8)', 'y': Y_mid_top, 'type': 'mid_top'}
]

# ==========================================
# 4. MOTOR DE DIBUJO (Technical Blueprint)
# ==========================================
def draw_blueprint():
    fig, ax = plt.subplots(figsize=(6, 12))
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f4f8') # Color de fondo estilo plano técnico
    
    # Dibujar el contorno del Baffle Frontal
    baffle = patches.Rectangle((0, 0), W_baffle, H_baffle, 
                               linewidth=3, edgecolor='#1f2937', facecolor='#e5e7eb',
                               zorder=1)
    ax.add_patch(baffle)
    
    # Línea de simetría central
    ax.plot([X_center, X_center], [-50, H_baffle + 50], 
            color='red', linestyle='dashdot', linewidth=1, alpha=0.6, zorder=2)

    # Bucle para dibujar cada parlante
    for driver in layout:
        name = driver['name']
        y_pos = driver['y']
        od, cutout = drivers_specs[name]
        
        # Diámetro exterior (Flange)
        outer_circle = patches.Circle((X_center, y_pos), od / 2.0, 
                                      linewidth=2, edgecolor='#374151', facecolor='#9ca3af', zorder=3)
        # Diámetro de corte (Hole)
        inner_circle = patches.Circle((X_center, y_pos), cutout / 2.0, 
                                      linewidth=1, edgecolor='#111827', facecolor='#4b5563', zorder=4)
        # Punto central
        center_dot = patches.Circle((X_center, y_pos), 3, color='red', zorder=5)
        
        ax.add_patch(outer_circle)
        ax.add_patch(inner_circle)
        ax.add_patch(center_dot)
        
        # Etiqueta del parlante
        ax.text(X_center + (od/2.0) + 15, y_pos, f"{name}\nCentro: {y_pos} mm", 
                verticalalignment='center', fontsize=9, color='#1f2937',
                bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

    # Dibujar cotas de separación (Distancias C-to-C)
    cota_x = -40  # Posición X para las líneas de cota
    for i in range(len(layout) - 1):
        y1 = layout[i]['y']
        y2 = layout[i+1]['y']
        dist = abs(y2 - y1)
        
        # Línea de cota
        ax.annotate('', xy=(cota_x, y2), xytext=(cota_x, y1),
                    arrowprops=dict(arrowstyle='<->', color='blue', lw=1.5))
        
        # Texto de la cota
        ax.text(cota_x - 10, (y1 + y2) / 2, f"{dist:.1f} mm", 
                rotation=90, horizontalalignment='right', verticalalignment='center',
                fontsize=9, color='blue', fontweight='bold')
        
        # Líneas guías horizontales desde los centros hasta las cotas
        ax.plot([cota_x, X_center], [y1, y1], color='blue', linestyle=':', linewidth=1, alpha=0.5)
        ax.plot([cota_x, X_center], [y2, y2], color='blue', linestyle=':', linewidth=1, alpha=0.5)

    # Cotas totales (Ancho y Alto)
    # Ancho
    ax.annotate('', xy=(0, -20), xytext=(W_baffle, -20), arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(X_center, -35, f"Ancho Total: {W_baffle} mm", ha='center')
    
    # Alto
    ax.annotate('', xy=(W_baffle + 40, 0), xytext=(W_baffle + 40, H_baffle), arrowprops=dict(arrowstyle='<->', color='black'))
    ax.text(W_baffle + 55, H_baffle / 2, f"Altura Total: {H_baffle} mm", va='center', rotation=-90)

    # Configuración final de la vista
    ax.set_xlim(-100, W_baffle + 200)
    ax.set_ylim(-100, H_baffle + 100)
    ax.axis('off') # Ocultar ejes estándar para que parezca un plano
    plt.title("Plano CAD 2D: Baffle Frontal de 4 Vías (Arreglo MTM)", fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.show()

# ==========================================
# 5. CONSOLA: REPORTE DE PERFORACIÓN
# ==========================================
if __name__ == '__main__':
    print("="*50)
    print("REPORTE DE PERFORACIÓN - PANEL FRONTAL (BAFFLE)")
    print("="*50)
    print(f"Dimensiones de la placa: {W_baffle}mm x {H_baffle}mm")
    print(f"Eje X (Línea central): Medir a {X_center} mm desde el borde izquierdo.\n")
    print("Posiciones Y (desde el borde inferior del mueble hacia arriba):")
    
    for driver in layout:
        print(f" - {driver['name']:<25} | Centro en Y: {driver['y']:>6.1f} mm | Diámetro Corte: {drivers_specs[driver['name']][1]} mm")
        
    print("\nSeparación Centro a Centro (C-to-C):")
    print(f" - Subwoofer a Mid-Bass:   {abs(Y_woofer - Y_subwoofer):.1f} mm")
    print(f" - Mid-Bass a Medio Inferior: {abs(Y_mid_bot - Y_woofer):.1f} mm")
    print(f" - Medio Inferior a Tweeter:  {abs(Y_tweeter - Y_mid_bot):.1f} mm (Crítico para MTM)")
    print(f" - Tweeter a Medio Superior:  {abs(Y_mid_top - Y_tweeter):.1f} mm (Crítico para MTM)")
    print("="*50)
    
    draw_blueprint()