import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_pdf import PdfPages

# ==========================================
# 1. PARÁMETROS GLOBALES DEL GABINETE
# ==========================================
H_total = 1476.0         # Altura total (82 capas de 18mm)
t_mdf = 18.0
W_front = 350.0          
W_back = 150.0           
D_total = 550.0          
T_wall = 35.0            
num_layers = int(round(H_total / t_mdf))

# Ecuaciones Lute Shape
C_ext = W_front / 2.0; B_ext = 0.0
A_ext = (W_back / 2.0 - C_ext) / (D_total**2)
def profile_ext(x): return A_ext * (x**2) + B_ext * x + C_ext
def profile_int(x): return np.maximum(0, profile_ext(x) - T_wall)

# ==========================================
# 2. PARÁMETROS Y POSICIONES DE LOS PARLANTES
# ==========================================
Y_subwoofer = 220.0
Y_woofer_bot = 520.0
Y_woofer_top = 770.0
Y_tweeter = 1175.0
MTM_spacing = 185.0
Y_mid_bot = Y_tweeter - MTM_spacing
Y_mid_top = Y_tweeter + MTM_spacing

drivers = [
    {'name': 'Subwoofer 12" (UM12-22)', 'y': Y_subwoofer, 'od': 315.0, 'cutout': 285.0, 'depth': 60.0, 'type': 'circle'},
    {'name': 'Mid-Bass 8" Bot (RS225-8)', 'y': Y_woofer_bot, 'od': 225.0, 'cutout': 185.0, 'depth': 40.0, 'type': 'circle'},
    {'name': 'Mid-Bass 8" Top (RS225-8)', 'y': Y_woofer_top, 'od': 225.0, 'cutout': 185.0, 'depth': 40.0, 'type': 'circle'},
    {'name': 'Mid-Range 2" Bot (RS52FN-8)', 'y': Y_mid_bot, 'od': 130.0, 'cutout': 105.0, 'depth': 15.0, 'type': 'circle'},
    {'name': 'Tweeter AMT (AMTPRO-4)', 'y': Y_tweeter, 'w': 100.0, 'h': 200.0, 'cw': 68.0, 'ch': 170.0, 'type': 'rect'},
    {'name': 'Mid-Range 2" Top (RS52FN-8)', 'y': Y_mid_top, 'od': 130.0, 'cutout': 105.0, 'depth': 15.0, 'type': 'circle'}
]

# ==========================================
# 3. FUNCIONES DE GENERACIÓN DE PÁGINAS PDF
# ==========================================
def create_cover_and_specs():
    fig = plt.figure(figsize=(8.5, 11))
    fig.patch.set_facecolor('white')
    ax = fig.add_axes([0, 0, 1, 1]); ax.axis('off')
    
    # Textos de Portada
    ax.text(0.5, 0.9, "Reporte Técnico de Diseño y Manufactura", fontsize=22, fontweight='bold', ha='center')
    ax.text(0.5, 0.85, "Proyecto Translam: Altavoz High-End de 4 Vías (1.47m)", fontsize=16, ha='center', color='#333333')
    ax.text(0.5, 0.80, "Revisión por: Ing. Melvin E. Padilla", fontsize=14, fontweight='bold', ha='center', color='#b30000')
    ax.text(0.5, 0.77, "Fecha: Julio 2026", fontsize=12, ha='center', color='#555555')
    
    ax.plot([0.1, 0.9], [0.74, 0.74], color='black', lw=2)
    
    specs_text = """
    ESPECIFICACIONES DEL SISTEMA
    ---------------------------------------------------------
    1. Arquitectura Acústica:
       - Vías: 4 Vías (Tri-amplificadas)
       - Arreglo Superior: D'Appolito (MTM)
       - Arreglo Medio: Dual Woofer en paralelo (4 Ohmios)
       - Subwoofer: Cámara sellada dedicada

    2. Transductores (Dayton Audio):
       - Vía 4 (Agudos): 1x AMTPRO-4 (Air Motion Transformer)
       - Vía 3 (Medios): 2x RS52FN-8 (2" Fabric Dome)
       - Vía 2 (Medio-Graves): 2x RS225-8 (8" Reference)
       - Vía 1 (Subwoofer): 1x UM12-22 (12" Ultimax)

    3. Gabinete y Manufactura (Translam):
       - Altura Total: 1476.0 mm (82 capas exactas)
       - Grosor MDF: 18.0 mm
       - Ancho Frontal: 350.0 mm
       - Profundidad: 550.0 mm
       - Geometría: Lute Shape (Gota truncada anti-resonante)
       - Separadores de Cámara: MDF Doble (36 mm de grosor sólido)
       
    4. Hardware y Amplificación Recomendada:
       - DSP: MiniDSP Flex Eight (Cortes activos y delay)
       - Amplificador Agudos/Medios: Sansui AU-D5 (Clase AB)
       - Amplificador Medio-Graves: Pioneer SA-9800 (Clase AB)
       - Amplificador Subwoofer: Módulo Clase D Profesional (600W)
    """
    
    ax.text(0.1, 0.68, specs_text, fontsize=12, family='monospace', va='top', ha='left')
    
    # CORRECCIÓN CRÍTICA: Bloquear los ejes para evitar el auto-zoom de la línea
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    return fig

