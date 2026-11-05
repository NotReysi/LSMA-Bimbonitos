# Práctica 1. Programación de un agente inteligente (reactivo o basado en modelos/objetivos) en un entorno simulado.

**Link a Notion:** https://erickordazr.notion.site/Pr-ctica-1-Programaci-n-de-un-agente-inteligente-reactivo-o-basado-en-modelos-objetivos-en-un-ent-d53598df262b82d2b43801b7a5c7fa86

<aside>  
❗

**Valor: 25 puntos** (se califica sobre 100).

</aside>

## Competencia Específica

> El estudiante será capaz de **implementar y verificar** el ciclo percepción-decisión-acción de un agente inteligente, utilizando dos arquitecturas de programa de agente (reflejo simple y basado en modelos) en Python sobre un entorno simulado de observabilidad parcial, con el fin de **justificar mediante evidencia experimental propia** las diferencias de desempeño entre ambas arquitecturas.

## Descripción de la Actividad

En esta práctica, cada equipo trabaja con un agente que explora una cuadrícula bidimensional con obstáculos y muestras (puntos de interés) ocultas. El agente cuenta con observabilidad parcial: en cada instante percibe únicamente las cuatro celdas adyacentes a su posición, nunca el mapa completo. Esta restricción reproduce en código la condición de percepción parcial estudiada en la sesión introductoria del curso teórico simultáneo.

El equipo recibe un script base (`practica1_agente_explorador.py`) que ya implementa ambas arquitecturas de agente. La actividad no consiste en programar desde cero, sino en ejecutar, modificar sistemáticamente y analizar el comportamiento del sistema bajo distintas condiciones, documentando con evidencia propia por qué una arquitectura con memoria del entorno supera de manera consistente a una que carece de ella.

[practica1_agente_explorador.py](attachment:074d8028-ee97-4282-934d-81a222af9b43:practica1_agente_explorador.py)

Sistemas a implementar y verificar durante la sesión:

1. Agente de reflejo simple (reactivo): decide únicamente a partir del percepto actual.
2. Agente basado en modelos: mantiene un mapa interno del entorno explorado y lo utiliza para decidir.
3. Comparación controlada de ambas arquitecturas sobre cuatro configuraciones distintas del entorno (semilla, dificultad, energía disponible y pesos de la medida de desempeño).

## Contenido Teórico de Referencia

Se presenta a continuación un resumen mínimo, suficiente para comprender el código de la práctica. Para la fundamentación completa, remitirse al material de la sesión introductoria del curso.

**El ciclo percepción-decisión-acción.** Todo agente, sin importar su arquitectura, opera mediante tres operaciones: percibe el entorno a través de sensores, decide una acción con base en lo percibido, y actúa sobre el entorno mediante actuadores. El entorno cambia como consecuencia de la acción, y el ciclo se repite (Russell y Norvig, 2020).

**Definición — Agente de reflejo simple.** Programa de agente que selecciona su acción exclusivamente a partir del percepto actual, mediante reglas de condición-acción, sin conservar ningún registro de estados anteriores del entorno.

**Definición — Agente basado en modelos.** Programa de agente que mantiene una representación interna (modelo) del entorno, construida a partir del historial de percepciones, y la utiliza para decidir su acción en cada paso.

**Medida de desempeño.** Conforme a la regla revisada en clase, la medida de desempeño debe definirse sobre estados del entorno (por ejemplo, celdas exploradas o muestras recolectadas) y no sobre las acciones o intenciones internas del agente.

|Aspecto|Agente reactivo|Agente basado en modelos|
|---|---|---|
|Información usada para decidir|Solo el percepto actual|Percepto actual + mapa interno acumulado|
|Memoria del entorno|Ninguna|Mapa interno actualizado en cada percepción|
|Comportamiento típico|Puede revisitar celdas ya exploradas|Se dirige preferentemente a territorio no explorado|
|Costo de implementación|Bajo|Mayor (requiere estructura de datos y búsqueda)|

## Explicación del Código Base

