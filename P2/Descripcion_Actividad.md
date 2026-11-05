# Práctica 2. Programación de un protocolo de comunicación y coordinación entre agentes para una tarea conjunta.

**Link a Notion:** https://erickordazr.notion.site/Pr-ctica-2-Programaci-n-de-un-protocolo-de-comunicaci-n-y-coordinaci-n-entre-agentes-para-una-tarea-f10598df262b83948d38814ee633c45a

<aside>  
❗

**Valor: 25 puntos** (se califica sobre 100).

</aside>

## Competencia Específica

> El estudiante será capaz de **implementar correctamente** el protocolo de comunicación y el mecanismo de coordinación entre agentes, mediante una práctica de programación en Python sobre un equipo de agentes simulados, con el fin de **documentar y justificar**, con evidencia experimental propia, cómo el mecanismo de intercambio de información utilizado determina la eficiencia de la coordinación del equipo.

## Descripción de la Actividad

En esta práctica, un equipo de agentes (su número es un parámetro configurable) explora de manera simultánea el mismo entorno de la Práctica 1: una cuadrícula con obstáculos y muestras ocultas, bajo observabilidad parcial. Todos los agentes parten del mismo punto de origen, lo cual es deliberado: sin ningún mecanismo de coordinación, tienden a agruparse y a explorar las mismas zonas, duplicando esfuerzo.

El equipo recibe un script base (`practica2_coordinacion_agentes.py`) que ya implementa el "cerebro" individual de cada agente (idéntico en ambos casos) y dos mecanismos distintos para que se coordinen entre sí. La actividad consiste en ejecutar, modificar sistemáticamente y analizar el comportamiento del sistema bajo ambos mecanismos, documentando con evidencia propia cómo cada uno resuelve —o no— el problema de repartirse el trabajo.

[practica2_coordinacion_robots.py](attachment:a8f6ad51-c1e8-47f5-a021-f7e5cd170ec7:practica2_coordinacion_robots.py)

Sistemas a implementar y verificar durante la sesión:

1. Pizarrón compartido (blackboard): una única estructura de datos, visible de manera instantánea para todos los agentes.
2. Mensajería directa (protocolo simplificado inspirado en FIPA-ACL): sin estructura compartida; cada agente solo conoce lo que percibió y lo que otros le comunicaron explícitamente, con un retraso de entrega configurable.
3. Comparación controlada de ambos mecanismos sobre el mismo entorno, variando el número de agentes y el retraso de los mensajes.

## Contenido Teórico de Referencia

Se presenta a continuación un resumen mínimo, suficiente para comprender el código de la práctica.

**El problema de la coordinación.** Cuando varios agentes autónomos comparten un mismo entorno y una misma meta colectiva, la falta de coordinación produce redundancia: dos o más agentes realizan el mismo trabajo sin saberlo. Un mecanismo de coordinación no cambia lo que cada agente es capaz de hacer individualmente; cambia qué tanto sabe cada agente sobre lo que los demás ya hicieron.

**Definición — Pizarrón compartido (blackboard).** Arquitectura de coordinación en la que todos los agentes leen y escriben sobre una única estructura de datos común, visible de manera instantánea para todo el equipo. No requiere el envío explícito de mensajes entre agentes.

**Definición — Mensajería directa.** Arquitectura de coordinación en la que no existe ninguna estructura compartida; los agentes intercambian mensajes explícitos entre sí. La entrega de un mensaje no es instantánea: transcurre un tiempo entre el envío y la recepción, por lo que el conocimiento de cada agente sobre el resto del equipo siempre puede estar, en algún grado, desactualizado.

**Estructura simplificada de un mensaje (inspirada en FIPA-ACL).** Todo mensaje del protocolo tiene un emisor, un destinatario (o ninguno, cuando es un aviso general), un performativo que indica la intención comunicativa, y un contenido. Se implementan dos performativos: `informar` (un agente avisa al resto de un hecho) y `proponer` (se usa para resolver una disputa, cuando el agente que gana un desempate le propone al otro ceder una reclamación previa).

