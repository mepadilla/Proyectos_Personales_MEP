#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 18 14:23:38 2026

@author: meppadilla
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches

# ==========================================
# 1. PARAMETROS DEL GABINETE FRONTAL
# ==========================================
H_baffle = 1476.0  # Altura total (mm) - Aumentada a 82 capas de 18mm
W_baffle = 350.0   # Ancho del panel frontal (mm)
X_center = W_baffle / 2.0

# ==========================================
# 2. ESPECIFICACIONES DE TRANSDUCTORES
# ==========================================
# od = Outer Diameter (Diámetro exterior / Brida)
# cutout = Diámetro de corte para el imán
drivers_specs = {
    'Subwoofer 12" (UM12-22)': {'type': 'circle', 'od': 315.0, 'cutout': 285.0},
    'Mid-Bass 8" (RS225-8)': {'type': 'circle', 'od': 225.0, 'cutout': 185.0},
    'Mid-Range 2" (RS52FN-8)': {'type': 'circle', 'od': 130.0, 'cutout': 105.0},
    'Tweeter AMT (AMTPRO-4)': {'type': 'rect', 'w': 100.0, 'h': 200.0, 'cw': 68.0, 'ch': 170.0}
}

# ==========================================
# 3. CÁLCULO DE POSICIONES (Eje Y)
# ==========================================
# Posición desde la base (Y=0) hasta el centro de cada parlante
Y_subwoofer = 220.0

# Arreglo Dual Mid-Bass
Y_woofer_bot = 520.0
Y_woofer_top = 770.0 # Ajustado para evitar colisión

# Arreglo MTM (D'Appolito)
Y_tweeter = 1175.0   # Subido para dar espacio a los woofers
MTM_spacing = 185.0  # Separación ampliada para acomodar los 200mm del AMTPRO-4
Y_mid_top = Y_tweeter + MTM_spacing
Y_mid_bot = Y_tweeter - MTM_spacing

# Lista estructurada para el motor de dibujo
layout = [
    {'name': 'Subwoofer 12" (UM12-22)', 'y': Y_subwoofer, 'spec_key': 'Subwoofer 12" (UM12-22)'},
    {'name': 'Mid-Bass 8" (Bot)', 'y': Y_woofer_bot, 'spec_key': 'Mid-Bass 8" (RS225-8)'},
    {'name': 'Mid-Bass 8" (Top)', 'y': Y_woofer_top, 'spec_key': 'Mid-Bass 8" (RS225-8)'},
    {'name': 'Mid-Range 2" (Bot)', 'y': Y_mid_bot, 'spec_key': 'Mid-Range 2" (RS52FN-8)'},
    {'name': 'Tweeter AMTPRO-4', 'y': Y_tweeter, 'spec_key': 'Tweeter AMT (AMTPRO-4)'},
    {'name': 'Mid-Range 2" (Top)', 'y': Y_mid_top, 'spec_key': 'Mid-Range 2" (RS52FN-8)'}
]

