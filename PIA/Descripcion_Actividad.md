# Producto Integrador de Aprendizaje

**Link a Notion:** https://erickordazr.notion.site/Producto-Integrador-de-Aprendizaje-131598df262b8225a96881531da70439

<aside>  
❗

**Valor: 30 puntos** (se califica sobre 100).

</aside>

## Competencia Específica

> El estudiante será capaz de **integrar y documentar**, en un portafolio técnico, las arquitecturas de agente, los mecanismos de coordinación y las consideraciones de robustez programados en las Prácticas 1, 2 y 3, con el fin de **justificar las decisiones de diseño adoptadas** y **aplicarlas al problema seleccionado para el Producto Integrador de Aprendizaje de la materia teórica de Sistemas Multiagente**.

## Descripción de la Actividad

El Producto Integrador de Aprendizaje de este laboratorio es un **portafolio de modelos y algoritmos basados en agentes inteligentes**, conforme a lo establecido en el programa analítico. No es un cuarto sistema que deba programarse desde cero: es la consolidación documentada del trabajo ya realizado en las Prácticas 1, 2 y 3, reinterpretado sobre el mismo problema que el equipo eligió para su Producto Integrador de Aprendizaje en la materia teórica de Sistemas Multiagente.

Esta condición es obligatoria: el sistema que se documente en este portafolio debe corresponder al mismo tema del PIA de la materia de ordinario, no a un problema distinto ni al ejemplo genérico entregado en los scripts de las prácticas (exploración en cuadrícula, búsqueda y rescate). El equipo debe explicar, con sus propias palabras y evidencia propia, cómo cada componente de las prácticas, arquitectura de agente, mecanismo de coordinación, condiciones de robustez, se traslada a su problema particular.

El núcleo de la evaluación no es la cantidad de código producido, sino la **calidad de la justificación**: por qué el equipo eligió una arquitectura de agente y no la otra, por qué eligió un mecanismo de coordinación y no el otro, y qué evidencia de las prácticas anteriores respalda esa elección. Una justificación que se limite a describir lo que el código hace, sin argumentar por qué esa fue la decisión correcta para el problema del equipo, no cumple con el propósito de esta actividad.

## Contenido Teórico de Referencia

Este portafolio no introduce conceptos nuevos: sintetiza los de las tres fases previas.

|Fase|Concepto central|Práctica relacionada|
|---|---|---|
|Fase 1 — Fundamentos de agentes|Ciclo percepción-decisión-acción; arquitectura reactiva frente a basada en modelos|Práctica 1|
|Fase 2 — Coordinación y comunicación|Mecanismos de coordinación entre agentes: pizarrón compartido frente a mensajería directa|Práctica 2|
|Fase 3 — Sistemas multiagente aplicados|Integración de componentes y condiciones prácticas de robustez|Práctica 3|

**Justificación de decisiones de diseño.** En ingeniería de sistemas multiagente, la elección de una arquitectura o de un mecanismo de coordinación no tiene una respuesta universalmente correcta: depende de las restricciones del problema (¿es viable una estructura centralizada?, ¿qué tan crítico es el retraso de comunicación?, ¿qué tan probable es la falla de un agente?). Justificar una decisión de diseño consiste en argumentar, con evidencia obtenida experimentalmente, por qué la opción elegida es la más adecuada para las restricciones del problema propio, no en enumerar las opciones disponibles.

## Contenido del Entregable

1. **Portada** — nombre de la actividad, título del proyecto (el mismo del PIA de la materia teórica), integrantes, matrículas, número de equipo, nombre del asesor y fecha. Plantilla LaTeX institucional.
2. **Introducción** — contexto del problema elegido para el PIA de la materia teórica, objetivo general del portafolio, y por qué un enfoque multiagente es pertinente para dicho problema.
3. **Descripción General del Sistema Integrado** — función principal del sistema aplicado al problema propio del equipo; diagrama del ciclo percepción-decisión-acción adaptado a dicho problema; entradas, salidas y comportamiento esperado.
4. **Marco Teórico** — síntesis de los conceptos de las tres fases (ver Contenido Teórico de Referencia), con al menos una cita textual por concepto.
5. **Justificación de las Decisiones de Diseño** — sección central del portafolio. Debe responder explícitamente: ¿qué arquitectura de agente se eligió (reactiva o basada en modelos) y por qué, con base en la evidencia de la Práctica 1? ¿Qué mecanismo de coordinación se eligió (pizarrón compartido o mensajería directa) y por qué, con base en la evidencia de la Práctica 2? ¿Qué condiciones de robustez de la Práctica 3 son relevantes para el problema propio, y cómo las maneja el sistema?
6. **Resultados Consolidados** — resumen de los hallazgos más relevantes obtenidos a lo largo de las tres prácticas, reinterpretados en función del problema propio del equipo (no se espera repetir los experimentos completos, sino consolidar la evidencia ya generada).
7. **Conclusiones** — cada integrante del equipo redacta su propia reflexión individual sobre el proceso de integración y su relación con los contenidos del curso.
8. **Referencias** — mínimo 10 fuentes. Formato APA.
9. **Anexos** — código fuente de las Prácticas 1, 2 y 3 adaptado al problema propio del equipo, incluido dentro del PDF mediante el entorno `lstlisting`, o enlace a repositorio Git.

