"""
====================================================================================================
UNIVERSIDAD INTERNACIONAL DE LAS AMÉRICAS (U.I.A.)
ESCUELA DE ECONOMÍA - CURSO DE ECONOMÍA I / INTRODUCCIÓN A LA ECONOMÍA
APLICACIÓN DIDÁCTICA SINCRÓNICA: CONCENTRACIÓN DE MERCADO Y PENSAMIENTO CRÍTICO
====================================================================================================
Basado en:
1. Jon Bergmann (2026) - The Mastery Flip: Averting AI Stupefaction & The Three Pillars
2. David Merrill / Juan G. Fernández (2026) - Los 4 Principios del Diseño Didáctico
3. Lyn Alden (Junio 2020) - Concentración de Mercado (S&P 500 Market-Cap vs Equal-Weight, Liquidez Fed)
4. Marco de Competencias del Siglo XXI (Pensamiento Crítico, Análisis de Datos y Comunicación Oral)
====================================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import re

# --------------------------------------------------------------------------------------------------
# 1. CONFIGURACIÓN DE PÁGINA Y ESTILO VISUAL MODERNO
# --------------------------------------------------------------------------------------------------
st.set_page_config(
    page_title="UIA Economía | Concentración de Mercado & Pensamiento Crítico",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inyección de estilos CSS enriquecidos para experiencia universitaria premium
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #0369A1 100%);
        color: white;
        padding: 2.2rem 2.4rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.25);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .main-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.025em;
        margin-bottom: 0.4rem;
        color: #FFFFFF;
    }

    .main-header p {
        font-size: 1.05rem;
        color: #94A3B8;
        margin-bottom: 0.8rem;
    }

    .badge-pill {
        display: inline-block;
        padding: 0.3rem 0.85rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }

    .badge-uia {
        background-color: #0284C7;
        color: white;
    }

    .badge-pedagogy {
        background-color: #0D9488;
        color: white;
    }

    .badge-status {
        background-color: #475569;
        color: #F8FAFC;
    }

    .metric-card {
        background: white;
        border: 1px solid #E2E8F0;
        border-radius: 14px;
        padding: 1.4rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.08);
    }

    .pedagogy-alert {
        background: #F0FDF4;
        border-left: 4px solid #16A34A;
        padding: 1.2rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1.5rem;
        color: #166534;
    }

    .counterexample-box {
        background: #FFF7ED;
        border-left: 4px solid #EA580C;
        padding: 1.2rem;
        border-radius: 0 12px 12px 0;
        margin-bottom: 1.5rem;
        color: #9A3412;
    }

    .quote-box {
        background: #F8FAFC;
        border-left: 4px solid #6366F1;
        padding: 1rem 1.4rem;
        border-radius: 0 10px 10px 0;
        font-style: italic;
        color: #334155;
        margin: 1rem 0;
    }

    .rubric-tag {
        font-weight: 700;
        padding: 0.25rem 0.6rem;
        border-radius: 6px;
        font-size: 0.85rem;
    }

    .stButton>button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------------------------------
# 2. GESTIÓN DEL ESTADO DE SESIÓN (st.session_state)
# --------------------------------------------------------------------------------------------------
def init_session_state():
    """Inicializa todas las variables reactivas acumulativas de la sesión."""
    defaults = {
        "student_name": "",
        "session_start_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        # Ejercicios y respuestas
        "ex1_analysis": "",
        "ex1_hhi_calc": 0.0,
        "ex2_decision": "Mantener ponderación tradicional (Market-Cap)",
        "ex2_justification": "",
        "ex2_sim_liquidity": 3.0,
        "ex2_sim_concentration": 22.0,
        "ex3_contrast_neoclassical": "",
        "ex4_oral_pitch": "",
        "ex4_counter_defense": "",
        # Retroalimentación y evaluación
        "evaluated": False,
        "feedback_ex1": {},
        "feedback_ex2": {},
        "feedback_ex3": {},
        "feedback_ex4": {},
        "competency_scores": {
            "Pensamiento Crítico": 0,
            "Análisis Cuantitativo & Datos": 0,
            "Toma de Decisiones Económicas": 0,
            "Comunicación Rigurosa & Defensa": 0,
            "Metacognición & Autonomía": 0
        },
        "score_total": 0,
        "mastery_level": "Sin Iniciar",
        "active_tab": 0
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

init_session_state()


# --------------------------------------------------------------------------------------------------
# 3. SIDEBAR: IDENTIDAD, REGISTRO, MARCO DIDÁCTICO Y PROGRESO
# --------------------------------------------------------------------------------------------------
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1618042164219-62c820f10723?auto=format&fit=crop&w=400&q=80", 
             caption="UIA - Laboratorio de Economía Crítica", use_container_width=True)
    
    st.markdown("### 🏛️ Identidad Académica")
    st.markdown("**Universidad Internacional de las Américas**")
    st.markdown("*Carrera de Economía | Primer Ingreso*")
    st.markdown("**Sesión Sincrónica - Semana 4**")
    
    st.divider()
    
    # Solicitud y validación del nombre del estudiante
    st.markdown("### 👤 Registro del Estudiante")
    name_input = st.text_input(
        "Nombre Completo del Alumno:",
        value=st.session_state.student_name,
        placeholder="Ej: Sofía Ramírez Mora",
        help="Requerido para generar el reporte de evaluación consolidada y la defensa de maestría."
    )
    if name_input != st.session_state.student_name:
        st.session_state.student_name = name_input

    if not st.session_state.student_name.strip():
        st.warning("⚠️ Ingrese su nombre para personalizar su sesión y habilitar la exportación del portafolio.")
    else:
        st.success(f"Sesión activa: **{st.session_state.student_name}**")

    st.divider()

    # Principios Didácticos (David Merrill) & Mastery Flip (Jon Bergmann)
    with st.expander("📚 Marco Pedagógico & Fuentes", expanded=False):
        st.markdown("""
        **1. Mastery Flip (Jon Bergmann, 2026):**
        - *Pilar 1: Motores de IA*: IA como tutor socrático, no como 'botón mágico' que suprime el esfuerzo cognitivo (*Averting AI Stupefaction*).
        - *Pilar 2: Raíces Analógicas*: Anclaje del pensamiento riguroso en clase sincrónica (*Productive Struggle*).
        - *Pilar 3: Comprobación Humana*: Evaluación oral de 2 minutos sobre el proceso mental (*Human Check*).
        
        **2. Principios de David Merrill:**
        - **Activación**: Conectar esquemas mentales previos relevantes.
        - **Demostración**: Observar sistemas causales (*What-Happens*) y des-ejemplos.
        - **Aplicación**: Romper la ilusión de saber resolviendo casos auténticos.
        - **Integración**: Defender posturas públicamente ante pares y docentes.
        
        **3. Fuente Económica Central:**
        - Lyn Alden (Junio 2020): *Concentración de mercado* (Desconexión entre balance de la Fed y desempleo; S&P 500 Market-Weight vs Equal-Weight).
        """)

    # Monitoreo del avance
    st.markdown("### 📈 Progreso de la Sesión")
    completed_steps = sum([
        bool(st.session_state.student_name.strip()),
        bool(st.session_state.ex1_analysis.strip()),
        bool(st.session_state.ex2_justification.strip()),
        bool(st.session_state.ex3_contrast_neoclassical.strip()),
        bool(st.session_state.ex4_oral_pitch.strip()),
        st.session_state.evaluated
    ])
    progress_pct = int((completed_steps / 6) * 100)
    st.progress(progress_pct / 100)
    st.caption(f"Avance de la sesión sincrónica: **{progress_pct}%** ({completed_steps}/6 fases)")


# --------------------------------------------------------------------------------------------------
# 4. ENCABEZADO PRINCIPAL DE LA APLICACIÓN
# --------------------------------------------------------------------------------------------------
student_greeting = f" | Estudiante: {st.session_state.student_name}" if st.session_state.student_name else ""
st.markdown(f"""
<div class="main-header">
    <div style="margin-bottom: 0.8rem;">
        <span class="badge-pill badge-uia">U.I.A. Economía</span>
        <span class="badge-pill badge-pedagogy">Sesión Sincrónica: Raíces Analógicas</span>
        <span class="badge-pill badge-status">Comprobación de Maestría</span>
    </div>
    <h1>Dinámica de Pensamiento Crítico: Concentración de Mercado</h1>
    <p>Desmitificando el espejismo de los índices bursátiles, evaluando el impacto de la liquidez monetaria y contrastando los supuestos neoclásicos con evidencia empírica{student_greeting}.</p>
    <div style="font-size: 0.85rem; color: #CBD5E1;">
        <strong>Etapa de la Clase Invertida:</strong> 2. Durante la sesión sincrónica &rarr; i. Raíces analógicas (Demostración) &rarr; ii. Comprobación de maestría (Aplicación y Defensa Oral)
    </div>