# ==========================================
# 4. MOTOR DE DIBUJO (Technical Blueprint)
# ==========================================
def draw_blueprint():
    fig, ax = plt.subplots(figsize=(6, 14))
    ax.set_aspect('equal')
    ax.set_facecolor('#f0f4f8')
    
    # Dibujar la tabla del panel frontal
    baffle = patches.Rectangle((0, 0), W_baffle, H_baffle, 
                               linewidth=3, edgecolor='#1f2937', facecolor='#e5e7eb', zorder=1)
    ax.add_patch(baffle)
    
    # Línea de simetría central
    ax.plot([X_center, X_center], [-50, H_baffle + 50], color='red', linestyle='dashdot', alpha=0.6, zorder=2)

    # Dibujar cada parlante
    for driver in layout:
        name_display = driver['name']
        spec_key = driver['spec_key']
        y_pos = driver['y']
        specs = drivers_specs[spec_key]
        
        # Evaluar si es circular o rectangular (para el AMTPRO)
        if specs['type'] == 'circle':
            od, cutout = specs['od'], specs['cutout']
            # Brida exterior
            outer = patches.Circle((X_center, y_pos), od / 2.0, linewidth=2, edgecolor='#374151', facecolor='#9ca3af', zorder=3)
            # Agujero de corte
            inner = patches.Circle((X_center, y_pos), cutout / 2.0, linewidth=1, edgecolor='#111827', facecolor='#4b5563', zorder=4)
            text_x = X_center + (od/2.0) + 15
            
        else: # Lógica para el Tweeter AMT rectangular
            w, h, cw, ch = specs['w'], specs['h'], specs['cw'], specs['ch']
            # Brida exterior rectangular
            outer = patches.Rectangle((X_center - w/2.0, y_pos - h/2.0), w, h, linewidth=2, edgecolor='#374151', facecolor='#9ca3af', zorder=3)
            # Agujero de corte rectangular
            inner = patches.Rectangle((X_center - cw/2.0, y_pos - ch/2.0), cw, ch, linewidth=1, edgecolor='#111827', facecolor='#4b5563', zorder=4)
            text_x = X_center + (w/2.0) + 15
            
        # Marcar el centro exacto
        dot = patches.Circle((X_center, y_pos), 3, color='red', zorder=5)
        
        ax.add_patch(outer)
        ax.add_patch(inner)
        ax.add_patch(dot)
        
        # Etiqueta lateral
        ax.text(text_x, y_pos, f"{name_display}\nCentro: {y_pos} mm", 
                va='center', fontsize=8, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

    # Dibujar Cotas para el arreglo MTM (Espaciado Crítico D'Appolito)
    cota_x = -40
    # Líneas delimitadoras de la cota
    ax.plot([cota_x, X_center], [Y_tweeter, Y_tweeter], color='blue', linestyle=':', alpha=0.5)
    ax.plot([cota_x, X_center], [Y_mid_top, Y_mid_top], color='blue', linestyle=':', alpha=0.5)
    ax.plot([cota_x, X_center], [Y_mid_bot, Y_mid_bot], color='blue', linestyle=':', alpha=0.5)
    
    # Flechas de cota
    ax.annotate(text='', xy=(cota_x, Y_tweeter), xytext=(cota_x, Y_mid_top), arrowprops=dict(arrowstyle='<->', color='blue'))
    ax.annotate(text='', xy=(cota_x, Y_tweeter), xytext=(cota_x, Y_mid_bot), arrowprops=dict(arrowstyle='<->', color='blue'))
    
    # Textos de cota
    ax.text(cota_x - 10, Y_tweeter + MTM_spacing/2, f"{MTM_spacing} mm", color='blue', rotation=90, va='center', ha='center', fontsize=9, fontweight='bold')
    ax.text(cota_x - 10, Y_tweeter - MTM_spacing/2, f"{MTM_spacing} mm", color='blue', rotation=90, va='center', ha='center', fontsize=9, fontweight='bold')

    # Ajustes finales del lienzo
    ax.set_xlim(-100, W_baffle + 180)
    ax.set_ylim(-50, H_baffle + 50)
    ax.set_title(f"Plano Técnico de Corte - Baffle Frontal\nAltura: {H_baffle} mm | Ancho: {W_baffle} mm\n(Eje central a {X_center} mm del borde)", fontsize=12, fontweight='bold', pad=20)
    ax.set_xlabel("Eje X (Ancho en mm)")
    ax.set_ylabel("Eje Y (Altura desde la base en mm)")
    ax.grid(True, linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()

# ==========================================
# 5. REPORTE EN CONSOLA (Para el Taller)
# ==========================================
def print_drilling_report():
    print("=" * 60)
    print(" REPORTE DE TALADRADO PARA PANEL FRONTAL (Baffle)")
    print("=" * 60)
    print(f"Dimensión Total de la Placa: {W_baffle} mm (Ancho) x {H_baffle} mm (Alto)")
    print(f"Todas las marcas X deben hacerse a {X_center} mm desde el borde lateral.\n")
    
    for d in reversed(layout): # Imprimir de arriba hacia abajo
        specs = drivers_specs[d['spec_key']]
        print(f"[*] {d['name']}")
        print(f"    - Marcar Centro en Y: {d['y']} mm")
        
        if specs['type'] == 'circle':
            print(f"    - Diámetro de Agujero (Corte pasante): {specs['cutout']} mm")
            print(f"    - Diámetro Fresado Brida (Rebajado): {specs['od']} mm")
        else:
            print(f"    - Rectángulo de Corte (Pasante): {specs['cw']} mm (Ancho) x {specs['ch']} mm (Alto)")
            print(f"    - Rectángulo Fresado (Rebajado): {specs['w']} mm (Ancho) x {specs['h']} mm (Alto)")
        print("-" * 60)

if __name__ == '__main__':
    print_drilling_report()
    draw_blueprint().