El script `practica1_agente_explorador.py` se entrega extensamente comentado. A continuación se explica la función de cada componente, no su sintaxis línea por línea.

**Sección de parámetros (`ParametrosPractica`).** Concentra todos los valores que el equipo debe modificar para las variaciones solicitadas en el Procedimiento: tamaño del entorno, densidad de obstáculos, número de muestras, semilla aleatoria, energía disponible y los pesos de la medida de desempeño.

**El entorno (`Entorno`).** Representa la cuadrícula y conoce la disposición real de obstáculos y muestras. Expone únicamente el método `percibir_adyacentes`, que entrega al agente el contenido de las cuatro celdas vecinas, nunca el mapa completo. Esta restricción es la que impone la observabilidad parcial descrita en el Contenido Teórico.

**La clase base (`AgenteExplorador`).** Define el contrato común a cualquier arquitectura: los métodos `percibir`, `decidir` y `actuar`. Ambas arquitecturas comparten `percibir` y `actuar`; cada una implementa su propio `decidir`, que es precisamente donde reside la diferencia conceptual entre ellas.

**Agente reactivo (`AgenteReactivo`).** Su método `decidir` aplica reglas de condición-acción sobre el percepto inmediato: si hay una muestra adyacente, se dirige hacia ella; en caso contrario, elige al azar una celda libre adyacente.

**Agente basado en modelos (`AgenteBasadoEnModelos`).** Añade una variable de instancia, `mapa_interno`, que actualiza en cada percepción. Su método `decidir` consulta dicho mapa para ubicar la frontera de exploración más cercana (la celda conocida más próxima adyacente a territorio no registrado) mediante una búsqueda en anchura, y calcula la ruta más corta conocida hacia ella.

**El simulador (`ejecutar_episodio`).** Repite el ciclo percepción-decisión-acción hasta agotar la energía disponible, y registra tanto la trayectoria como una bitácora narrada de las decisiones tomadas, útil para redactar el Procedimiento.

**Comparación y reportes (`comparar_arquitecturas`, `generar_figura_comparativa`, `generar_animacion`).** Ejecutan ambas arquitecturas sobre un entorno idéntico (misma semilla) y generan la tabla comparativa, la figura estática y la animación del recorrido que deben incluirse en Resultados y Análisis.

## Contenido del Entregable

1. **Portada** — nombre de la actividad, integrantes, matrículas, número de equipo, nombre del asesor y fecha. Plantilla LaTeX institucional.
2. **Objetivo** — qué se busca demostrar: que la arquitectura basada en modelos supera de forma medible a la reactiva en cobertura del entorno y recolección de muestras, bajo condiciones idénticas.
3. **Marco Teórico** — ciclo percepción-decisión-acción; definición de agente de reflejo simple y de agente basado en modelos; regla de definición de la medida de desempeño sobre estados del entorno. Mínimo una cita textual por concepto.
4. **Materiales y Herramientas** — Python 3.10 o superior; bibliotecas `matplotlib` y `pillow`; script base `practica1_agente_explorador.py`; editor de texto o entorno de desarrollo integrado (IDE).
5. **Procedimiento** — descripción paso a paso de la ejecución realizada, incluyendo capturas de pantalla de la terminal y de las figuras generadas en cada una de las siguientes variaciones obligatorias de `ParametrosPractica`:
    - Variación de semilla aleatoria (mínimo tres semillas distintas).
    - Variación de la densidad de obstáculos (`densidad_obstaculos = 0.30`).
    - Variación del presupuesto de energía (`energia_maxima = 30`).
    - Variación de los pesos de la medida de desempeño (`peso_energia = 1.0`).
6. **Resultados y Análisis** — para cada una de las cuatro variaciones: la tabla comparativa generada por el script, la figura correspondiente (`comparacion_practica1.png`) y un análisis escrito que explique el resultado en términos del ciclo percepción-decisión-acción de cada arquitectura, no solo en términos numéricos.
7. **Conclusiones** — cada integrante del equipo redacta su propia reflexión individual sobre la evidencia obtenida y su relación con los contenidos de la sesión introductoria del curso.
8. **Referencias** — mínimo 3 fuentes. Formato APA.
9. **Anexos** — código fuente completo `practica1_agente_explorador.py`, incluido dentro del PDF mediante el entorno `lstlisting`, o enlace a repositorio Git del equipo.