def create_3d_assembly():
    fig = plt.figure(figsize=(8.5, 11), facecolor='#121212')
    ax = fig.add_subplot(111, projection='3d')
    ax.set_facecolor('#121212'); ax.axis('off')
    
    # Caja (Rojo Magico)
    x_vals = np.linspace(0, D_total, 25); z_vals = np.linspace(0, H_total, 35)
    X, Z = np.meshgrid(x_vals, z_vals); Y_ext = profile_ext(X)
    color_caja = '#b30000'
    ax.plot_surface(X, Y_ext, Z, color=color_caja, shade=True, alpha=0.9)
    ax.plot_surface(X, -Y_ext, Z, color=color_caja, shade=True, alpha=0.9)
    
    # Tapas
    Yb, Zb = np.meshgrid(np.linspace(-W_back/2.0, W_back/2.0, 5), z_vals)
    ax.plot_surface(np.full_like(Yb, D_total), Yb, Zb, color=color_caja, shade=True)
    ax.plot_surface(X, Y_ext, np.full_like(X, H_total), color=color_caja, shade=True)
    ax.plot_surface(X, -Y_ext, np.full_like(X, H_total), color=color_caja, shade=True)
    
    # Baffle Frontal Transparente
    Yf, Zf = np.meshgrid(np.linspace(-W_front/2.0, W_front/2.0, 5), z_vals)
    ax.plot_surface(np.zeros_like(Yf), Yf, Zf, color='#050505', shade=True, alpha=0.7)

    # Dibujar Parlantes
    for drv in drivers:
        z_c = drv['y']
        if drv['type'] == 'circle':
            R = drv['od'] / 2.0; depth = drv['depth']; theta = np.linspace(0, 2 * np.pi, 30)
            r_flange = np.linspace(R * 0.85, R, 3); R_f, T_f = np.meshgrid(r_flange, theta)
            ax.plot_surface(-2.0*np.ones_like(R_f), R_f * np.cos(T_f), z_c + R_f * np.sin(T_f), color='#222222', shade=True)
            r_cone = np.linspace(R * 0.2, R * 0.85, 10); R_c, T_c = np.meshgrid(r_cone, theta)
            X_c = -2.0 + (depth + 2.0) * (1 - (R_c - R*0.2) / (R*0.85 - R*0.2))
            ax.plot_surface(X_c, R_c * np.cos(T_c), z_c + R_c * np.sin(T_c), color='#111111', shade=True)
        elif drv['type'] == 'rect':
            w = drv['w']; h = drv['h']
            Y_f, Z_f = np.meshgrid(np.linspace(-w/2.0, w/2.0, 5), np.linspace(z_c - h/2.0, z_c + h/2.0, 5))
            ax.plot_surface(-2.0*np.ones_like(Y_f), Y_f, Z_f, color='#222222', shade=True)
            Y_r, Z_r = np.meshgrid(np.linspace(-68.0/2.0, 68.0/2.0, 5), np.linspace(z_c - 170.0/2.0, z_c + 170.0/2.0, 5))
            ax.plot_surface(5.0*np.ones_like(Y_r), Y_r, Z_r, color='#d4af37', shade=True) # Cinta AMT Dorada

    max_range = np.array([D_total, W_front, H_total]).max() / 2.0
    ax.set_xlim(D_total/2.0 - max_range, D_total/2.0 + max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(H_total/2.0 - max_range, H_total/2.0 + max_range)
    ax.view_init(elev=15, azim=-125)
    fig.suptitle('Render 3D: Ensamblaje Completo de Transductores', fontsize=16, color='white', fontweight='bold', y=0.95)
    return fig

def create_blueprint():
    fig, ax = plt.subplots(figsize=(8.5, 11))
    ax.set_aspect('equal'); ax.set_facecolor('#f0f4f8')
    X_center = W_front / 2.0
    
    baffle = patches.Rectangle((0, 0), W_front, H_total, linewidth=3, edgecolor='#1f2937', facecolor='#e5e7eb', zorder=1)
    ax.add_patch(baffle)
    ax.plot([X_center, X_center], [-50, H_total + 50], color='red', linestyle='dashdot', alpha=0.6, zorder=2)

    for d in drivers:
        y_pos = d['y']
        if d['type'] == 'circle':
            od, cutout = d['od'], d['cutout']
            ax.add_patch(patches.Circle((X_center, y_pos), od / 2.0, linewidth=2, edgecolor='#374151', facecolor='#9ca3af', zorder=3))
            ax.add_patch(patches.Circle((X_center, y_pos), cutout / 2.0, linewidth=1, edgecolor='#111827', facecolor='#4b5563', zorder=4))
        else:
            w, h, cw, ch = d['w'], d['h'], d['cw'], d['ch']
            ax.add_patch(patches.Rectangle((X_center - w/2.0, y_pos - h/2.0), w, h, linewidth=2, edgecolor='#374151', facecolor='#9ca3af', zorder=3))
            ax.add_patch(patches.Rectangle((X_center - cw/2.0, y_pos - ch/2.0), cw, ch, linewidth=1, edgecolor='#111827', facecolor='#4b5563', zorder=4))
        ax.add_patch(patches.Circle((X_center, y_pos), 3, color='red', zorder=5))
        ax.text(X_center + (d.get('od', d.get('w'))/2.0) + 15, y_pos, f"{d['name']}\nCentro: {y_pos} mm", va='center', fontsize=7, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    cota_x = -40
    ax.annotate(text='', xy=(cota_x, Y_tweeter), xytext=(cota_x, Y_mid_top), arrowprops=dict(arrowstyle='<->', color='blue'))
    ax.annotate(text='', xy=(cota_x, Y_tweeter), xytext=(cota_x, Y_mid_bot), arrowprops=dict(arrowstyle='<->', color='blue'))
    ax.text(cota_x - 10, Y_tweeter + MTM_spacing/2, f"{MTM_spacing} mm", color='blue', rotation=90, va='center', ha='center', fontsize=9, fontweight='bold')
    ax.text(cota_x - 10, Y_tweeter - MTM_spacing/2, f"{MTM_spacing} mm", color='blue', rotation=90, va='center', ha='center', fontsize=9, fontweight='bold')

    ax.set_xlim(-100, W_front + 150); ax.set_ylim(-50, H_total + 50)
    ax.set_title(f"Plano Técnico: Baffle Frontal\nAltura: {H_total} mm | Ancho: {W_front} mm", fontsize=14, fontweight='bold', pad=20)
    ax.set_xlabel("Eje X (mm)"); ax.set_ylabel("Eje Y (mm)"); ax.grid(True, linestyle='--', alpha=0.5)
    return fig

def create_template(mode="standard"):
    fig, ax = plt.subplots(figsize=(8.5, 11))
    x_ext = np.linspace(0, D_total, 200); y_e = profile_ext(x_ext)
    
    ax.plot(x_ext, y_e, 'k-', linewidth=3); ax.plot(x_ext, -y_e, 'k-', linewidth=3)
    ax.plot([0, 0], [-C_ext, C_ext], 'k-', linewidth=3); ax.plot([D_total, D_total], [-W_back/2.0, W_back/2.0], 'k-', linewidth=3)
    
    if mode == "standard":
        ax.set_title(f'Plantilla 1: Anillo de Volumen Interno (MDF {t_mdf}mm)', fontsize=14, fontweight='bold')
        x_int = np.linspace(T_wall, D_total - T_wall, 200); y_i = profile_int(x_int)
        ax.plot(x_int, y_i, 'b--', linewidth=2); ax.plot(x_int, -y_i, 'b--', linewidth=2)
        ax.plot([T_wall, T_wall], [-profile_int(T_wall), profile_int(T_wall)], 'b--', linewidth=2)
        ax.plot([D_total-T_wall, D_total-T_wall], [-profile_int(D_total-T_wall), profile_int(D_total-T_wall)], 'b--', linewidth=2)
        
    elif mode == "bracing":
        ax.set_title(f'Plantilla 2: Anillo de Refuerzo Estructural - Bracing (MDF {t_mdf}mm)', fontsize=14, fontweight='bold')
        brace_c = D_total / 2.0; brace_w = T_wall / 2.0
        x_i1 = np.linspace(T_wall, brace_c - brace_w, 100)
        ax.plot(x_i1, profile_int(x_i1), 'b--', linewidth=2); ax.plot(x_i1, -profile_int(x_i1), 'b--', linewidth=2)
        ax.plot([T_wall, T_wall], [-profile_int(T_wall), profile_int(T_wall)], 'b--', linewidth=2)
        ax.plot([brace_c - brace_w, brace_c - brace_w], [-profile_int(brace_c - brace_w), profile_int(brace_c - brace_w)], 'b--', linewidth=2)
        x_i2 = np.linspace(brace_c + brace_w, D_total - T_wall, 100)
        ax.plot(x_i2, profile_int(x_i2), 'b--', linewidth=2); ax.plot(x_i2, -profile_int(x_i2), 'b--', linewidth=2)
        ax.plot([brace_c + brace_w, brace_c + brace_w], [-profile_int(brace_c + brace_w), profile_int(brace_c + brace_w)], 'b--', linewidth=2)
        ax.plot([D_total-T_wall, D_total-T_wall], [-profile_int(D_total-T_wall), profile_int(D_total-T_wall)], 'b--', linewidth=2)
        ax.fill_between(x_ext, y_e, -y_e, color='#deb887', alpha=0.3)
        ax.fill_between(x_i1, profile_int(x_i1), -profile_int(x_i1), color='white', alpha=1.0)
        ax.fill_between(x_i2, profile_int(x_i2), -profile_int(x_i2), color='white', alpha=1.0)
        
    elif mode == "solid":
        ax.set_title('Plantilla 3: Separador Sólido y Tapas (2 Capas MDF = 36mm)', fontsize=14, fontweight='bold')
        ax.fill_between(x_ext, y_e, -y_e, color='#8b4513', alpha=0.6)
        ax.text(D_total/2, 0, "MDF SÓLIDO SIN VACIADO\n(Aísla cámaras acústicas)", ha='center', va='center', fontsize=12, color='white', fontweight='bold', bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))

    ax.axis('equal'); ax.grid(True, linestyle=':', alpha=0.6)
    ax.set_xlabel('Profundidad X (mm)'); ax.set_ylabel('Ancho Y (mm)')
    return fig

# ==========================================
# 4. COMPILACIÓN EN PDF
# ==========================================
if __name__ == '__main__':
    pdf_filename = 'Reporte_Translam_Ingenieria.pdf'
    print(f"Generando el documento: {pdf_filename} ...")
    
    with PdfPages(pdf_filename) as pdf:
        # Página 1: Textos y Especificaciones
        print(" -> Generando Página 1: Especificaciones Técnicas")
        pdf.savefig(create_cover_and_specs())
        
        # Página 2: Render 3D
        print(" -> Generando Página 2: Render 3D Ensamblaje")
        pdf.savefig(create_3d_assembly())
        
        # Página 3: Plano Frontal
        print(" -> Generando Página 3: Plano Técnico Baffle Frontal")
        pdf.savefig(create_blueprint())
        
        # Página 4: Plantilla 1 (Vaciado)
        print(" -> Generando Página 4: Plantilla de Vaciado Estándar")
        pdf.savefig(create_template(mode="standard"))
        
        # Página 5: Plantilla 2 (Bracing)
        print(" -> Generando Página 5: Plantilla de Refuerzo Estructural")
        pdf.savefig(create_template(mode="bracing"))
        
        # Página 6: Plantilla 3 (Sólido)
        print(" -> Generando Página 6: Plantilla de Separador Sólido")
        pdf.savefig(create_template(mode="solid"))
        
    print(f"¡Éxito! El archivo '{pdf_filename}' se ha generado correctamente en tu directorio.")