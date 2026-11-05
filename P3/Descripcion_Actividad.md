# Práctica 3. Integración de un sistema multiagente aplicado.

**Link a Notion:** https://erickordazr.notion.site/Pr-ctica-3-Integraci-n-de-un-sistema-multiagente-aplicado-825598df262b82fa86dd818153aabe59

<aside>  
❗

**Valor: 20 puntos** (se califica sobre 100).

</aside>

## Competencia Específica

> El estudiante será capaz de **integrar de forma funcional**, mediante una práctica de programación, los componentes de agente y de coordinación programados en las Prácticas 1 y 2 dentro de un sistema multiagente aplicado a un problema real simulado, con el fin de **justificar la pertinencia** de dicho sistema para el problema elegido y **documentar su comportamiento** bajo condiciones prácticas de robustez.

## Descripción de la Actividad

Esta práctica no introduce una arquitectura de agente ni un mecanismo de coordinación nuevos: integra los que ya se programaron en las Prácticas 1 y 2 dentro de un sistema aplicado a un problema concreto. El ejemplo que trae el script base es un sistema de búsqueda y rescate: un equipo de agentes explora una zona de desastre con escombros, localizando víctimas atrapadas, usando el mismo ciclo percepción-decisión-acción de la Práctica 1 y los mismos dos mecanismos de coordinación de la Práctica 2.

Lo que esta práctica agrega es una condición que las dos anteriores no contemplaban: un sistema real no opera en un entorno perfecto. El equipo recibe un script base (`practica3_sistema_busqueda_rescate.py`) con tres condiciones de robustez, independientes entre sí y activables por separado: un agente puede fallar y quedar fuera de servicio, un mensaje puede perderse por completo (no solo retrasarse), y el entorno puede cambiar mientras el sistema opera.

[practica3_sistema_busqueda_rescate.py](attachment:97b1f7d9-27e5-4463-8eed-7d7b898026c0:practica3_sistema_busqueda_rescate.py)

Sistemas a integrar y verificar durante la sesión:

1. Reutilización del ciclo percepción-decisión-acción de la Práctica 1, aplicado a la localización de víctimas en lugar de muestras.
2. Reutilización de los dos mecanismos de coordinación de la Práctica 2 (pizarrón compartido y mensajería directa), aplicados al mismo sistema.
3. Tres condiciones de robustez, cada una como parámetro independiente: falla de agente, pérdida de mensajes y entorno dinámico.
4. Elección y justificación de UN mecanismo de coordinación para el sistema final, con base en evidencia propia obtenida bajo condiciones de robustez.

## Contenido Teórico de Referencia

Se presenta a continuación un resumen mínimo, suficiente para comprender el código de la práctica.

**Integración de un sistema multiagente aplicado.** Consiste en componer módulos ya validados por separado (una arquitectura de agente, un mecanismo de coordinación) dentro de un sistema orientado a un problema concreto, sin rediseñar el funcionamiento interno de dichos módulos. La integración se evalúa por si el sistema compuesto sigue funcionando correctamente como un todo, no por la novedad de sus partes.

**Definición — Tolerancia a fallas.** Capacidad de un sistema multiagente de continuar operando, con un desempeño reducido pero predecible, cuando uno o más de sus agentes dejan de funcionar durante la ejecución.

**Definición — Pérdida de mensajes.** En un sistema de mensajería real, un mensaje enviado no siempre llega a su destinatario, independientemente del tiempo que se espere. Es una condición distinta del retraso: un mensaje retrasado llega tarde; un mensaje perdido no llega nunca.

**Definición — Entorno dinámico.** Entorno cuyo estado puede cambiar por causas ajenas a las acciones de los agentes mientras el sistema está en operación, de modo que el conocimiento que el equipo ya había adquirido puede volverse obsoleto sin previo aviso.

|Condición de robustez|Qué simula|A qué mecanismo afecta más directamente|
|---|---|---|
|Falla de agente|Pérdida de un recurso del equipo durante la operación|A ambos por igual: reduce la capacidad total del equipo|
|Pérdida de mensajes|Comunicación poco confiable entre agentes distribuidos|A la mensajería directa, que depende por completo de que sus avisos lleguen|
|Entorno dinámico|Un entorno real que cambia por causas externas al equipo|A ambos, aunque de forma distinta según qué tan rápido cada uno detecta el cambio|

## Explicación del Código Base

El script `practica3_sistema_busqueda_rescate.py` se entrega extensamente comentado. A continuación se explica la función de cada componente nuevo; los componentes heredados de las Prácticas 1 y 2 (el ciclo de decisión, ambos mecanismos de coordinación) no se repiten aquí.

**Sección de parámetros (`ParametrosPractica`).** Adiciona tres campos independientes de robustez: `prob_falla_agente`, `prob_perdida_mensaje` y `prob_obstaculo_dinamico`, todos en 0.0 por defecto. Con los tres en 0.0, la práctica se comporta exactamente igual que la Práctica 2.

**Falla de agente (`_procesar_falla_de_agente`).** En cada paso, antes de que un agente decida, se evalúa la probabilidad de falla. Si ocurre, el agente se congela de inmediato: su energía consumida se fija al máximo, de modo que el resto de la simulación lo trata como si ya hubiera agotado su presupuesto, sin necesidad de una bandera adicional en cada verificación.

**Pérdida de mensajes (`_enviar_o_perder`).** Cada mensaje que el sistema intenta enviar se somete a esta probabilidad antes de ingresar a la cola de pendientes. Un mensaje perdido nunca se agrega a dicha cola ni al historial de entregables: se comporta exactamente como si jamás se hubiera enviado, desde el punto de vista de quien debía recibirlo.