## Formato del Documento

El documento debe seguir **exclusivamente** la **plantilla LaTeX institucional**.

El PDF es el único archivo entregable. No se aceptan archivos adicionales de ningún tipo.

## Criterios de Evaluación

|Criterio|Porcentaje|Descripción|
|---|---|---|
|Implementación y verificación del ciclo percepción-decisión-acción|30%|Ambas arquitecturas se ejecutan correctamente y el equipo demuestra comprensión de su funcionamiento interno.|
|Resultados y Análisis|25%|Las cuatro variaciones obligatorias están documentadas con tabla, figura e interpretación propia, no solo datos crudos.|
|Marco Teórico|15%|Definiciones correctas de ambas arquitecturas y de la medida de desempeño, con cita textual.|
|Conclusiones|15%|Reflexión personal de cada integrante, evidenciando relación explícita con los contenidos del curso.|
|Formato y Portada|10%|Documento generado exclusivamente desde la plantilla LaTeX institucional en Overleaf, sin errores de compilación.|
|Referencias|5%|Mínimo 3 fuentes correctamente citadas en formato APA.|

## Entrega de la Actividad

- **Modalidad:** En equipo de 3 a 4 integrantes.
- **Plataforma:** Microsoft Teams.
- **Formato de entrega:** Un solo archivo PDF generado desde LaTeX. Todo el material complementario (código, capturas, datos) debe incluirse dentro del PDF como anexos o mediante enlaces referenciados en el documento. No se aceptan archivos .zip, .rar ni adjuntos adicionales.
- **Responsable de entrega:** Un solo integrante por equipo (el representante) realiza la entrega. Los demás integrantes no deben entregar.

**Nombrado del archivo:**

```
LSMA-L-V3-01-AF4
```

## Guías y Lineamientos

- **Indicaciones generales para la entrega de actividades:** [](https://app.notion.com/Indicaciones-para-la-entrega-de-tareas-239598df262b80a5b34cebadea9a25ae?pvs=21)[https://erickordazr.notion.site/Indicaciones-para-la-entrega-de-tareas-239598df262b80a5b34cebadea9a25ae](https://erickordazr.notion.site/Indicaciones-para-la-entrega-de-tareas-239598df262b80a5b34cebadea9a25ae)
- **Guía para el formato del documento en LaTeX:** [](https://app.notion.com/Gu-a-para-usar-la-plantilla-de-actividades-en-Overleaf-238598df262b802098d2d9957542f8d4?pvs=21)[https://erickordazr.notion.site/Gu-a-para-usar-la-plantilla-de-actividades-en-Overleaf-238598df262b802098d2d9957542f8d4?source=copy_link](https://erickordazr.notion.site/Gu-a-para-usar-la-plantilla-de-actividades-en-Overleaf-238598df262b802098d2d9957542f8d4?source=copy_link)

<aside>  
⚠️

**Nota Importante:**

- Todas las fuentes deben citarse correctamente para evitar problemas de plagio.
- El incumplimiento del formato LaTeX institucional será penalizado.
- El documento entregado debe ser un PDF único. No se aceptan archivos adicionales de ningún tipo.
- Solo el representante del equipo realiza la entrega en Teams. Los demás integrantes no deben entregar.
- Las conclusiones son personales: cada integrante del equipo redacta su propia reflexión dentro del documento.
- Las capturas de pantalla deben mostrar claramente la terminal y las figuras generadas por el script en cada una de las cuatro variaciones solicitadas.
- El reporte debe elaborarse a partir de la plantilla de Overleaf indicada en Guías y Lineamientos; no se aceptan reportes generados fuera de dicha plantilla.  
    </aside>