|Aspecto|Pizarrón compartido|Mensajería directa|
|---|---|---|
|Visibilidad de la información|Instantánea para todo el equipo|Retrasada; depende de cuándo se entrega cada mensaje|
|¿Puede haber disputas?|No, por construcción|Sí: dos agentes pueden reclamar el mismo recurso sin saberlo|
|Requiere estructura centralizada|Sí|No|
|Realismo frente a un sistema distribuido real|Bajo (no siempre existe un pizarrón central posible)|Alto|

## Explicación del Código Base

El script `practica2_coordinacion_agentes.py` se entrega extensamente comentado. A continuación se explica la función de cada componente, no su sintaxis línea por línea.

**Sección de parámetros (`ParametrosPractica`).** Además de los parámetros ya conocidos de la Práctica 1 (tamaño del entorno, obstáculos, muestras, energía), agrega `num_agentes` (tamaño del equipo) y `retraso_mensaje` (cuántos pasos tarda un mensaje en llegar).

**La regla de decisión común (`decidir_accion_agente`).** Es una única función, compartida por ambos mecanismos: si el agente percibe una muestra libre, va por ella; si no, prefiere una celda que el equipo (según lo que él sabe) no haya explorado; si no hay ninguna, elige al azar entre las conocidas. Esta función es idéntica en ambos casos — la diferencia entre mecanismos nunca está en qué tan "inteligente" es cada agente, sino en qué tan actualizada está la información que recibe.

**Mecanismo de pizarrón (`ejecutar_episodio_pizarron`).** Procesa a los agentes uno por uno, en un orden fijo, dentro de cada paso, y actualiza el pizarrón compartido de inmediato después de que cada uno actúa —antes de que decida el siguiente—. Esa actualización instantánea y secuencial es, por construcción, la razón por la que este mecanismo nunca produce disputas.

**Mecanismo de mensajería (`ejecutar_episodio_mensajeria`).** Separa cada paso en dos fases: primero todos los agentes perciben y deciden con base en el entorno tal como estaba al inicio del paso (sin que nadie se haya movido todavía); solo después se ejecutan los movimientos, uno por uno. Esta separación es necesaria para que dos agentes puedan, genuinamente, reclamar el mismo recurso en el mismo paso sin haberse enterado todavía el uno del otro.

**Resolución de disputas.** Cuando eso ocurre, se aplica una regla de desempate determinista (conserva la reclamación el agente con el identificador numérico más bajo) y se envía un mensaje `proponer` al perdedor, con el mismo retraso que cualquier otro mensaje.

**Métrica de redundancia (`_empaquetar_resultados`).** Se calcula comparando el total de pasos recorridos por todo el equipo (sumando a todos los agentes, con repeticiones) contra el número de celdas realmente distintas que se llegaron a explorar. La diferencia es, exactamente, el número de veces que una celda fue visitada de más.

**Visualización explícita de la comunicación.** El script también registra, para el mecanismo de mensajería, un historial completo de mensajes y cuántos quedan "en tránsito" en cada paso. La figura y la animación marcan con un anillo rojo el instante y la celda exacta de cada disputa, y la animación muestra en vivo un contador de mensajes en tránsito, para que el costo de la comunicación no instantánea sea visible y no solo un concepto abstracto.

## Contenido del Entregable