## Formato del Documento

El documento debe seguir **exclusivamente** la **plantilla LaTeX institucional**.

El PDF es el único archivo entregable. No se aceptan archivos adicionales de ningún tipo.

## Criterios de Evaluación

|Criterio|Porcentaje|Descripción|
|---|---|---|
|Justificación de la arquitectura de agente y el mecanismo de coordinación elegidos|25%|El equipo argumenta, con evidencia propia de las Prácticas 1 y 2, por qué las opciones elegidas son las más adecuadas para su problema.|
|Integración funcional de las tres fases|20%|El portafolio consolida de forma coherente los componentes de agente, coordinación y robustez en un solo sistema aplicado.|
|Vínculo explícito con el PIA de la materia teórica|15%|El sistema documentado corresponde al mismo problema elegido por el equipo en la materia teórica, no a un ejemplo genérico.|
|Resultados consolidados|15%|Los hallazgos de las tres prácticas se resumen y se reinterpretan correctamente en función del problema propio.|
|Marco Teórico|10%|Síntesis correcta de los conceptos de las tres fases, con cita textual.|
|Conclusiones|10%|Reflexión personal de cada integrante, evidenciando relación explícita con los contenidos del curso.|
|Formato y Referencias|5%|Documento generado exclusivamente desde la plantilla LaTeX institucional en Overleaf, con mínimo 10 fuentes citadas en formato APA.|

## Entrega de la Actividad

- **Modalidad:** En equipo de 3 a 4 integrantes (el mismo equipo y el mismo tema del PIA de la materia teórica).
- **Plataforma:** Microsoft Teams.
- **Formato de entrega:** Un solo archivo PDF generado desde LaTeX. Todo el material complementario (código, capturas, datos) debe incluirse dentro del PDF como anexos o mediante enlaces referenciados en el documento. No se aceptan archivos .zip, .rar ni adjuntos adicionales.
- **Responsable de entrega:** Un solo integrante por equipo (el representante) realiza la entrega. Los demás integrantes no deben entregar.

**Nombrado del archivo:**

```
LSMA-L-V3-01-AF3
```

## Guías y Lineamientos

- **Indicaciones generales para la entrega de actividades:** [](https://app.notion.com/Indicaciones-para-la-entrega-de-tareas-239598df262b80a5b34cebadea9a25ae?pvs=21)[https://erickordazr.notion.site/Indicaciones-para-la-entrega-de-tareas-239598df262b80a5b34cebadea9a25ae](https://erickordazr.notion.site/Indicaciones-para-la-entrega-de-tareas-239598df262b80a5b34cebadea9a25ae)
- **Guía para el formato del documento en LaTeX:** [](https://app.notion.com/Gu-a-para-usar-la-plantilla-de-actividades-en-Overleaf-238598df262b802098d2d9957542f8d4?pvs=21)[https://erickordazr.notion.site/Gu-a-para-usar-la-plantilla-de-actividades-en-Overleaf-238598df262b802098d2d9957542f8d4?source=copy_link](https://erickordazr.notion.site/Gu-a-para-usar-la-plantilla-de-actividades-en-Overleaf-238598df262b802098d2d9957542f8d4?source=copy_link)

<aside>  
⚠️

**Nota Importante:**

- El sistema documentado debe corresponder exactamente al mismo problema elegido por el equipo para el PIA de la materia ordinaria; un portafolio construido sobre un problema distinto o sobre el ejemplo genérico de las prácticas no cumple con esta actividad.
- La justificación de las decisiones de diseño debe apoyarse en evidencia propia generada durante las Prácticas 1 y 2 (tablas, figuras, cifras), no en afirmaciones sin respaldo.
- Todas las fuentes deben citarse correctamente para evitar problemas de plagio.
- El incumplimiento del formato LaTeX institucional será penalizado.
- El documento entregado debe ser un PDF único. No se aceptan archivos adicionales de ningún tipo.
- Solo el representante del equipo realiza la entrega en Teams. Los demás integrantes no deben entregar.
- Las conclusiones son personales: cada integrante del equipo redacta su propia reflexión dentro del documento.
- El reporte debe elaborarse a partir de la plantilla de Overleaf indicada en Guías y Lineamientos; no se aceptan reportes generados fuera de dicha plantilla.  
    </aside>
