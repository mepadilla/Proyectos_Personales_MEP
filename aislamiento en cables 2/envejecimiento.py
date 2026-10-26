import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF
import datetime
import os

# ==========================================
# 0. CLASES Y MODELOS FÍSICOS
# ==========================================

class SistemaBombeo:
    def __init__(self, k_iso_20c, r_mot_20c, r_spl_20c):
        # AHORA RECIBIMOS VALORES NORMALIZADOS A 20°C
        self.k_iso_base = k_iso_20c
        self.r_mot_base = r_mot_20c
        self.r_spl_base = r_spl_20c
        self.t_ref = 20.0
        self.lambda_permeabilidad = 0.008 

    def _factor_termico(self, t_op):
        """Corrección por Temperatura (Arrhenius)"""
        return 0.5 ** ((t_op - self.t_ref)/10.0)

    def _factor_envejecimiento(self, profundidad_m, tiempo_anios, nivel_agua_m):
        """Degradación por presión (solo bajo agua) y tiempo"""
        if tiempo_anios <= 0: return 1.0
        if profundidad_m < nivel_agua_m:
            presion_atm = 1.0 
        else:
            columna_agua = profundidad_m - nivel_agua_m
            presion_atm = 1.0 + (columna_agua / 10.0)
        return np.exp(-self.lambda_permeabilidad * presion_atm * tiempo_anios)

    def calcular_sistema_completo(self, depths_m, t_amb, tiempo_anios, nivel_agua_m, t_fondo_est):
        max_depth = np.max(depths_m)
        # Interpolación lineal de temperatura
        temps_vector = t_amb + (depths_m / max_depth) * (t_fondo_est - t_amb)

        r_cable_vec = []
        r_sistema_vec = []

        for d, t_local in zip(depths_m, temps_vector):
            kt = self._factor_termico(t_local)
            kh = self._factor_envejecimiento(d, tiempo_anios, nivel_agua_m)
            factor_total = kt * kh
            
            k_cable_t = self.k_iso_base * factor_total
            r_mot_t = self.r_mot_base * factor_total
            r_spl_t = self.r_spl_base * factor_total
            
            l_km = max(d, 0.1) / 1000.0
            rc = k_cable_t / l_km
            cond = (1/rc) + (1/r_mot_t) + (1/r_spl_t)
            
            r_cable_vec.append(rc)
            r_sistema_vec.append(1/cond)

        return np.array(r_cable_vec), np.array(r_sistema_vec)

class ReportePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Reporte Tecnico: Simulacion de Aislamiento', 0, 1, 'C')
        self.set_font('Arial', 'I', 10)
        self.cell(0, 10, 'Analisis Avanzado (Termico + Presion + Humedad)', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-20)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(95, 5, 'Elaborado por: ', 0, 0, 'R')
        self.set_text_color(0, 0, 255)
        self.set_font('Arial', 'IU', 8)
        link = 'https://www.linkedin.com/in/melvin-padilla-3425106'
        self.cell(95, 5, 'Ing. Melvin E. Padilla', 0, 1, 'L', link=link)
        self.set_text_color(128, 128, 128)
        self.set_font('Arial', '', 8)
        fecha = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.ln(5)
        self.cell(0, 5, f'Pagina {self.page_no()} - {fecha}', 0, 0, 'C')

    def chapter_title(self, label):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 0, 0)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, label, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 5, text)
        self.ln()

def solicitar_valor(msg, val_def):
    txt = input(f"{msg} [Defecto: {val_def}]: ")
    return float(txt) if txt else val_def

# ==========================================
# 1. EJECUCIÓN PRINCIPAL
# ==========================================
print("\n--- SISTEMA DE ANÁLISIS COMPLETO (NORMALIZADO) ---")
r_medida = solicitar_valor("1. Resistencia medida cable (MΩ)", 2000)
l_medida = solicitar_valor("2. Longitud total instalada (m)", 100)
nivel_agua = solicitar_valor("3. Nivel de Bombeo/Agua (m)", 50)
r_mot = solicitar_valor("4. Resistencia Motor (MΩ)", 100)
r_spl = solicitar_valor("5. Resistencia Empalme (MΩ)", 100)
t_amb = solicitar_valor("6. Temp. Ambiente al medir (°C)", 30)

