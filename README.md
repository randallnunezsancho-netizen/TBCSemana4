# 🏛️ Plataforma Didáctica de Economía: Concentración de Mercado & Pensamiento Crítico

> **Universidad Internacional de las Américas (U.I.A.)**  
> **Escuela de Economía** — *Curso: Economía I / Introducción a la Economía (Semana 4)*  
> **Metodología Didáctica:** *Mastery Flip (Jon Bergmann, 2026)* & *Principios de Instrucción (David Merrill)*

---

## 📖 1. Descripción General del Proyecto y Propósito

Esta aplicación web interactiva, desarrollada en **Python** con **Streamlit**, está diseñada específicamente para estudiantes de primer ingreso de la carrera de Economía en la **Universidad Internacional de las Américas (U.I.A.)**.

El propósito fundamental de la plataforma es **fomentar el pensamiento crítico genuino y autónomo**, rompiendo con la memorización pasiva, la repetición acrítica de fórmulas y la trampa de la "estupefacción por IA" (*AI Stupefaction*).

### 🎯 Enfoque Pedagógico Integrado

La plataforma materializa la transición entre dos grandes hitos didácticos del curso:

1. **La Sesión Sincrónica — Raíces Analógicas (*Analog Roots*):**
   - **Fase de Demostración $\rightarrow$ Exposición Docente $\rightarrow$ Trabajo en la Aplicación Web:** El estudiante explora el sistema causal (*What-Happens*) que explica el desacople entre los mercados financieros y la economía real durante la crisis de junio de 2020.
2. **Comprobación de Maestría (*Human Check*):**
   - **Fase de Aplicación $\rightarrow$ Defensa Oral (2 minutos):** El estudiante utiliza el *Analog Anchor* generado por la app para defender de manera concisa y rigurosa sus hipótesis y decisiones de inversión ante el docente.

---

## ✨ 2. Características Principales Implementadas

La plataforma cuenta con un flujo cognitivo estructurado en cinco fases progresivas:

- **👤 Registro y Persistencia de Sesión (`st.session_state`):** Identificación del alumno y almacenamiento acumulativo en memoria de todas sus respuestas, parámetros de simulación y diagnósticos formativos.
- **📚 Barra Lateral (Sidebar) de Contexto Pedagógico:** Resumen visible de los 3 pilares del *Mastery Flip* (Jon Bergmann), los 4 principios del diseño didáctico (David Merrill), las fuentes macroeconómicas analizadas y un medidor interactivo de avance porcentual.
- **📊 Fase 1: Demostración Sincrónica y Sistema Causal (*What-Happens*):**
  - Gráfico interactivo en **Plotly** de la *armonía de contrapaso* entre la expansión del balance de la Reserva Federal ($7.1B) y el rebote del S&P 500, contrastado con 20 millones de solicitudes continuas de desempleo.
  - Visualización histórica (1980–2020) del incremento de la concentración de las *Big 5* (Microsoft, Apple, Amazon, Alphabet y Meta) superando el **22%** del S&P 500 (máximo histórico en 40 años, superior a la burbuja puntocom de 2000).
  - *Des-ejemplo Didáctico de Merrill:* Demostración de cómo la ponderación por capitalización bursátil (*Market-Cap*) disfraza la fragilidad de 495 empresas bajo el rendimiento de 5 gigantes monopólicos.
- **🕹️ Fase 2: Laboratorio de Simulación y Toma de Decisiones:**
  - Controles deslizantes para manipular la inyección de liquidez de la Fed, la cuota agregada de las *Big 5*, la tasa de interés de referencia y la presión regulatoria antimonopolio (*Antitrust*).
  - Cálculo algorítmico en tiempo real del **Índice Herfindahl-Hirschman (HHI)** implícito, la ventaja proyectada del índice de peso igual (*Equal-Weight - RSP*) y el indicador de vulnerabilidad sistémica.
  - Dilema auténtico de inversión donde el estudiante asume el rol de Director de Estrategia Macroeconómica para justificar la asignación de cartera de un fondo universitario.
- **⚖️ Fase 3: Contraste Dialéctico de Modelos (Teoría vs. Realidad Empírica):**
  - Confrontación entre los axiomas del modelo neoclásico de competencia perfecta (atomización, libre entrada, disolución natural de rentas extraordinarias) y la evidencia moderna de externalidades de red, adquisiciones preventivas y el *efecto Cantillon* monetario.