1. **Portada** — nombre de la actividad, integrantes, matrículas, número de equipo, nombre del asesor y fecha. Plantilla LaTeX institucional.
2. **Objetivo** — qué se busca demostrar: que el mecanismo de pizarrón compartido logra menor redundancia que la mensajería directa, a costa de requerir una estructura centralizada que no siempre es viable en un sistema distribuido real.
3. **Marco Teórico** — el problema de la coordinación entre agentes; definición de pizarrón compartido y de mensajería directa; estructura simplificada de un mensaje inspirada en FIPA-ACL. Mínimo una cita textual por concepto.
4. **Materiales y Herramientas** — Python 3.10 o superior; bibliotecas `matplotlib` y `pillow`; script base `practica2_coordinacion_agentes.py`; editor de texto o entorno de desarrollo integrado (IDE).
5. **Procedimiento** — descripción paso a paso de la ejecución realizada, incluyendo capturas de pantalla de la terminal, la figura y la animación, en cada una de las siguientes variaciones obligatorias de `ParametrosPractica`:
    - Variación del número de agentes (mínimo tres valores distintos, por ejemplo 1, 3 y 6).
    - Variación del retraso de mensaje (por ejemplo 0, 1 y 5 pasos).
    - Variación de la densidad de obstáculos (`densidad_obstaculos = 0.30`).
    - Variación del peso de redundancia (`peso_redundancia = 1.0`).
6. **Resultados y Análisis** — para cada una de las cuatro variaciones: la tabla comparativa generada por el script, la figura correspondiente (`comparacion_practica2.png`), y un análisis escrito que explique el resultado en términos de qué tan actualizada estaba la información de cada agente — no solo en términos numéricos. Se debe reportar explícitamente cuántas disputas ocurrieron en cada variación y por qué.
7. **Conclusiones** — cada integrante del equipo redacta su propia reflexión individual sobre la evidencia obtenida y su relación con los contenidos de la sesión introductoria del curso.
8. **Referencias** — mínimo 3 fuentes. Formato APA.
9. **Anexos** — código fuente completo `practica2_coordinacion_agentes.py`, incluido dentro del PDF mediante el entorno `lstlisting`, o enlace a repositorio Git del equipo.

## Formato del Documento

El documento debe seguir **exclusivamente** la **plantilla LaTeX institucional**.

El PDF es el único archivo entregable. No se aceptan archivos adicionales de ningún tipo.

## Criterios de Evaluación

|Criterio|Porcentaje|Descripción|
|---|---|---|
|Implementación del protocolo de comunicación|25%|El mecanismo de mensajería (mensajes, retraso de entrega, resolución de disputas) funciona correctamente y el equipo demuestra comprender su funcionamiento interno.|
|Implementación del mecanismo de coordinación|25%|El pizarrón compartido funciona correctamente y el equipo explica por qué nunca produce disputas.|
|Resultados y Análisis|20%|Las cuatro variaciones obligatorias están documentadas con tabla, figura e interpretación propia, incluyendo el número de disputas de cada una.|
|Marco Teórico|15%|Definiciones correctas de ambos mecanismos y de la estructura de un mensaje, con cita textual.|
|Conclusiones|10%|Reflexión personal de cada integrante, evidenciando relación explícita con los contenidos del curso.|
|Formato y Referencias|5%|Documento generado exclusivamente desde la plantilla LaTeX institucional en Overleaf, con mínimo 3 fuentes citadas en formato APA.|

## Entrega de la Actividad

- **Modalidad:** En equipo de 3 a 4 integrantes.
- **Plataforma:** Microsoft Teams.
- **Formato de entrega:** Un solo archivo PDF generado desde LaTeX. Todo el material complementario (código, capturas, datos) debe incluirse dentro del PDF como anexos o mediante enlaces referenciados en el documento. No se aceptan archivos .zip, .rar ni adjuntos adicionales.
- **Responsable de entrega:** Un solo integrante por equipo (el representante) realiza la entrega. Los demás integrantes no deben entregar.

**Nombrado del archivo:**

```
LSMA-L-V3-01-AF5
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
- Las capturas de pantalla deben mostrar claramente la terminal, la figura y la animación generadas por el script, incluyendo los momentos de disputa cuando existan.
- El reporte debe elaborarse a partir de la plantilla de Overleaf indicada en Guías y Lineamientos; no se aceptan reportes generados fuera de dicha plantilla.  
    </aside>