# --- PASO CRÍTICO: NORMALIZACIÓN A 20°C ---
# Calculamos cuánto valdrían estos componentes si estuviéramos a 20°C.
# Si medimos a 30°C, el valor a 20°C debe ser MAYOR (el doble).
factor_norm = 2 ** ((t_amb - 20.0) / 10.0)

print(f"\n[INFO] Normalizando datos de {t_amb}°C a base 20°C (Factor: {factor_norm:.2f}x)...")

k_raw = r_medida * (l_medida / 1000.0)
k_iso_20c = k_raw * factor_norm
r_mot_20c = r_mot * factor_norm
r_spl_20c = r_spl * factor_norm

# Inicializamos el sistema con valores BASE 20°C
sistema = SistemaBombeo(k_iso_20c, r_mot_20c, r_spl_20c)

# --- EVALUACIÓN CUALITATIVA (Usamos el K normalizado o el medido? 
# Normalmente se evalúa el K a 20°C para estandarizar)
if k_iso_20c < 36: # Valores IEEE usualmente referidos a 20C o 40C
    calidad_desc = "BAJA / CRITICA"
    consejo = "Cable con fugas importantes."
elif k_iso_20c < 150:
    calidad_desc = "ESTANDAR (PVC)"
    consejo = "Comportamiento normal para PVC estandar."
else:
    calidad_desc = "EXCELENTE"
    consejo = "Aislamiento superior."

# Datos Térmicos
t_fondo_est = t_amb + (l_medida/100.0)*3.0 + 8.0
delta_t = t_fondo_est - t_amb
# Factor térmico en el fondo (para reporte)
factor_termico_fondo = 0.5 ** (delta_t / 10.0)

# Vectores
depths = np.linspace(1, l_medida, 200)

# ==========================================
# 2. GENERACIÓN DE GRÁFICAS
# ==========================================
plt.figure(figsize=(10, 6))
# Escenario 1: Frio (Debe coincidir con la medición inicial si Prof=L y T=T_amb)
rc_amb, rs_amb = sistema.calcular_sistema_completo(depths, t_amb, 0, nivel_agua, t_amb)
# Escenario 2: Caliente
rc_hot, rs_hot = sistema.calcular_sistema_completo(depths, t_amb, 0, nivel_agua, t_fondo_est)

plt.plot(depths, rc_amb, 'b--', alpha=0.4, label=f'Solo Cable @ {t_amb}°C')
plt.plot(depths, rs_amb, 'b-', linewidth=2.5, label=f'SISTEMA @ {t_amb}°C')
plt.plot(depths, rc_hot, 'r--', alpha=0.4, label=f'Solo Cable (Gradiente T)')
plt.plot(depths, rs_hot, 'r-', linewidth=2.5, label=f'SISTEMA (Operativo)')

plt.axvline(x=nivel_agua, color='cyan', linestyle='-.', label='Nivel Agua')
plt.axhline(y=5, color='black', linestyle=':', label='Lim. 5 MΩ')

plt.annotate(f"{rs_amb[-1]:.1f} MΩ", xy=(l_medida, rs_amb[-1]), xytext=(5, 5), textcoords='offset points', color='blue', fontsize=8, fontweight='bold')
plt.annotate(f"{rs_hot[-1]:.1f} MΩ", xy=(l_medida, rs_hot[-1]), xytext=(5, -10), textcoords='offset points', color='red', fontsize=8, fontweight='bold')

plt.yscale('log')
plt.grid(True, which="both", alpha=0.2)
plt.title(f"Impacto Térmico Inmediato\n(K Norm a 20°C: {k_iso_20c:.1f} MΩ·km)")
plt.xlabel("Profundidad (m)")
plt.ylabel("Resistencia (MΩ)")
plt.legend(loc='lower left', fontsize=8)
plt.tight_layout()
plt.savefig("grafica_termica.png", dpi=100)
plt.close()