- **🌟 Fase 4: Feedback Formativo Inteligente y Radar de Habilidades:**
  - Motor de evaluación socrática en Python que analiza la profundidad causal y el rigor conceptual de las respuestas sin entregar soluciones predeterminadas ni masticadas.
  - Rúbrica formativa con cuatro niveles de maestría: *Novicio*, *En Desarrollo*, *Competente* y *Maestría Avanzada (High Mastery)*.
  - Gráfico polar (Radar Chart) con las 5 dimensiones de las **Competencias del Siglo XXI**: Pensamiento Crítico, Análisis de Datos, Toma de Decisiones, Comunicación Rigurosa y Metacognición.
- **🎙️ Fase 5: Preparación de la Defensa Oral y Exportación Consolidada:**
  - Generador de la hoja de defensa oral (*Elevator Pitch* de 60 segundos y anticipación de contra-preguntas del profesor).
  - **Botón Único de Exportación:** Genera y descarga un informe exhaustivo en formato Markdown (`.md`) con toda la evidencia del portafolio del alumno.

---

## 💻 3. Requisitos Técnicos

### Versión del Intérprete

- **Python:** Versión **3.10** o superior (probado y validado en **Python 3.13**).

### Librerías Principales

| Paquete | Versión Recomendada | Propósito en el Proyecto |
| :--- | :--- | :--- |
| `streamlit` | `>= 1.30.0` | Framework web reactivo e interfaz de usuario |
| `plotly` | `>= 5.18.0` | Gráficos interactivos (Series temporales, barras agrupadas y radar polar) |
| `pandas` | `>= 2.0.0` | Manipulación y estructuración de datos tabulares |
| `numpy` | `>= 1.26.0` | Interpolación matemática y cálculos algorítmicos (HHI, retornos) |

*(El detalle exhaustivo de dependencias y submódulos se encuentra en el archivo [`requirements.txt`](requirements.txt)).*

---

## 🛠️ 4. Instrucciones de Instalación Paso a Paso

Sigue estas instrucciones para clonar y ejecutar el entorno localmente:

### Paso 1: Clonar el repositorio

Abre una terminal (PowerShell en Windows o Bash en macOS/Linux) y clona el proyecto:

```bash
git clone https://github.com/randallnunezsancho-netizen/TBCSemana4.git
cd "TBCSemana4"
```

### Paso 2: Crear y activar un entorno virtual

Se recomienda crear un entorno virtual aislado para evitar conflictos de dependencias:

- **En Windows (PowerShell):**

  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```

* **En macOS / Linux:**

  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Paso 3: Instalar las dependencias

Con el entorno virtual activado, instala los requisitos necesarios:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Paso 4: Ejecutar la aplicación

Inicia el servidor local de Streamlit:

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador web predeterminado en la dirección:
👉 **`http://localhost:8501`**

---

## 🧭 5. Guía de Uso con Ejemplos Básicos

1. **Ingreso y Registro:**
   - En la barra lateral izquierda, ingresa tu **Nombre Completo**. Esto personalizará tu portafolio y activará el seguimiento de tu progreso.
2. **Pestaña 1 (Activación y Demostración):**
   - Examina las gráficas de contrapaso del balance de la Fed y la concentración histórica.
   - Lee el des-ejemplo pedagógico.
   - Redacta tu análisis en el **Ejercicio 1** explicando cómo la inyección monetaria benefició de forma desproporcionada a las empresas tecnológicas mientras la economía real se contraía. Presiona `Guardar Respuesta`.
3. **Pestaña 2 (Simulación y Toma de Decisiones):**
   - Mueve los controles de la simulación: eleva la inyección de la Fed a `$4.0T` o aumenta la tasa de interés a `4.5%`. Observa cómo cambian en tiempo real el HHI implícito y la ventaja esperada del índice de peso igual (*Equal-Weight*).
   - En el **Ejercicio 2**, selecciona tu recomendación estratégica de cartera y redacta tu justificación técnica. Presiona `Guardar Dictamen`.
4. **Pestaña 3 (Contraste de Modelos):**
   - Lee las columnas comparativas entre la teoría neoclásica y la economía de plataformas digitales.
   - En el **Ejercicio 3**, elabora tu respuesta dialéctica contrastando eficiencia de escala frente a barreras a la competencia.
