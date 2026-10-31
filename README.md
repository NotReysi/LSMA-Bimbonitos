# Laboratorio de Sistemas Multiagente
**Profesor:** Dr. Erick de Jesús Ordaz Rivas




### Equipo 3: Bimbonitos
| Integrante | Matrícula |
|--------|-----------|
| Orlando Alvarado Vargas | 2226968 |
| Mariana Flores Rosales | 2143017 |
| Kevin Ramsés Ríos Hernández | 2157213 |
| Kenner Shahid López Ramírez | 2142291 |
## Prácticas

| Práctica | Descripción | Estado |
|----------|-------------|--------|
| [Práctica 1](https://erickordazr.notion.site/Pr-ctica-1-Programaci-n-de-un-agente-inteligente-reactivo-o-basado-en-modelos-objetivos-en-un-ent-d53598df262b82d2b43801b7a5c7fa86) | Agente inteligente reactivo y basado en modelos | ✅ Terminada |
| [Práctica 2](https://erickordazr.notion.site/Pr-ctica-2-Programaci-n-de-un-protocolo-de-comunicaci-n-y-coordinaci-n-entre-agentes-para-una-tarea-f10598df262b83948d38814ee633c45a) | Protocolo de comunicación y coordinación entre agentes | ⏳ Pendiente |
| [Práctica 3](https://erickordazr.notion.site/Pr-ctica-3-Integraci-n-de-un-sistema-multiagente-aplicado-825598df262b82fa86dd818153aabe59?source=copy_link) | Integración de un sistema multiagente aplicado | ⏳ Pendiente |
| [PIA](https://erickordazr.notion.site/Producto-Integrador-de-Aprendizaje-131598df262b8225a96881531da70439?source=copy_link) | Producto Integrador de Aprendizaje | ⏳ Pendiente |

## Práctica 1: Agentes exploradores

Simulación de un robot que explora una cuadrícula con obstáculos y muestras ocultas, percibiendo solo las cuatro celdas adyacentes. Se comparan dos agentes sobre el mismo entorno:

- **Reactivo:** decide solo con lo que percibe en el momento.
- **Basado en modelos:** guarda un mapa de lo explorado y lo usa para buscar zonas nuevas.

El programa imprime una tabla comparativa y una bitácora en la terminal. También genera una imagen (`comparacion_practica1.png`) y una animación (`simulacion_practica1.gif`).

### Contenido de `P1/`

- `Agentes_Exploradores.py`: código de la simulación.
- Evidencias de ejecución: capturas con variaciones de densidad, energía, peso y semilla.
- `LSMA_L_V3_03_AF4.pdf`: reporte.

### Ejecución

```bash
pip install numpy matplotlib pillow
python P1/Agentes_Exploradores.py
```

Los parámetros se modifican en la clase `ParametrosPractica`, dentro del script.