**Entorno dinámico (`agregar_escombro_dinamico`).** En cada paso, con la probabilidad configurada, una celda libre que ningún agente esté ocupando en ese instante se convierte en escombro nuevo, representando que la zona de desastre sigue siendo inestable mientras el equipo opera en ella.

**Generador de aleatoriedad independiente para la robustez.** Las tres condiciones se deciden con un generador de números aleatorios separado del que usan los agentes para explorar. Esto permite activar o desactivar la robustez sin alterar la secuencia de decisiones que toma cada agente, de modo que la única diferencia entre una ejecución y otra sea, exactamente, la robustez que se está probando.

## Contenido del Entregable

1. **Portada** — nombre de la actividad, integrantes, matrículas, número de equipo, nombre del asesor y fecha. Plantilla LaTeX institucional.
2. **Objetivo** — qué se busca demostrar: que el sistema integrado (arquitectura de agente + mecanismo de coordinación de las Prácticas 1 y 2) resuelve el problema de búsqueda y rescate de forma funcional, y que uno de los dos mecanismos de coordinación es más adecuado que el otro bajo condiciones realistas de robustez.
3. **Marco Teórico** — integración de sistemas multiagente aplicados; definición de las tres condiciones de robustez (falla de agente, pérdida de mensajes, entorno dinámico). Mínimo una cita textual por concepto.
4. **Materiales y Herramientas** — Python 3.10 o superior; bibliotecas `matplotlib` y `pillow`; script base `practica3_sistema_busqueda_rescate.py`; editor de texto o entorno de desarrollo integrado (IDE).
5. **Procedimiento** — descripción paso a paso de la ejecución realizada, incluyendo capturas de pantalla de la terminal, la figura y la animación, en cada una de las siguientes variaciones obligatorias de `ParametrosPractica`:
    - Activar únicamente `prob_falla_agente` (valor mayor a 0) y ejecutar la comparación entre mecanismos.
    - Activar únicamente `prob_perdida_mensaje` (valor mayor a 0) y ejecutar la comparación.
    - Activar únicamente `prob_obstaculo_dinamico` (valor mayor a 0) y ejecutar la comparación.
    - Activar las tres condiciones combinadas y ejecutar la comparación final.
6. **Resultados y Análisis** — para cada una de las cuatro variaciones: la tabla comparativa generada por el script, la figura correspondiente (`comparacion_practica3.png`) y un análisis escrito que explique el efecto observado de cada condición de robustez sobre cada mecanismo. A partir de esta evidencia, el equipo debe **elegir y justificar UN mecanismo de coordinación** para su sistema final, y **justificar la pertinencia** de este sistema de agentes para el problema que el equipo eligió para su PIA (aun cuando el ejemplo entregado sea de búsqueda y rescate, la justificación debe explicar la correspondencia entre los elementos del código —agentes, víctimas, escombros— y los del problema propio del equipo).
7. **Conclusiones** — cada integrante del equipo redacta su propia reflexión individual sobre la evidencia obtenida y su relación con los contenidos de la sesión introductoria del curso.
8. **Referencias** — mínimo 3 fuentes. Formato APA.
9. **Anexos** — código fuente completo `practica3_sistema_busqueda_rescate.py`, incluido dentro del PDF mediante el entorno `lstlisting`, o enlace a repositorio Git del equipo.

## Formato del Documento

El documento debe seguir **exclusivamente** la **plantilla LaTeX institucional**.

El PDF es el único archivo entregable. No se aceptan archivos adicionales de ningún tipo.

## Criterios de Evaluación

|Criterio|Porcentaje|Descripción|
|---|---|---|
|Integración funcional de los componentes de fases previas|30%|El sistema integra correctamente el ciclo de decisión de la Práctica 1 y los mecanismos de coordinación de la Práctica 2, y opera bajo las condiciones de robustez solicitadas.|
|Justificación de la pertinencia del sistema|25%|El equipo explica, con evidencia propia, por qué este sistema multiagente y el mecanismo de coordinación elegido son adecuados para el problema seleccionado en su PIA.|
|Resultados y Análisis|20%|Las cuatro variaciones obligatorias de robustez están documentadas con tabla, figura e interpretación propia.|
|Marco Teórico|10%|Definiciones correctas de integración de sistemas y de las tres condiciones de robustez, con cita textual.|
|Conclusiones|10%|Reflexión personal de cada integrante, evidenciando relación explícita con los contenidos del curso.|
|Formato y Referencias|5%|Documento generado exclusivamente desde la plantilla LaTeX institucional en Overleaf, con mínimo 3 fuentes citadas en formato APA.|

## Entrega de la Actividad

- **Modalidad:** En equipo de 3 a 4 integrantes.
- **Plataforma:** Microsoft Teams.
- **Formato de entrega:** Un solo archivo PDF generado desde LaTeX. Todo el material complementario (código, capturas, datos) debe incluirse dentro del PDF como anexos o mediante enlaces referenciados en el documento. No se aceptan archivos .zip, .rar ni adjuntos adicionales.
- **Responsable de entrega:** Un solo integrante por equipo (el representante) realiza la entrega. Los demás integrantes no deben entregar.

**Nombrado del archivo:**

```
LSMA-L-V3-01-AF6
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
- Las capturas de pantalla deben mostrar claramente los eventos de robustez (fallas de agente, escombros dinámicos, mensajes perdidos) además de los resultados normales de cada variación.
- El reporte debe elaborarse a partir de la plantilla de Overleaf indicada en Guías y Lineamientos; no se aceptan reportes generados fuera de dicha plantilla.  
    </aside>