5. **Pestaña 4 (Feedback y Competencias):**
   - Haz clic en el botón **`⚡ Procesar y Evaluar Calidad del Razonamiento`**.
   - Revisa tu nivel de dominio alcanzado, lee las preguntas socráticas para identificar sesgos y analiza tu **Radar de Habilidades del Siglo XXI**.
6. **Pestaña 5 (Defensa Oral y Exportación):**
   - Redacta tu *Elevator Pitch* de 60 segundos y tu respuesta a contra-preguntas.
   - Presiona el botón **`📥 Descargar Reporte Consolidado de la Sesión`** para obtener tu archivo `.md`, listo para ser entregado en el campus virtual o como portafolio para la sesión sincrónica.

---

## 📂 6. Estructura del Proyecto y Archivos Clave

```plaintext
semana 4/
├── .git/                                                  # Historial de control de versiones Git
├── app.py                                                 # Aplicación web completa en Streamlit
├── requirements.txt                                       # Especificación de dependencias del entorno
├── funcionalidades.txt                                     # Requerimientos didácticos y técnicos del sistema
├── README.md                                              # Documentación general y manual del usuario
│
├── 2020 06 - Concentración de mercado.pdf                 # Boletín económico de Lyn Alden (fuente empírica)
├── MasteryFlip-A_Guide_to_the_Future_of_Educcation.pdf    # Guía metodológica de Jon Bergmann (2026)
├── substack.com-Los 4 principios del diseño didáctico.pdf # Principios de David Merrill (activación, demostración, etc.)
├── Método de estudio sugerido.pdf                         # Plan de clase invertida y fases sincrónicas UIA
└── competencias_siglo_xxi.pdf                             # Marco de competencias para el siglo XXI
```

---

## 📊 7. Interpretación Pedagógica de Resultados

La aplicación evalúa el aprendizaje a través de métricas cuantitativas y cualitativas diseñadas para enriquecer la reflexión del estudiante:

### 1. Índice Herfindahl-Hirschman (HHI) y Concentración

* **Interpretación:** Un HHI bajo ($< 100$) en un índice de 500 empresas denota diversificación real. Sin embargo, cuando las 5 principales compañías superan el 20% del índice, el HHI se duplica y el índice se vuelve vulnerable a correcciones idiosincráticas de unas pocas corporaciones.
- **Pregunta de Reflexión:** ¿Está el mercado en bonanza o está expuesto a un riesgo sistémico oculto?

### 2. Divergencia Market-Cap vs. Equal-Weight

* **Fases Tardías / Recesión:** La ponderación por capitalización (*Market-Cap*) suele superar temporalmente al índice de peso igual porque los inversores huyen hacia mega-corporaciones con liquidez masiva.
- **Fases Tempranas de Expansión:** Históricamente, el índice de peso igual (*Equal-Weight*) supera de forma contundente en los nuevos ciclos, debido a que las acciones líderes previas quedan sobrevaloradas y el crecimiento se democratiza en el resto de los sectores económicos.

### 3. Rúbrica de Maestría Cognitiva

* **Nivel Novicio ($< 60$ pts):** Respuestas breves que memorizan definiciones sin conectarlas con datos reales.
- **En Desarrollo ($60 - 74$ pts):** Identifica variables aisladas (ej. balance de la Fed o desempleo), pero carece de un encadenamiento causal completo.
- **Pensamiento Crítico Competente ($75 - 87$ pts):** Demuestra consistencia causal, conecta la política monetaria con las valuaciones y contrasta la teoría con los hechos.
- **Maestría Avanzada ($88 - 100$ pts):** Análisis dialéctico riguroso, anticipación de contraejemplos y formulación de juicios económicos fundamentados.

---

## 📜 8. Licencia y Nota Educativa

### Declaración de Fines Académicos
>
> **NOTA EDUCATIVA:** Este proyecto ha sido desarrollado exclusivamente con fines didácticos y de investigación formativa para la **Universidad Internacional de las Américas (U.I.A.)** en Costa Rica. Los datos, análisis y simulaciones tienen como objetivo el entrenamiento pedagógico de estudiantes universitarios y no constituyen asesoría financiera ni recomendaciones de inversión profesional.

### Licencia

Este repositorio se distribuye bajo la licencia **MIT License**, permitiendo su uso, estudio, adaptación y mejora continua para entornos académicos y formativos.

---
*Plataforma desarrollada por el equipo docente de la Escuela de Economía — Universidad Internacional de las Américas, 2026.*