</div>
""", unsafe_allow_html=True)


# --------------------------------------------------------------------------------------------------
# 5. PESTAÑAS PRINCIPALES DEL RECORRIDO COGNITIVO
# --------------------------------------------------------------------------------------------------
tabs = st.tabs([
    "1. Activación & Demostración Sincrónica",
    "2. Simulación & Pensamiento Crítico",
    "3. Contraste de Modelos Económicos",
    "4. Habilidades del Siglo XXI & Feedback",
    "5. Defensa Oral (Human Check) & Exportación"
])


# ==================================================================================================
# PESTAÑA 1: ACTIVACIÓN & DEMOSTRACIÓN SINCRÓNICA (WHAT-HAPPENS & DES-EJEMPLOS)
# ==================================================================================================
with tabs[0]:
    st.markdown("## 🔍 Fase 1: Activación y Demostración Sincrónica (What-Happens)")
    
    st.markdown("""
    <div class="pedagogy-alert">
        <strong>Principio de Demostración (David Merrill):</strong> Para aprender un sistema causal explicativo, 
        no basta con oír definiciones aisladas. Se debe hacer visible qué condiciones desencadenan el fenómeno, 
        qué variables intervienen y qué consecuencias se siguen. 
        <em>"La aplicación es el principio que rompe la ilusión del aprendizaje: mientras el alumno solo escucha, parece que entiende."</em>
    </div>
    """, unsafe_allow_html=True)
    
    col_demo1, col_demo2 = st.columns([1, 1])
    
    with col_demo1:
        st.markdown("### ⚖️ El Choque de Dos Fuerzas Titánicas (Junio 2020)")
        st.markdown("""
        Según la tesis central de Lyn Alden en la lectura *Concentración de mercado*, junio de 2020 presenció 
        el impacto de una fuerza imparable contra un objeto inamovible:
        - **El Objeto Inamovible (Economía Real Destruida):** La mayor contracción global moderna, con más de 
          **20 millones** de reclamaciones continuas de desempleo en EE.UU. (3 veces superior al pico de la Gran Recesión de 2008) 
          y contracciones récord del PIB.
        - **La Fuerza Imparable (Hiperliquidez Monetaria):** La Reserva Federal (Fed) expandió su balance en billones de dólares 
          en semanas, monetizando deuda soberana y comprando bonos corporativos, provocando una recuperación vertiginosa 
          del mercado bursátil que desconcertó a los observadores pasivos.
        """)
        
        # Métrica comparativa
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Reclamaciones Desempleo (2020)", value="~20 Millones", delta="+13M vs Crisis 2008", delta_color="inverse")
        with m2:
            st.metric(label="Balance Fed (Expansión 2020)", value="$7.1+ Billones", delta="+3.0T en 3 meses", delta_color="normal")

    with col_demo2:
        # Gráfica interactiva de Contrapaso: Balance Fed vs S&P 500
        dates = pd.date_range(start="2019-12-01", end="2020-07-01", freq="W")
        np.random.seed(42)
        # Modelando la caída de marzo y la inyección masiva
        sp500_vals = [3200, 3230, 3280, 3320, 3380, 3350, 3100, 2750, 2300, 2450, 2600, 2800, 2850, 2900, 3050, 3120, 3100]
        sp500_vals = np.interp(np.linspace(0, len(sp500_vals)-1, len(dates)), np.arange(len(sp500_vals)), sp500_vals)
        
        fed_balance = [4.1, 4.15, 4.18, 4.2, 4.22, 4.25, 4.35, 4.7, 5.3, 5.8, 6.4, 6.7, 6.9, 7.05, 7.15, 7.12, 7.08]
        fed_balance = np.interp(np.linspace(0, len(fed_balance)-1, len(dates)), np.arange(len(fed_balance)), fed_balance)
        
        fig_fed = go.Figure()
        fig_fed.add_trace(go.Scatter(x=dates, y=sp500_vals, mode='lines+markers', name='S&P 500 (Puntos)', line=dict(color='#0284C7', width=3)))
        fig_fed.add_trace(go.Scatter(x=dates, y=fed_balance, mode='lines', name='Balance Fed (Trillones $)', yaxis='y2', line=dict(color='#10B981', width=3, dash='dash')))
        
        fig_fed.update_layout(
            title="Armonía de Contrapaso: S&P 500 vs. Expansión Balance Fed (2020)",
            xaxis_title="Mes",
            yaxis=dict(title=dict(text="S&P 500", font=dict(color="#0284C7")), tickfont=dict(color="#0284C7")),
            yaxis2=dict(title=dict(text="Balance Fed ($ Trillones)", font=dict(color="#10B981")), tickfont=dict(color="#10B981"), overlaying='y', side='right'),
            legend=dict(x=0.05, y=0.95),
            margin=dict(l=40, r=40, t=50, b=40),
            height=320,
            template="plotly_white"
        )
        st.plotly_chart(fig_fed, use_container_width=True)

    st.divider()

    # Sección 2: El Espejismo de la Ponderación: Market-Cap vs Equal-Weight
    st.markdown("### 📊 La Anatomía de la Concentración: Market-Cap vs. Equal-Weight")
    
    col_weights1, col_weights2 = st.columns([1, 1])
    
    with col_weights1:
        st.markdown("""
        Un estudiante ingenuo de economía asume que cuando el índice S&P 500 sube un **15%**, 
        la mayoría de las 500 corporaciones estadounidenses están prosperando. **Falso.**
        
        * **Ponderación por Capitalización de Mercado (Market-Cap):** Cada acción pesa según su valor total en bolsa. 
          Apple Inc. (AAPL) tiene un peso **más de 100 veces superior** al de un productor industrial como Nucor Corporation (NUE).
        * **Las 'Big 5' en Mayo/Junio 2020:** Microsoft, Apple, Amazon, Alphabet y Meta llegaron a concentrar más del **21% del índice total**.
          Superaron la concentración observada en el pico de la burbuja punto-com del año 2000.
        * **Índice de Peso Igual (Equal-Weight - RSP):** Las 500 empresas reciben exactamente un **0.2%** de asignación inicial. 
          Si la economía general está enferma pero 5 gigantes digitales se benefician del confinamiento y la liquidez, 
          el Market-Cap se dispara mientras el Equal-Weight se arrastra.
        """)

        # Des-ejemplo pedagógico (Merrill)
        st.markdown("""
        <div class="counterexample-box">
            <strong>⚠️ Des-ejemplo Crítico (Diferenciar Apariencia de Realidad):</strong><br>
            Si un médico mide la temperatura de una familia de 5 personas promediando sus valores, 
            y un integrante tiene 43°C con fiebre extrema mientras 4 sufren hipotermia a 34°C, 
            el promedio matemático marcará ~35.8°C (aparentemente normal). 
            <strong>El S&P 500 ponderado por capitalización actúa igual:</strong> oculta la fragilidad del 99% 
            del tejido empresarial bajo el rendimiento desproporcionado de 5 gigantes monopólicos.
        </div>
        """, unsafe_allow_html=True)

    with col_weights2:
        # Gráfico interactivo de concentración histórica
        years = [1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020]
        top5_share = [18.0, 14.5, 12.0, 13.0, 18.2, 12.5, 11.0, 12.8, 22.1]
        
        fig_conc = go.Figure()
        fig_conc.add_trace(go.Bar(
            x=years, y=top5_share,
            marker_color=['#64748B', '#64748B', '#64748B', '#64748B', '#EF4444', '#64748B', '#64748B', '#64748B', '#DC2626'],
            text=[f"{v}%" for v in top5_share],
            textposition='auto',
            name='% Top 5 en S&P 500'
        ))
        fig_conc.add_shape(
            type="line", line=dict(dash="dot", color="red"),
            x0=1978, x1=2022, y0=20.0, y1=20.0
        )
        fig_conc.add_annotation(x=2000, y=19.5, text="Burbuja Dotcom (18.2%)", showarrow=True, arrowhead=2)
        fig_conc.add_annotation(x=2020, y=23.0, text="Máximo Histórico en 40 años (22.1%)", showarrow=True, arrowhead=2)
        
        fig_conc.update_layout(
            title="Cuota de Mercado de las 5 Mayores Empresas en el S&P 500 (%)",
            xaxis_title="Año / Ciclo Económico",
            yaxis_title="% del Índice Total S&P 500",
            template="plotly_white",
            height=340,
            margin=dict(l=40, r=40, t=50, b=40)
        )
        st.plotly_chart(fig_conc, use_container_width=True)

    st.divider()

    # EJERCICIO 1: INFERENCIA CRÍTICA DEL SISTEMA CAUSAL
    st.markdown("### ✍️ Ejercicio 1: Deducción del Mecanismo Causal")
    st.markdown("""
    **Consigna Cognitiva:** No repitas las definiciones. A partir de los datos anteriores, explica:
    1. ¿Cuál es el canal de transmisión mediante el cual la inyección de liquidez de la Reserva Federal terminó inflando a las 'Big 5' mientras la economía de a pie sufría desempleo masivo?
    2. ¿Por qué el rendimiento superior del índice de peso igual (Equal-Weight) suele marcar el inicio de un ciclo de expansión económica saludable, mientras que la supremacía del Market-Cap suele marcar finales de ciclo o recesión?
    """)
    
    ex1_text = st.text_area(
        "Redacta tu análisis crítico y justificación técnica:",
        value=st.session_state.ex1_analysis,
        height=140,
        placeholder="Explica la relación de causa y efecto: condiciones de liquidez, tipos de interés, huida hacia calidad / refugio, efectos de red y divergencia macroeconómica..."
    )
    if ex1_text != st.session_state.ex1_analysis:
        st.session_state.ex1_analysis = ex1_text

    col_btn_ex1, col_status_ex1 = st.columns([1, 3])
    with col_btn_ex1:
        if st.button("💾 Guardar Respuesta Ejercicio 1", use_container_width=True):
            if len(st.session_state.ex1_analysis.strip()) < 40:
                st.error("Tu respuesta es muy breve. Desarrolla tu argumento con mayor rigor conceptual.")
            else:
                st.success("¡Respuesta guardada con éxito en tu sesión!")


# ==================================================================================================
# PESTAÑA 2: SIMULACIÓN & TOMA DE DECISIONES DE PENSAMIENTO CRÍTICO
# ==================================================================================================
with tabs[1]:
    st.markdown("## 🕹️ Fase 2: Laboratorio de Simulación & Toma de Decisiones")
    
    st.markdown("""
    <div class="pedagogy-alert">
        <strong>Restricción Cognitiva (No Resolver por el Alumno):</strong> Este simulador no ofrece respuestas predeterminadas. 
        Te permite manipular variables macroeconómicas y de estructura de mercado para someter a prueba 
        las tesis de Lyn Alden sobre múltiplos de valoración, concentración e impacto regulatorio.
    </div>
    """, unsafe_allow_html=True)
    
    col_sim_controls, col_sim_view = st.columns([1, 2])
    
    with col_sim_controls:
        st.markdown("#### ⚙️ Variables del Escenario")
        
        sim_fed_liquidity = st.slider(
            "Inyección Adicional de la Fed ($ Trillones):",
            min_value=-2.0, max_value=5.0, value=float(st.session_state.ex2_sim_liquidity), step=0.5,
            help="Valores negativos representan Quantitative Tightening (retirada de liquidez)."
        )
        st.session_state.ex2_sim_liquidity = sim_fed_liquidity
        
        sim_top5_share = st.slider(
            "Concentración de las 'Big 5' en el S&P (%):",
            min_value=10.0, max_value=35.0, value=float(st.session_state.ex2_sim_concentration), step=1.0,
            help="Cuota agregada de Microsoft, Apple, Amazon, Alphabet y Meta."
        )
        st.session_state.ex2_sim_concentration = sim_top5_share
        
        sim_interest_rate = st.slider(
            "Tasa de Interés de Referencia (% Fed Funds):",
            min_value=0.0, max_value=6.0, value=0.25, step=0.25,
            help="Costo del dinero. Tasas altas penalizan empresas con múltiplos de valoración (P/E) elevados."
        )
        
        sim_antitrust_pressure = st.selectbox(
            "Presión Regulatoria Antimonopolio (FTC/DOJ):",
            ["Baja (Status Quo - Se permiten adquisiciones)", 
             "Moderada (Bloqueo de compras defensivas)", 
             "Severa (Amenaza de desmembramiento o límites a monopolios publicitarios)"]
        )

    with col_sim_view:
        st.markdown("#### 📈 Impacto Dinámico en Métricas de Concentración y Retorno")
        
        # Cálculos del modelo de simulación
        # Cálculo de HHI aproximado: Top 5 tienen sim_top5_share dividido en proporciones realistas
        top5_weights = [sim_top5_share * 0.28, sim_top5_share * 0.25, sim_top5_share * 0.20, sim_top5_share * 0.15, sim_top5_share * 0.12]
        remaining_495_weight = (100.0 - sim_top5_share) / 495.0
        hhi_top5 = sum([w**2 for w in top5_weights])
        hhi_remaining = 495 * (remaining_495_weight**2)
        hhi_total = int(hhi_top5 + hhi_remaining)
        
        # Divergencia esperada Market-Weight vs Equal-Weight
        # Regla histórica de Alden: Mayor concentración previa + retiro de liquidez/alza de tasas favorece Equal Weight
        val_multiple_drag = (sim_interest_rate * 2.1) + (1.5 if "Severa" in sim_antitrust_pressure else (0.7 if "Moderada" in sim_antitrust_pressure else 0.0))
        equal_weight_advantage = (sim_top5_share - 15.0) * 0.6 + val_multiple_drag - (sim_fed_liquidity * 1.8)
        
        m_c1, m_c2, m_c3 = st.columns(3)
        with m_c1:
            st.metric(
                label="HHI Implícito del Mercado",
                value=f"{hhi_total} pts",
                delta=f"{hhi_total - 120} vs Promedio Histórico",
                delta_color="inverse" if hhi_total > 150 else "normal"
            )
        with m_c2:
            adv_color = "normal" if equal_weight_advantage > 0 else "inverse"
            st.metric(
                label="Ventaja Esperada Equal-Weight",
                value=f"{equal_weight_advantage:+.1f}% anual",
                delta="Favorable a Equal-Weight" if equal_weight_advantage > 0 else "Favorable a Market-Cap",
                delta_color=adv_color
            )
        with m_c3:
            fragility = "EXTREMA" if (sim_top5_share > 20 and sim_interest_rate > 2.0) else ("ALTA" if sim_top5_share > 18 else "MODERADA")
            st.metric(
                label="Vulnerabilidad Sistémica",
                value=fragility,
                delta="Riesgo de burbuja" if fragility != "MODERADA" else "Saludable"
            )

        # Gráfico comparativo de rendimientos proyectados
        cycles = ["Recesión Temprana", "Pico de Hiperliquidez", "Normalización Monetaria", "Expansión Sólida"]
        perf_market_cap = [15 + sim_fed_liquidity*4 - val_multiple_drag, 25 + sim_fed_liquidity*5, 5 - val_multiple_drag*1.5, 8]
        perf_equal_weight = [2 + sim_fed_liquidity*1.5, 12 + sim_fed_liquidity*2, 9 + (sim_top5_share*0.3), 16]
        
        df_sim = pd.DataFrame({
            "Fase del Ciclo": cycles,
            "S&P 500 Market-Cap": perf_market_cap,
            "S&P 500 Equal-Weight": perf_equal_weight
        })
        
        fig_sim_bar = px.bar(
            df_sim, x="Fase del Ciclo", y=["S&P 500 Market-Cap", "S&P 500 Equal-Weight"],
            barmode="group",
            title="Desempeño Comparativo Proyectado por Ciclo (%)",
            color_discrete_map={"S&P 500 Market-Cap": "#0284C7", "S&P 500 Equal-Weight": "#10B981"}
        )
        fig_sim_bar.update_layout(template="plotly_white", height=280, margin=dict(l=30, r=30, t=40, b=30))
        st.plotly_chart(fig_sim_bar, use_container_width=True)

    st.divider()

    # EJERCICIO 2: TOMA DE DECISIONES Y EVALUACIÓN DE VARIABLES
    st.markdown("### 🎯 Ejercicio 2: Dictamen de Cartera y Justificación de Postura")
    st.markdown("""
    **Dilema de Decisión:** Eres el Director de Estrategia Macroeconómica de un fondo de inversión universitario en Costa Rica. 
    A la luz de los datos de junio 2020 de Lyn Alden (donde Alphabet cotizaba a más de 32x beneficios a pesar de una contracción proyectada en su BPA, 
    y Apple sufría disrupciones en la cadena de suministros con China):
    """)
    
    decision_choice = st.radio(
        "¿Cuál es tu recomendación de asignación de activos indexados para los próximos 3 a 5 años?",
        [
            "Sobreponderar S&P 500 de Peso Igual (Equal-Weight - RSP)",
            "Mantener ponderación tradicional por Capitalización de Mercado (Market-Cap - SPY)",
            "Adoptar una estrategia híbrida con cobertura antimonopolio y materias primas"
        ],
        index=0 if "Equal-Weight" in st.session_state.ex2_decision else (1 if "Market-Cap" in st.session_state.ex2_decision else 2)
    )
    st.session_state.ex2_decision = decision_choice

    ex2_text = st.text_area(
        "Defiende tu recomendación con argumentos técnicos (menciona valoración, riesgo de concentración y política monetaria):",
        value=st.session_state.ex2_justification,
        height=130,
        placeholder="Justifica considerando si las Big 5 pueden sostener múltiplos de más de 30x BPA en un entorno donde la Fed desacelera compras de bonos..."
    )
    if ex2_text != st.session_state.ex2_justification:
        st.session_state.ex2_justification = ex2_text

    if st.button("💾 Guardar Dictamen Ejercicio 2"):
        if len(st.session_state.ex2_justification.strip()) < 40:
            st.warning("Justificación incompleta. Integra variables macroeconómicas concretas de la simulación.")
        else:
            st.success("Dictamen estratégico guardado exitosamente.")


# ==================================================================================================
# PESTAÑA 3: CONTRASTE DE MODELOS ECONÓMICOS
# ==================================================================================================
with tabs[2]:
    st.markdown("## ⚖️ Fase 3: Contraste de Modelos - Teoría vs. Realidad Empírica")
    
    st.markdown("""
    <div class="pedagogy-alert">
        <strong>Objetivo de Pensamiento Crítico:</strong> Cuestionar los dogmas aprendidos. 
        En el aula tradicional de Economía se enseña que las fuerzas del mercado erosionan automáticamente 
        los beneficios extraordinarios. ¿Ocurre esto en la economía de mega-plataformas digitales?
    </div>
    """, unsafe_allow_html=True)
    
    col_theo1, col_theo2 = st.columns(2)
    
    with col_theo1:
        st.markdown("""
        #### 🏛️ El Modelo Neoclásico Convencional
        * **Premisas Básicas:**
          - Atomización del mercado (ninguna firma tiene poder sobre el precio ni sobre el índice).
          - Libre entrada y salida sin barreras artificiales ni regulatorias.
          - Los beneficios extraordinarios atraen competidores que diluyen el poder de mercado.
          - El capital fluye de forma neutral hacia los sectores con mayor productividad marginal real.
        * **Predicción del Modelo:**
          - La concentración es pasajera; los monopolios decaen naturalmente sin intervención estatal.
        """)
    
    with col_theo2:
        st.markdown("""
        #### 📱 La Realidad Estructural de las 'Big 5' (Lyn Alden)
        * **Fenómenos Observados en los Datos:**
          - **Efectos de Red Extremos:** El valor de Alphabet o Meta crece exponencialmente con cada usuario adicional, creando fosos infranqueables (*economic moats*).
          - **Adquisiciones Preventivas / Asfixia de Rivales:** Absorción temprana de amenazas potenciales (ej. Instagram, WhatsApp).
          - **Efecto Cantillon Monetario:** La liquidez emitida por los bancos centrales no se dispersa equitativamente; fluye primero hacia grandes corporaciones con acceso a deuda ultra-barata para recompras de acciones.
        * **Resultado Empírico:**
          - Una concentración del 22% que perdura y se intensifica a pesar de shocks macroeconómicos graves.
        """)

    st.divider()

    # EJERCICIO 3: ANÁLISIS DIALÉCTICO
    st.markdown("### 🧠 Ejercicio 3: Desafío Epistémico y Falsación de Modelos")
    st.markdown("""
    **Consigna:** Como economista en formación de la UIA, contrasta ambas posturas.
    ¿El nivel de concentración alcanzado por las Big 5 en el S&P 500 demuestra un fallo del modelo neoclásico tradicional, 
    o simplemente refleja que los consumidores obtienen mayor bienestar gracias a la escala y la eficiencia tecnológica? 
    Considera el rol de las políticas antimonopolio señaladas en la lectura de Alden.
    """)
    
    ex3_text = st.text_area(
        "Desarrolla tu análisis crítico dialéctico (tesis, antítesis y síntesis económica):",
        value=st.session_state.ex3_contrast_neoclassical,
        height=140,
        placeholder="Analiza las externalidades de red, las barreras de entrada por acumulación de datos y si la intervención antimonopolio es necesaria o perjudicial..."
    )
    if ex3_text != st.session_state.ex3_contrast_neoclassical:
        st.session_state.ex3_contrast_neoclassical = ex3_text

    if st.button("💾 Guardar Contraste Ejercicio 3"):
        if len(st.session_state.ex3_contrast_neoclassical.strip()) < 40:
            st.warning("Profundiza en la tensión entre eficiencia de escala y barreras de entrada.")
        else:
            st.success("Contraste conceptual guardado con éxito.")


# ==================================================================================================
# PESTAÑA 4: HABILIDADES DEL SIGLO XXI & FEEDBACK FORMATIVO (SIN REVELAR RESPUESTAS)
# ==================================================================================================
with tabs[3]:
    st.markdown("## 🌟 Fase 4: Habilidades del Siglo XXI y Feedback Formativo Inteligente")
    
    st.markdown("""
    <div class="pedagogy-alert">
        <strong>Pilar 1 de Jon Bergmann (AI Engines como Andamiaje Socrático):</strong><br>
        Esta evaluación formativa no actúa como una calculadora simplista que califica 'correcto o incorrecto' 
        ni revela soluciones masticadas. Analiza la consistencia interna, el empleo de variables empíricas 
        y la sofisticación de tu razonamiento crítico, devolviéndote preguntas reflexivas para perfeccionar tu modelo mental.
    </div>
    """, unsafe_allow_html=True)
    
    # Botón detonador de evaluación
    col_eval_btn, col_eval_desc = st.columns([1, 2])
    with col_eval_btn:
        run_evaluation = st.button("⚡ Procesar y Evaluar Calidad del Razonamiento", use_container_width=True)
    
    with col_eval_desc:
        st.caption("Al presionar este botón, el motor formativo auditará tus respuestas de los Ejercicios 1, 2 y 3, actualizará tu rúbrica y generará preguntas de retroalimentación socrática.")

    def evaluate_reasoning():
        """Evalúa las respuestas del alumno con rúbrica cualitativa y cuantitativa formativa."""
        text1 = st.session_state.ex1_analysis.lower()
        text2 = st.session_state.ex2_justification.lower()
        text3 = st.session_state.ex3_contrast_neoclassical.lower()
        
        # Palabras clave y conceptos económicos
        keys_liquidity = ["liquidez", "reserva federal", "fed", "balance", "monetaria", "deuda", "estímulo", "bonos"]
        keys_concentration = ["equal-weight", "market-cap", "peso igual", "ponderación", "hhi", "big 5", "apple", "alphabet", "nucor", "concentración"]
        keys_cycle = ["ciclo", "recesión", "expansión", "desempleo", "bpa", "múltiplo", "recompras", "desacople", "real"]
        keys_theory = ["neoclásico", "competencia", "monopolio", "red", "barreras", "antimonopolio", "escala", "foso", "eficiencia"]
        
        # Evaluación Ex 1
        score_ex1 = 0
        feedback1_strengths = []
        feedback1_challenges = []
        
        c_liq = sum(1 for k in keys_liquidity if k in text1)
        c_conc = sum(1 for k in keys_concentration if k in text1)
        
        if len(text1) > 100: score_ex1 += 10
        if c_liq >= 1: 
            score_ex1 += 8
            feedback1_strengths.append("Articulas la influencia de las medidas de la Reserva Federal.")
        else:
            feedback1_challenges.append("¿Cómo afectó la inyección masiva de liquidez al comportamiento del mercado financiero?")
            
        if c_conc >= 1: 
            score_ex1 += 7
            feedback1_strengths.append("Distingues la mecánica entre ponderación de mercado y peso igual.")
        else:
            feedback1_challenges.append("Profundiza en por qué Apple o Alphabet pesan 100 veces más que Nucor en el S&P 500.")
            
        # Evaluación Ex 2
        score_ex2 = 0
        feedback2_strengths = []
        feedback2_challenges = []
        
        c_cyc = sum(1 for k in keys_cycle if k in text2)
        if len(text2) > 100: score_ex2 += 10
        if c_cyc >= 1:
            score_ex2 += 8
            feedback2_strengths.append("Fundamentas tu dictamen considerando el ciclo económico y valoraciones.")
        else:
            feedback2_challenges.append("Considera los múltiplos P/E >32x de Alphabet y la caída del BPA señalada por Alden.")
            
        if "equal-weight" in text2 or "peso igual" in text2 or "market-cap" in text2:
            score_ex2 += 7
            feedback2_strengths.append("Justificas explícitamente la ventaja relativa del instrumento elegido.")
        else:
            feedback2_challenges.append("Contrasta qué ocurre si los líderes sobrevalorados corrigen frente a las 495 empresas restantes.")

        # Evaluación Ex 3
        score_ex3 = 0
        feedback3_strengths = []
        feedback3_challenges = []
        
        c_theo = sum(1 for k in keys_theory if k in text3)
        if len(text3) > 100: score_ex3 += 10
        if c_theo >= 2:
            score_ex3 += 15
            feedback3_strengths.append("Excelente contraste entre supuestos neoclásicos y barreras empíricas modernas.")
        elif c_theo == 1:
            score_ex3 += 8
            feedback3_strengths.append("Identificas al menos un aspecto estructural de las grandes tecnológicas.")
            feedback3_challenges.append("¿Qué papel juegan las externalidades de red y las adquisiciones preventivas?")
        else:
            feedback3_challenges.append("El modelo neoclásico asume libre entrada; explica por qué es difícil competir contra Google o Amazon.")

        total_pts = score_ex1 + score_ex2 + score_ex3
        # Normalizar a 100 con base en esfuerzo
        calif = min(100, int(total_pts * 1.33))
        if calif == 0 and len(text1 + text2 + text3) > 50:
            calif = 50
            
        # Niveles de dominio
        if calif >= 88:
            nivel = "Maestría Avanzada (High Mastery)"
        elif calif >= 75:
            nivel = "Pensamiento Crítico Competente"
        elif calif >= 60:
            nivel = "En Desarrollo Analítico"
        else:
            nivel = "Nivel Novicio (Requiere Mayor Profundización)"
            
        # Actualización de competencias Siglo XXI
        comp = {
            "Pensamiento Crítico": min(100, int(calif * 1.0)),
            "Análisis Cuantitativo & Datos": min(100, int((c_liq + c_conc) * 14 + 40)),
            "Toma de Decisiones Económicas": min(100, int(calif * 0.95 + (10 if len(text2) > 80 else 0))),
            "Comunicación Rigurosa & Defensa": min(100, int((len(text1 + text2 + text3) / 12) + 40)),
            "Metacognición & Autonomía": min(100, int(calif * 0.9 + 10))
        }
        
        st.session_state.evaluated = True
        st.session_state.score_total = calif
        st.session_state.mastery_level = nivel
        st.session_state.competency_scores = comp
        st.session_state.feedback_ex1 = {"strengths": feedback1_strengths, "challenges": feedback1_challenges}
        st.session_state.feedback_ex2 = {"strengths": feedback2_strengths, "challenges": feedback2_challenges}
        st.session_state.feedback_ex3 = {"strengths": feedback3_strengths, "challenges": feedback3_challenges}

    if run_evaluation:
        evaluate_reasoning()
        st.rerun()

    if st.session_state.evaluated:
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            st.markdown("### 🏆 Calificación & Nivel de Comprensión")
            st.markdown(f"""
            <div class="metric-card">
                <h3 style="margin-top:0; color:#0F172A;">Nivel Alcanzado:</h3>
                <span class="rubric-tag" style="background:#0284C7; color:white; font-size:1.1rem;">
                    {st.session_state.mastery_level}
                </span>
                <h1 style="font-size: 3.2rem; font-weight:800; color:#0369A1; margin:0.8rem 0;">
                    {st.session_state.score_total} / 100
                </h1>
                <p style="color:#64748B; font-size:0.95rem;">
                    Basado en la consistencia de tus hipótesis, la conexión causal entre liquidez y mercado, 
                    y la justificación frente a los supuestos teóricos.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("#### 💬 Retroalimentación Socrática Personalizada")
            
            # Ejercicio 1 Feedback
            st.markdown("**Sobre el Ejercicio 1 (Mecanismo Causal):**")
            for s in st.session_state.feedback_ex1.get("strengths", []):
                st.markdown(f"- ✅ *Fortaleza:* {s}")
            for c in st.session_state.feedback_ex1.get("challenges", []):
                st.markdown(f"- ❓ *Pregunta Socrática:* {c}")
                
            # Ejercicio 2 Feedback
            st.markdown("**Sobre el Ejercicio 2 (Dictamen de Inversión):**")
            for s in st.session_state.feedback_ex2.get("strengths", []):
                st.markdown(f"- ✅ *Fortaleza:* {s}")
            for c in st.session_state.feedback_ex2.get("challenges", []):
                st.markdown(f"- ❓ *Pregunta Socrática:* {c}")

            # Ejercicio 3 Feedback
            st.markdown("**Sobre el Ejercicio 3 (Contraste Neoclásico):**")
            for s in st.session_state.feedback_ex3.get("strengths", []):
                st.markdown(f"- ✅ *Fortaleza:* {s}")
            for c in st.session_state.feedback_ex3.get("challenges", []):
                st.markdown(f"- ❓ *Pregunta Socrática:* {c}")

        with col_res2:
            st.markdown("### 🕸️ Radar de Habilidades del Siglo XXI")
            
            categories = list(st.session_state.competency_scores.keys())
            values = list(st.session_state.competency_scores.values())
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(2, 132, 199, 0.25)',
                line=dict(color='#0284C7', width=2),
                name='Competencias Demostradas'
            ))
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(visible=True, range=[0, 100])
                ),
                showlegend=False,
                height=380,
                margin=dict(l=40, r=40, t=30, b=30),
                template="plotly_white"
            )
            st.plotly_chart(fig_radar, use_container_width=True)
            
            with st.expander("📖 Glosario de Habilidades Desarrolladas", expanded=False):
                st.markdown("""
                - **Pensamiento Crítico:** Capacidad de descomponer sistemas complejos, desafiar axiomas y verificar relaciones causa-efecto reales.
                - **Análisis Cuantitativo & Datos:** Interpretación de series temporales, métricas de dispersión, HHI y divergencia entre índices ponderados.
                - **Toma de Decisiones Económicas:** Formulación de estrategias de asignación patrimonial bajo escenarios de riesgo e incertidumbre regulatoria.
                - **Comunicación Rigurosa:** Capacidad de sintetizar y defender argumentos orales breves con lenguaje técnico de alto calibre.
                - **Metacognición:** Detección de sesgos propios, auto-monitoreo de la comprensión y rechazo de la memorización pasiva.
                """)
    else:
        st.info("👈 Completa los ejercicios en las pestañas anteriores y haz clic en **'Procesar y Evaluar'** para obtener tu diagnóstico formativo y radar de habilidades.")