# Gráfica 2: Tiempo
plt.figure(figsize=(10, 6))
anios = [0, 1, 3, 5]
colores = ['red', 'orange', 'green', 'purple']
for anio, color in zip(anios, colores):
    _, rs_anio = sistema.calcular_sistema_completo(depths, t_amb, anio, nivel_agua, t_fondo_est)
    label = "Instalación" if anio == 0 else f"Año {anio}"
    plt.plot(depths, rs_anio, color=color, linewidth=2, label=label)
    plt.annotate(f"{rs_anio[-1]:.1f}", xy=(l_medida, rs_anio[-1]), xytext=(3, 0), textcoords='offset points', color=color, fontsize=8)

plt.axvline(x=nivel_agua, color='cyan', linestyle='-.')
plt.axhline(y=5, color='black', linestyle=':')
plt.yscale('log')
plt.grid(True, which="both", alpha=0.2)
plt.title("Proyección Vida Útil (Presión + Humedad)")
plt.xlabel("Profundidad (m)")
plt.ylabel("Resistencia (MΩ)")
plt.legend()
plt.tight_layout()
plt.savefig("grafica_tiempo.png", dpi=100)
plt.close()

# ==========================================
# 3. REPORTE PDF
# ==========================================
print("[INFO] Generando PDF Detallado...")
pdf = ReportePDF()
pdf.add_page()

# Sección 1
pdf.chapter_title("1. Datos de Entrada (Campo)")
datos_txt = (
    f"Resistencia Medida Cable: {r_medida} MOhm\n"
    f"Longitud Total Instalada: {l_medida} m\n"
    f"Nivel de Agua (Bombeo): {nivel_agua} m\n"
    f"Resistencia Motor (Ref): {r_mot} MOhm\n"
    f"Resistencia Empalme: {r_spl} MOhm\n"
    f"Temperatura Ambiente: {t_amb} C"
)
pdf.chapter_body(datos_txt)

# Sección 2 (Ahora incluye los valores normalizados)
pdf.chapter_title("2. Analisis Tecnico (Normalizado IEEE 43)")
tecnico_txt = (
    f"Constante K (a T.Medida): {k_raw:.2f} MOhm-km\n"
    f"Constante K (Base 20C): {k_iso_20c:.2f} MOhm-km\n"
    f"Estado del Cable: {calidad_desc}\n"
    f"Temp. Estimada en Fondo: {t_fondo_est:.1f} C (Delta T: +{delta_t:.1f} C)\n"
    f"Factor Degradacion Termica (Fondo vs Superficie): {factor_termico_fondo:.4f}"
)
pdf.chapter_body(tecnico_txt)

# Sección 3
val_frio = rs_amb[-1]
val_caliente = rs_hot[-1]
val_5_anos = sistema.calcular_sistema_completo([l_medida], t_amb, 5, nivel_agua, t_fondo_est)[1][0]

pdf.chapter_title(f"3. Prediccion a {l_medida} metros")
prediccion_txt = (
    f"Resistencia Total en Frio (Superficie): {val_frio:.2f} MOhm\n"
    f"Resistencia Total Operativa (T=0): {val_caliente:.2f} MOhm\n"
    f"Proyeccion a 5 Anos (Envejecimiento): {val_5_anos:.2f} MOhm\n\n"
    f"Evaluacion: {consejo}"
)
pdf.chapter_body(prediccion_txt)

# Sección 4
pdf.chapter_title("4. Curvas de Comportamiento Termico")
pdf.image("grafica_termica.png", x=15, w=180)

pdf.add_page()
pdf.chapter_title("5. Analisis de Vida Util (Dinamico)")
pdf.chapter_body(
    f"Este modelo incorpora el efecto de la presion hidrostatica variable a partir de los {nivel_agua}m "
    "de profundidad."
)
pdf.image("grafica_tiempo.png", x=15, w=180)

pdf.output("Reporte_Aislamiento_Corregido.pdf")
print("[EXITO] Reporte generado.")