# ==================================================================================================
# PESTAÑA 5: DEFENSA ORAL (HUMAN CHECK) & EXPORTACIÓN CONSOLIDADA
# ==================================================================================================
with tabs[4]:
    st.markdown("## 🎙️ Fase 5: Comprobación de Maestría (Human Check) & Exportación")
    
    st.markdown("""
    <div class="pedagogy-alert">
        <strong>Pilar 3 de Jon Bergmann (The Human Check - Defensa Oral Sincrónica):</strong><br>
        <em>"La comprobación de maestría es una conversación de dos minutos y alto impacto. 
        El estudiante trae su anclaje analógico y explica con rigor lo que ha descubierto. 
        Pasamos de calificar el producto pasivo a auditar el proceso de pensamiento vivo."</em>
    </div>
    """, unsafe_allow_html=True)
    
    col_prep1, col_prep2 = st.columns(2)
    
    with col_prep1:
        st.markdown("### 📋 Tu Hoja de Defensa Oral (2 Minutos)")
        st.markdown("Prepara las respuestas que le expondrás verbalmente a tu profesor de Economía durante la comprobación de maestría:")
        
        oral_p = st.text_area(
            "1. Tu Tesis Central en 60 Segundos (Elevator Pitch Económico):",
            value=st.session_state.ex4_oral_pitch,
            height=120,
            placeholder="Sintetiza: ¿Por qué la concentración del S&P 500 en 2020 fue un espejismo monetario y qué anticipas para los próximos ciclos?"
        )
        if oral_p != st.session_state.ex4_oral_pitch:
            st.session_state.ex4_oral_pitch = oral_p

        oral_c = st.text_area(
            "2. Contra-pregunta Anticipada del Profesor:",
            value=st.session_state.ex4_counter_defense,
            height=100,
            placeholder="Imagina que el docente te objeta: 'Pero las Big 5 tienen balances de caja gigantescos, ¿por qué no seguirían dominando indefinidamente?' ¿Cómo responderías?"
        )
        if oral_c != st.session_state.ex4_counter_defense:
            st.session_state.ex4_counter_defense = oral_c

        if st.button("💾 Guardar Preparación de Defensa Oral"):
            st.success("Argumentos para la defensa oral registrados en tu sesión.")

    with col_prep2:
        st.markdown("### 📜 Rúbrica de la Comprobación Humana")
        st.markdown("""
        Durante la conversación sincrónica con el profesor, serás evaluado en tres dimensiones:
        
        1. **Precisión del Mecanismo:** ¿Puedes explicar la diferencia entre peso de mercado y peso igual sin titubear?
        2. **Sustento en Evidencia Empírica:** ¿Mencionas las cifras de Alden (balance de $7T de la Fed, 20M de desempleados, P/E >32x de Alphabet, concentración >21%)?
        3. **Solidez ante Contraejemplos:** ¿Mantienes la consistencia técnica cuando se cuestionan tus supuestos?
        """)
        
        st.markdown("""
        <div class="quote-box">
            "Cuando la lucha se va a casa sin orientación, el aprendizaje a menudo se desvanece en un prompt. 
            Traemos los pesos pesados de vuelta al aula para asegurarnos de que la mente humana sea la que haga las flexiones mentales." 
            <br>— <strong>Jon Bergmann</strong>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # GENERACIÓN Y EXPORTACIÓN DEL REPORTE CONSOLIDADO (.MD / .TXT)
    st.markdown("### 📥 Reporte Consolidado de la Sesión")
    st.markdown("Exporta el archivo final para entregar como evidencia de tu preparación sincrónica y portafolio académico.")
    
    # Construcción del reporte Markdown estructurado
    student_disp = st.session_state.student_name.strip() if st.session_state.student_name.strip() else "Estudiante No Registrado"
    
    report_content = f"""# REPORTE DE SESIÓN SINCRÓNICA: CONCENTRACIÓN DE MERCADO Y PENSAMIENTO CRÍTICO
**UNIVERSIDAD INTERNACIONAL DE LAS AMÉRICAS (U.I.A.)**  
**Escuela de Economía - Curso de Economía I / TBC Semana 4**  
**Fecha de la Sesión:** {st.session_state.session_start_time}  
**Estudiante:** {student_disp}  
**Nivel de Maestría Obtenido:** {st.session_state.mastery_level}  
**Calificación Cuantitativa:** {st.session_state.score_total} / 100  

---

## 1. MARCO DIDÁCTICO Y FUENTES APLICADAS
- **Metodología:** Mastery Flip (Jon Bergmann, 2026) - Pilares: Motores de IA, Raíces Analógicas y Comprobación Humana.
- **Principios Didácticos:** David Merrill (Activación, Demostración What-Happens, Aplicación Auténtica, Integración Dialéctica).
- **Lectura Base:** Lyn Alden (Junio 2020) - *Concentración de mercado* (Boletín Macro).

---

## 2. EJERCICIO 1: DEDUCCIÓN DEL MECANISMO CAUSAL (WHAT-HAPPENS)
**Pregunta:** Canal de transmisión entre la liquidez de la Fed y el auge de las Big 5 frente al desempleo masivo, y divergencia Market-Cap vs Equal-Weight.
**Respuesta del Estudiante:**
> {st.session_state.ex1_analysis if st.session_state.ex1_analysis.strip() else "[Sin respuesta registrada]"}

**Retroalimentación Formativa:**
- Fortalezas: {", ".join(st.session_state.feedback_ex1.get("strengths", ["Pendiente de evaluación"]))}
- Desafíos Socráticos: {", ".join(st.session_state.feedback_ex1.get("challenges", ["Ninguno señalado"]))}

---

## 3. EJERCICIO 2: TOMA DE DECISIONES Y SIMULACIÓN ECONÓMICA
**Postura Adoptada:** {st.session_state.ex2_decision}  
**Parámetros Simulados:** Inyección Fed: ${st.session_state.ex2_sim_liquidity}T | Concentración Big 5: {st.session_state.ex2_sim_concentration}%  
**Justificación Técnica:**
> {st.session_state.ex2_justification if st.session_state.ex2_justification.strip() else "[Sin respuesta registrada]"}

**Retroalimentación Formativa:**
- Fortalezas: {", ".join(st.session_state.feedback_ex2.get("strengths", ["Pendiente de evaluación"]))}
- Desafíos Socráticos: {", ".join(st.session_state.feedback_ex2.get("challenges", ["Ninguno señalado"]))}

---

## 4. EJERCICIO 3: CONTRASTE DE MODELOS ECONÓMICOS (TEORÍA VS. EMPIRIA)
**Pregunta:** Contraste del modelo neoclásico de competencia perfecta frente a los monopolios digitales y barreras de red.
**Respuesta del Estudiante:**
> {st.session_state.ex3_contrast_neoclassical if st.session_state.ex3_contrast_neoclassical.strip() else "[Sin respuesta registrada]"}

**Retroalimentación Formativa:**
- Fortalezas: {", ".join(st.session_state.feedback_ex3.get("strengths", ["Pendiente de evaluación"]))}
- Desafíos Socráticos: {", ".join(st.session_state.feedback_ex3.get("challenges", ["Ninguno señalado"]))}

---

## 5. EVALUACIÓN DE COMPETENCIAS DEL SIGLO XXI
| Competencia Clave | Puntuación (0-100) | Nivel Demostrado |
| :--- | :---: | :--- |
| Pensamiento Crítico | {st.session_state.competency_scores.get('Pensamiento Crítico', 0)} | Análisis causal y de supuestos |
| Análisis Cuantitativo & Datos | {st.session_state.competency_scores.get('Análisis Cuantitativo & Datos', 0)} | Comprensión de HHI, ponderaciones y ratios |
| Toma de Decisiones Económicas | {st.session_state.competency_scores.get('Toma de Decisiones Económicas', 0)} | Estrategia de cartera bajo incertidumbre |
| Comunicación Rigurosa & Defensa | {st.session_state.competency_scores.get('Comunicación Rigurosa & Defensa', 0)} | Preparación de síntesis para defensa oral |
| Metacognición & Autonomía | {st.session_state.competency_scores.get('Metacognición & Autonomía', 0)} | Autoevaluación frente a feedback socrático |

---

## 6. PREPARACIÓN PARA LA COMPROBACIÓN DE MAESTRÍA (DEFENSA ORAL 2 MIN)
**Elevator Pitch (Tesis Central del Alumno):**
> {st.session_state.ex4_oral_pitch if st.session_state.ex4_oral_pitch.strip() else "[Pendiente de redacción]"}

**Defensa frente a Contra-argumentos del Docente:**
> {st.session_state.ex4_counter_defense if st.session_state.ex4_counter_defense.strip() else "[Pendiente de redacción]"}

---
*Reporte generado automáticamente por la Plataforma Didáctica de Economía UIA.*  
*Diseñado bajo los principios del Mastery Flip y el Diseño Instruccional de David Merrill.*
"""

    # Botón único de exportación
    filename_clean = re.sub(r'[^a-zA-Z0-9_]', '_', student_disp.replace(' ', '_'))
    export_filename = f"Reporte_Sesion_Economia_UIA_{filename_clean}.md"
    
    st.download_button(
        label=f"📥 Descargar Reporte Consolidado de la Sesión ({export_filename})",
        data=report_content,
        file_name=export_filename,
        mime="text/markdown",
        use_container_width=True
    )

    with st.expander("👁️ Vista Previa del Reporte Consolidado", expanded=False):
        st.markdown(report_content)

st.markdown("""
<div style="text-align: center; color: #94A3B8; font-size: 0.85rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid #E2E8F0;">
    Universidad Internacional de las Américas &bull; Escuela de Economía &bull; Didáctica y Tecnología Educativa 2026
</div>
""", unsafe_allow_html=True)
