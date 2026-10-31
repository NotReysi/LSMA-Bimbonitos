"""
================================================================================
Laboratorio de Sistemas Multiagente
Práctica 1 - Fase 1: Fundamentos de agentes
Programación de un agente individual reactivo y basado en modelos
================================================================================

GUÍA DE LECTURA

Este archivo contiene un programa desarrollado en el lenguaje Python. Para
comprender su funcionamiento no es indispensable contar con experiencia
previa en programación: basta con conocer los siguientes cuatro conceptos,
que se emplean de manera recurrente a lo largo del código. Cada bloque
relevante del archivo incluye un comentario (líneas que inician con el
símbolo #) que explica su propósito y su relación con los conceptos vistos
en clase.

Clase: una plantilla que define las características y el comportamiento de
un tipo de objeto. Por ejemplo, la clase Entorno define cómo se construye
un mapa de simulación; la clase AgenteReactivo define cómo se construye un
agente que decide de forma reactiva. Cada vez que el programa "crea" un
objeto a partir de una clase, produce una instancia concreta de dicha
plantilla.

Función (o método, cuando pertenece a una clase): un bloque de
instrucciones identificado con un nombre, que recibe datos de entrada,
realiza un proceso con ellos y devuelve un resultado.

Bucle (for / while): una instrucción que repite un bloque de código varias
veces. La instrucción "for" repite el bloque una vez por cada elemento de
una colección de datos; la instrucción "while" repite el bloque mientras
se cumpla una condición determinada.

Condicional (if / elif / else): una instrucción que ejecuta un bloque de
código únicamente si se cumple una condición determinada. Es el mecanismo
mediante el cual el programa toma decisiones.

PROPÓSITO DEL PROGRAMA

Este programa simula un agente robótico que se desplaza en una
cuadrícula bidimensional con obstáculos y muestras (puntos de interés)
ocultas. El agente cuenta con observabilidad parcial del entorno: en cada
instante únicamente percibe las cuatro celdas adyacentes a su posición
(arriba, abajo, izquierda, derecha), no el mapa completo.

El programa implementa y compara dos arquitecturas distintas para el
programa de agente, en el sentido definido por Russell y Norvig (2020):

    1. Agente de reflejo simple (reactivo): selecciona su acción
       únicamente a partir del percepto actual, sin conservar memoria de
       los estados previos del entorno.

    2. Agente basado en modelos: mantiene una representación interna
       (mapa) del entorno explorado hasta el momento, y la utiliza para
       orientar su búsqueda hacia el territorio aún no explorado.

Ambas arquitecturas se ejecutan sobre un entorno idéntico (misma semilla
aleatoria, mismo punto de partida) para permitir una comparación
controlada de su desempeño, conforme a la especificación PEAS revisada en
la sesión introductoria del curso.

ARCHIVOS QUE GENERA LA EJECUCIÓN

    1. Un reporte en la terminal con una tabla comparativa de desempeño y
       una bitácora que documenta las decisiones más relevantes de cada
       agente.
    2. Un archivo de imagen (comparacion_practica1.png) con el mapa
       completo, la trayectoria seguida por cada agente y las muestras
       recolectadas.
    3. Un archivo de animación (simulacion_practica1.gif) que reproduce el
       recorrido de ambos agentes de forma secuencial, paso a paso.

Ambos archivos se guardan automáticamente en la misma carpeta donde se
encuentra este script, sin importar desde qué ubicación se ejecute.

FORMA DE EJECUCIÓN

    python practica1_agente_explorador.py
"""

from __future__ import annotations
# La línea anterior activa una funcionalidad del lenguaje que permite
# escribir anotaciones de tipo (por ejemplo, "tuple[int, int]") de
# forma compatible con distintas versiones de Python. No afecta la
# lógica del programa: únicamente concierne a la documentación de
# tipos de datos que aparece en las firmas de las funciones.

import os                                # para ubicar la carpeta de este script
import random                            # para generar números y elecciones aleatorias
from collections import Counter, deque   # utilidades para conteo y manejo de colas
from dataclasses import dataclass, field  # para definir clases que almacenan datos
from enum import Enum                    # para definir conjuntos cerrados de valores válidos
from typing import Optional              # para documentar valores que pueden estar ausentes


def _ruta_junto_al_script(nombre_archivo: str) -> str:
    """
    Devuelve la ruta completa (absoluta) de un archivo de salida,
    ubicándolo siempre en la misma carpeta donde se encuentra este
    script, independientemente de la carpeta desde la que se ejecute.
    """
    carpeta_del_script = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(carpeta_del_script, nombre_archivo)


# =============================================================================
# SECCIÓN 0. PARÁMETROS CONFIGURABLES POR EL ESTUDIANTE
#
# Los valores definidos en esta clase son los únicos que se requiere
# modificar para experimentar con la práctica. No es necesario editar
# ninguna otra sección del archivo para realizar las variaciones
# solicitadas en la actividad.
# =============================================================================

@dataclass
class ParametrosPractica:
    """
    Conjunto de parámetros configurables de la simulación. Cada campo
    incluye un valor por defecto y una descripción de su efecto sobre
    el comportamiento del sistema. Modifique los valores y vuelva a
    ejecutar el script para observar el resultado de cada cambio.
    """

    # --- Geometría y dificultad del entorno ---

    tamano_entorno: int = 12
    # Dimensión de la cuadrícula (tamano_entorno x tamano_entorno celdas).
    # Sugerencia: compare un entorno pequeño (8) con uno grande (20) y
    # observe cómo cambia la ventaja relativa del agente basado en
    # modelos conforme el entorno crece.

    densidad_obstaculos: float = 0.15
    # Probabilidad, entre 0.0 y 1.0, de que una celda dada sea un
    # obstáculo. Un valor de 0.15 equivale a que, en promedio, el 15 %
    # de las celdas sean intransitables.
    # Sugerencia: incremente este valor a 0.30 y observe el efecto
    # sobre la ruta calculada por el agente basado en modelos.

    num_muestras: int = 6
    # Número de muestras (puntos de interés) que deben recolectarse.
    # Sugerencia: reduzca este valor a 1 para comparar qué arquitectura
    # localiza primero una muestra única; auméntelo a 15 para comparar
    # cobertura total del entorno.

    semilla: int = 79
    # Valor entero que determina de manera reproducible la disposición
    # de obstáculos y muestras en el entorno. Con la misma semilla se
    # genera siempre el mismo mapa; con una semilla distinta se genera
    # un mapa diferente, aunque igualmente reproducible.
    # Sugerencia: ejecute la comparación con varias semillas distintas
    # para verificar que la ventaja del agente basado en modelos se
    # sostiene de manera general y no depende de un mapa particular.

    # --- Presupuesto del agente ---

    energia_maxima: int = 80
    # Número máximo de pasos que el agente puede ejecutar antes de
    # agotar su energía disponible.
    # Sugerencia: reduzca este valor a 30 y determine si, con ese
    # presupuesto, cada arquitectura logra recolectar alguna muestra.

    # --- Pesos de la medida de desempeño (véase la función calcular_puntaje) ---

    peso_muestra: float = 10.0
    # Puntos otorgados por cada muestra recolectada.

    peso_celda_explorada: float = 1.0
    # Puntos otorgados por cada celda nueva explorada.

    peso_energia: float = 1
    # Puntos que se restan por cada unidad de energía consumida.
    # Sugerencia: incremente este valor a 1.0 y observe cómo un agente
    # que explora sin control de su consumo energético deja de ser
    # competitivo, aun cuando explore una mayor superficie. Este
    # ejercicio ilustra que la medida de desempeño determina qué se
    # considera un "buen" agente, conforme a lo señalado en la clase
    # magistral sobre racionalidad.

    # --- Nombres de los archivos de salida ---

    ruta_figura: str = "comparacion_practica1.png"
    ruta_animacion: str = "simulacion_practica1.gif"


# =============================================================================
# SECCIÓN 1. Definición del entorno
# =============================================================================

class TipoCelda(Enum):
    """
    Una enumeración (Enum) define un conjunto cerrado de valores
    válidos. En este caso, se establece que toda celda del entorno
    corresponde a exactamente uno de los siguientes tres estados.
    """
    LIBRE = "libre"           # el agente puede desplazarse a esta celda
    OBSTACULO = "obstaculo"   # celda intransitable
    MUESTRA = "muestra"       # punto de interés que debe recolectarse


# Marca interna utilizada por el agente basado en modelos para registrar
# que una celda vecina se encuentra fuera de los límites del entorno.
# Esta marca permite distinguir "el borde del mapa" de "territorio aún
# no explorado"; su uso se detalla en la sección correspondiente.
FUERA_DE_RANGO = "fuera_de_rango"


@dataclass
class Entorno:
    """
    Representa la cuadrícula completa de simulación. Esta clase
    conoce con exactitud la ubicación de cada obstáculo y cada
    muestra. Los agentes no tienen acceso directo a esta información:
    únicamente reciben lo que el método percibir_adyacentes() les
    proporciona, es decir, el contenido de las cuatro celdas contiguas
    a su posición actual. Esta restricción reproduce la condición de
    observabilidad parcial estudiada en clase.
    """
    tamano: int
    densidad_obstaculos: float = 0.15
    num_muestras: int = 6
    semilla: int = 42

    terreno: list = field(init=False)
    muestras_restantes: set = field(init=False)
    # La expresión field(init=False) indica que estos dos atributos NO
    # se reciben como argumento al crear un Entorno: en su lugar, se
    # calculan automáticamente dentro de __post_init__, inmediatamente
    # después de la creación del objeto.

    def __post_init__(self) -> None:
        """
        Python ejecuta automáticamente este método inmediatamente
        después de crear una instancia de Entorno. Aquí se genera la
        disposición del mapa: se determina qué celdas son obstáculo y
        en cuáles se ubica una muestra.
        """
        rng = random.Random(self.semilla)

        # Se inicializa la cuadrícula completa como celdas libres. La
        # estructura es una lista de listas: la lista externa
        # representa las filas; cada lista interna representa las
        # columnas correspondientes a esa fila.
        self.terreno = [
            [TipoCelda.LIBRE for _ in range(self.tamano)]
            for _ in range(self.tamano)
        ]

        # Se recorre cada celda del entorno y, con la probabilidad
        # indicada por densidad_obstaculos, se convierte en obstáculo.
        # La celda (0, 0) se conserva siempre libre, pues corresponde
        # al punto de partida del agente.
        for f in range(self.tamano):
            for c in range(self.tamano):
                if (f, c) == (0, 0):
                    continue
                if rng.random() < self.densidad_obstaculos:
                    self.terreno[f][c] = TipoCelda.OBSTACULO

        # Se seleccionan aleatoriamente, entre las celdas libres
        # restantes, las posiciones donde se ubicará cada muestra.
        celdas_libres = [
            (f, c)
            for f in range(self.tamano)
            for c in range(self.tamano)
            if self.terreno[f][c] == TipoCelda.LIBRE and (f, c) != (0, 0)
        ]
        rng.shuffle(celdas_libres)
        posiciones_muestras = celdas_libres[: self.num_muestras]
        for (f, c) in posiciones_muestras:
            self.terreno[f][c] = TipoCelda.MUESTRA

        self.muestras_restantes = set(posiciones_muestras)

    def dentro_de_rango(self, pos: tuple[int, int]) -> bool:
        """Determina si una posición (fila, columna) existe dentro del entorno."""
        f, c = pos
        return 0 <= f < self.tamano and 0 <= c < self.tamano

    def es_transitable(self, pos: tuple[int, int]) -> bool:
        """Determina si el agente puede ocupar la celda indicada."""
        if not self.dentro_de_rango(pos):
            return False
        f, c = pos
        return self.terreno[f][c] != TipoCelda.OBSTACULO

    def celdas_obstaculo(self) -> list:
        """Devuelve la lista de todas las celdas ocupadas por un obstáculo."""
        return [
            (f, c)
            for f in range(self.tamano)
            for c in range(self.tamano)
            if self.terreno[f][c] == TipoCelda.OBSTACULO
        ]

    def percibir_adyacentes(self, pos: tuple[int, int]) -> dict:
        """
        Constituye la única fuente de información que el agente
        recibe del entorno: el contenido de las cuatro celdas
        contiguas a la posición indicada. Toda dirección que quede
        fuera de los límites del entorno se omite del resultado. El
        resultado es un diccionario cuyas llaves son posiciones
        (fila, columna) y cuyos valores son el tipo de celda
        correspondiente.
        """
        f, c = pos
        vecinos = [(f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)]
        percepto = {}
        for v in vecinos:
            if self.dentro_de_rango(v):
                percepto[v] = self.terreno[v[0]][v[1]]
        return percepto

    def recolectar_si_hay_muestra(self, pos: tuple[int, int]) -> bool:
        """
        Si la posición indicada contiene una muestra, la recolecta
        (la elimina del entorno) y devuelve True. En caso contrario,
        devuelve False.
        """
        if pos in self.muestras_restantes:
            self.muestras_restantes.remove(pos)
            f, c = pos
            self.terreno[f][c] = TipoCelda.LIBRE
            return True
        return False


# =============================================================================
# SECCIÓN 2. Medida de desempeño
# =============================================================================

@dataclass
class Desempeno:
    """
    Registro acumulado de resultados de un agente durante la
    ejecución: celdas nuevas exploradas, muestras recolectadas y
    energía consumida.

    Conforme a lo señalado en la clase magistral, la medida de
    desempeño se define sobre el estado del entorno (celdas
    exploradas, muestras recolectadas) y no sobre las intenciones o
    creencias internas del agente. Un agente racional se evalúa por
    los resultados que produce en el mundo.
    """
    celdas_exploradas: int = 0
    muestras_recolectadas: int = 0
    energia_consumida: int = 0
    movimientos_efectivos: int = 0  # pasos en los que el agente cambió de celda
    veces_espero: int = 0           # pasos en los que el agente permaneció en su lugar


def calcular_puntaje(desempeno: Desempeno, parametros: ParametrosPractica) -> float:
    """
    Convierte el registro de desempeño en un valor numérico único,
    empleando los pesos definidos en ParametrosPractica. Es una
    función independiente (no pertenece a ninguna clase): recibe
    datos, realiza un cálculo y devuelve un resultado.
    """
    return (
        desempeno.muestras_recolectadas * parametros.peso_muestra
        + desempeno.celdas_exploradas * parametros.peso_celda_explorada
        - desempeno.energia_consumida * parametros.peso_energia
    )


# =============================================================================
# SECCIÓN 3. Clase base común a ambas arquitecturas
# =============================================================================

class AgenteExplorador:
    """
    Define la estructura común que debe seguir cualquier arquitectura
    de agente implementada en esta práctica, mediante tres operaciones
    fundamentales:

        1. percibir  - obtener información del entorno
        2. decidir   - seleccionar una acción
        3. actuar    - ejecutar dicha acción

    Este orden corresponde al ciclo percepción-decisión-acción descrito
    en la sesión introductoria del curso.

    Las clases AgenteReactivo y AgenteBasadoEnModelos, definidas más
    adelante, heredan de esta clase base: reutilizan tal cual los
    métodos percibir() y actuar(), pero cada una define su propia
    versión del método decidir(), que es precisamente donde reside la
    diferencia entre ambas arquitecturas.

    Diferencia conceptual entre ambas arquitecturas: el agente
    reactivo selecciona su acción exclusivamente a partir de lo que
    percibe en el instante presente, sin conservar ningún registro de
    lo ocurrido en pasos anteriores. El agente basado en modelos, en
    cambio, mantiene una variable adicional (una representación
    interna del entorno) que actualiza en cada percepción y consulta
    en cada decisión. En términos de programación, la diferencia entre
    ambas arquitecturas se reduce a la presencia o ausencia de un
    estado interno que persiste entre un paso de ejecución y el
    siguiente.
    """

    def __init__(self, posicion_inicial: tuple[int, int], energia_maxima: int):
        # El método __init__ se ejecuta automáticamente cada vez que
        # se crea un nuevo agente a partir de esta clase. Aquí se
        # inicializan sus atributos: la información interna asociada
        # a cada instancia.
        self.posicion = posicion_inicial
        self.energia_maxima = energia_maxima
        self.desempeno = Desempeno()
        self.historial_perceptos: list = []

    def percibir(self, entorno: Entorno) -> dict:
        """Solicita al entorno el contenido de las celdas adyacentes a la posición actual."""
        percepto = entorno.percibir_adyacentes(self.posicion)
        self.historial_perceptos.append(percepto)
        return percepto

    def decidir(self, percepto: dict) -> tuple[str, str]:
        """
        Este método debe ser definido por cada subclase (cada
        arquitectura de agente). Si una subclase no lo define, Python
        genera un error explícito en lugar de fallar de manera
        silenciosa.

        Debe devolver una tupla con dos elementos: la acción
        seleccionada (por ejemplo, "arriba") y una justificación en
        español de dicha decisión, empleada para elaborar la bitácora
        de ejecución.
        """
        raise NotImplementedError

    def actuar(self, accion: str, entorno: Entorno) -> bool:
        """
        Ejecuta la acción seleccionada por decidir(): desplaza al
        agente (cuando es posible) y descuenta la energía
        correspondiente. Devuelve True si, como resultado del
        movimiento, el agente recolectó una muestra.
        """
        f, c = self.posicion
        destino = {
            "arriba": (f - 1, c),
            "abajo": (f + 1, c),
            "izquierda": (f, c - 1),
            "derecha": (f, c + 1),
            "esperar": (f, c),
        }[accion]

        if accion != "esperar" and entorno.es_transitable(destino):
            self.posicion = destino
            self.desempeno.movimientos_efectivos += 1
        elif accion == "esperar":
            self.desempeno.veces_espero += 1

        # Toda acción, incluida "esperar", consume una unidad de
        # energía, ya que representa el transcurso de una unidad de
        # tiempo. Nótese que, en la práctica, "esperar" ejecuta como
        # máximo una sola vez por episodio: ejecutar_episodio() detiene
        # la simulación en cuanto ocurre, en lugar de repetirla hasta
        # agotar la energía disponible (véase la documentación de esa
        # función para el razonamiento completo).
        self.desempeno.energia_consumida += 1

        recolecto = entorno.recolectar_si_hay_muestra(self.posicion)
        if recolecto:
            self.desempeno.muestras_recolectadas += 1

        return recolecto


# =============================================================================
# SECCIÓN 4. Arquitectura 1: agente de reflejo simple (reactivo)
# =============================================================================

class AgenteReactivo(AgenteExplorador):
    """
    La expresión "class AgenteReactivo(AgenteExplorador)" indica que
    esta clase hereda de AgenteExplorador: reutiliza sus métodos
    percibir() y actuar(), y define su propia versión de decidir().

    Esta arquitectura selecciona su acción únicamente a partir del
    percepto actual, mediante reglas de tipo condición-acción, sin
    mantener memoria alguna de los estados previos del entorno. En
    consecuencia, puede visitar reiteradamente una misma celda sin
    tener manera de advertirlo.
    """

    def decidir(self, percepto: dict) -> tuple[str, str]:
        """
        El parámetro percepto es el diccionario con el contenido de
        las celdas adyacentes. A continuación se aplican reglas de
        condición-acción, evaluadas en orden de prioridad.
        """
        # Regla 1: si una muestra se encuentra en una celda adyacente,
        # el agente se desplaza directamente hacia ella.
        for pos, tipo in percepto.items():
            if tipo == TipoCelda.MUESTRA:
                motivo = f"Detecta una muestra en la celda adyacente {pos} y se dirige hacia ella."
                return self._direccion_hacia(pos), motivo

        # Regla 2: en ausencia de una muestra visible, se selecciona
        # de manera aleatoria una celda libre adyacente. En esta regla
        # reside la naturaleza reactiva de la arquitectura: la
        # decisión no considera si dicha celda ya fue visitada con
        # anterioridad, pues el agente no conserva ese registro.
        libres = [pos for pos, tipo in percepto.items() if tipo == TipoCelda.LIBRE]
        if libres:
            destino = random.choice(libres)
            motivo = (
                f"No percibe ninguna muestra; selecciona aleatoriamente la celda "
                f"libre adyacente {destino}, sin considerar si fue visitada previamente."
            )
            return self._direccion_hacia(destino), motivo

        # Regla 3: si no existe ninguna celda libre adyacente, el
        # agente permanece en su posición actual.
        return "esperar", "No existe ninguna celda libre adyacente disponible; permanece en su posición."

    def _direccion_hacia(self, destino: tuple[int, int]) -> str:
        """
        Método auxiliar (el guion bajo inicial indica que su uso está
        restringido al funcionamiento interno de esta clase). Traduce
        una posición vecina a la dirección de desplazamiento
        correspondiente.
        """
        f, c = self.posicion
        df, dc = destino
        if df < f:
            return "arriba"
        if df > f:
            return "abajo"
        if dc < c:
            return "izquierda"
        if dc > c:
            return "derecha"
        return "esperar"


# =============================================================================
# SECCIÓN 5. Arquitectura 2: agente basado en modelos
# =============================================================================

class AgenteBasadoEnModelos(AgenteExplorador):
    """
    Esta arquitectura incorpora, respecto de la clase base, un único
    elemento adicional: una variable de instancia, mapa_interno, que
    constituye la representación interna del entorno construida por
    el agente a partir de lo percibido. Cada vez que el agente
    percibe, no solo obtiene información: la incorpora a dicha
    representación. Al momento de decidir, en lugar de seleccionar una
    acción al azar, consulta su mapa interno para dirigirse hacia la
    celda conocida más cercana que sea adyacente a territorio aún no
    explorado (denominada, en adelante, "frontera").
    """

    def __init__(self, posicion_inicial: tuple[int, int], energia_maxima: int):
        # Se invoca el constructor de la clase base para inicializar
        # los atributos comunes (posición, energía, registro de
        # desempeño) y, a continuación, se agrega el atributo propio
        # de esta arquitectura: el mapa interno. Al inicio, el agente
        # únicamente tiene certeza sobre su propia celda de partida.
        super().__init__(posicion_inicial, energia_maxima)
        self.mapa_interno: dict = {posicion_inicial: TipoCelda.LIBRE}

    def percibir(self, entorno: Entorno) -> dict:
        """
        Reutiliza el método percibir() de la clase base mediante
        super(), y adicionalmente actualiza el mapa interno con la
        información recién obtenida. Esta actualización es
        precisamente lo que la arquitectura reactiva no realiza.
        """
        percepto = super().percibir(entorno)
        self.mapa_interno.update(percepto)

        # Toda dirección vecina que no figure en el percepto
        # corresponde a una celda fuera de los límites del entorno
        # (el entorno únicamente reporta celdas existentes). Dicha
        # dirección se registra con la marca FUERA_DE_RANGO, con el
        # fin de que el agente no confunda el borde del mapa con
        # territorio pendiente de exploración.
        f, c = self.posicion
        vecinos_esperados = [(f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)]
        for v in vecinos_esperados:
            if v not in percepto:
                self.mapa_interno.setdefault(v, FUERA_DE_RANGO)

        return percepto

    def decidir(self, percepto: dict) -> tuple[str, str]:
        # Al igual que en la arquitectura reactiva, si una muestra se
        # encuentra en una celda adyacente, el agente se dirige
        # directamente hacia ella.
        for pos, tipo in percepto.items():
            if tipo == TipoCelda.MUESTRA:
                motivo = f"El mapa interno confirma una muestra en {pos}; se dirige hacia ella."
                return self._paso_hacia(pos), motivo

        # La diferencia sustantiva respecto de la arquitectura
        # reactiva se encuentra en este punto: en lugar de una
        # selección aleatoria, se consulta el mapa interno para
        # localizar la frontera de exploración más cercana y se
        # calcula la ruta correspondiente.
        objetivo = self._frontera_mas_cercana()
        if objetivo:
            motivo = (
                f"No percibe ninguna muestra; consulta su mapa interno y se dirige "
                f"a la frontera de territorio no explorado más cercana, próxima a {objetivo}."
            )
            return self._paso_hacia(objetivo), motivo

        return "esperar", "El mapa interno no registra fronteras alcanzables; permanece en su posición."

    def _frontera_mas_cercana(self) -> Optional[tuple[int, int]]:
        """
        Recorre el mapa interno mediante una búsqueda en anchura
        (Breadth-First Search, BFS): se examinan primero las celdas
        más próximas a la posición actual y, progresivamente, las más
        alejadas, hasta identificar la primera celda conocida que sea
        adyacente a una celda no registrada en el mapa interno. Dicha
        celda constituye la frontera de exploración.

        La estructura deque se utiliza por ser una estructura de datos
        eficiente para extraer elementos de un extremo mientras se
        agregan por el otro, característica requerida por este tipo de
        búsqueda.
        """
        visitados = {self.posicion}
        cola = deque([self.posicion])

        while cola:
            actual = cola.popleft()
            f, c = actual
            vecinos = [(f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)]

            for v in vecinos:
                if v in visitados:
                    continue

                if v not in self.mapa_interno:
                    # Se identificó una celda no registrada en el mapa
                    # interno: la celda "actual", desde la cual se
                    # observó, constituye la frontera buscada.
                    return actual

                contenido = self.mapa_interno[v]
                if contenido == FUERA_DE_RANGO:
                    continue  # límite del entorno: no constituye frontera ni es transitable

                if contenido != TipoCelda.OBSTACULO:
                    visitados.add(v)
                    cola.append(v)

        return None  # no existe ninguna frontera alcanzable

    def _paso_hacia(self, objetivo: tuple[int, int]) -> str:
        """
        Una vez determinado el destino, este método calcula el primer
        paso de la ruta más corta conocida hacia dicho destino,
        mediante otra búsqueda en anchura, en este caso orientada a
        encontrar un camino.
        """
        if objetivo == self.posicion:
            return "esperar"

        inicio = self.posicion
        # El diccionario "padres" registra, para cada celda visitada
        # durante la búsqueda, la celda desde la cual fue alcanzada.
        # Esta información permite reconstruir, al final, cuál fue el
        # primer paso del recorrido.
        padres = {inicio: None}
        cola = deque([inicio])

        while cola:
            actual = cola.popleft()
            if actual == objetivo:
                break
            f, c = actual
            vecinos = [(f - 1, c), (f + 1, c), (f, c - 1), (f, c + 1)]
            for v in vecinos:
                conocido_transitable = (
                    v in self.mapa_interno
                    and self.mapa_interno[v] not in (TipoCelda.OBSTACULO, FUERA_DE_RANGO)
                ) or v == objetivo
                if conocido_transitable and v not in padres:
                    padres[v] = actual
                    cola.append(v)

        if objetivo not in padres:
            return "esperar"  # no se identificó ninguna ruta conocida hacia el objetivo

        paso = objetivo
        while padres[paso] != inicio:
            paso = padres[paso]

        return self._direccion_entre(inicio, paso)

    def _direccion_entre(self, origen: tuple[int, int], destino: tuple[int, int]) -> str:
        f, c = origen
        df, dc = destino
        if df < f:
            return "arriba"
        if df > f:
            return "abajo"
        if dc < c:
            return "izquierda"
        if dc > c:
            return "derecha"
        return "esperar"


# =============================================================================
# SECCIÓN 6. Simulador: ejecución de un episodio completo
# =============================================================================

def ejecutar_episodio(agente: AgenteExplorador, entorno: Entorno, energia_maxima: int) -> tuple[list, list]:
    """
    Ejecuta de manera reiterada el ciclo percepción-decisión-acción,
    mediante una instrucción while, hasta que el agente agota su
    energía disponible o hasta que deja de tener alguna acción
    productiva por realizar. Constituye el mecanismo central de la
    simulación.

    Condición de paro anticipado: en esta implementación, la acción
    "esperar" únicamente se produce cuando el agente no percibe
    ninguna muestra y, además, no existe ninguna celda libre adyacente
    (caso del agente reactivo) o ninguna frontera de exploración
    alcanzable en su mapa interno (caso del agente basado en modelos).
    Dado que el entorno es estático -los obstáculos no cambian de
    posición durante la simulación-, ambas condiciones son
    permanentes: si se cumplen en un paso determinado, se seguirán
    cumpliendo en todos los pasos siguientes. Por ello, en cuanto el
    agente selecciona "esperar", el episodio se da por concluido de
    inmediato, en lugar de continuar consumiendo energía sin ningún
    efecto sobre el resultado.

    Devuelve dos listas:
      - trayectoria: la secuencia completa de posiciones ocupadas por
        el agente, empleada posteriormente para representar su
        recorrido.
      - bitacora: un registro paso a paso de las acciones ejecutadas y
        su justificación, destinado a la elaboración del reporte de la
        práctica. El último elemento de la bitácora indica, mediante
        su campo "motivo", la causa exacta de la finalización del
        episodio (agotamiento de energía o ausencia de acciones
        productivas).
    """
    trayectoria = [agente.posicion]
    bitacora = []
    paso = 0

    while agente.desempeno.energia_consumida < energia_maxima:
        percepto = agente.percibir(entorno)
        accion, motivo = agente.decidir(percepto)
        recolecto = agente.actuar(accion, entorno)
        paso += 1

        bitacora.append({
            "paso": paso,
            "accion": accion,
            "motivo": motivo,
            "posicion": agente.posicion,
            "muestra_recolectada": recolecto,
        })
        trayectoria.append(agente.posicion)

        if accion == "esperar":
            # Condición permanente (véase la explicación anterior):
            # continuar el bucle únicamente repetiría la misma espera
            # hasta agotar la energía disponible, sin ningún cambio en
            # el resultado. Se detiene el episodio de inmediato.
            break

    # La expresión set(trayectoria) elimina las posiciones repetidas;
    # su longitud corresponde al número de celdas únicas visitadas.
    agente.desempeno.celdas_exploradas = len(set(trayectoria))
    return trayectoria, bitacora


# =============================================================================
# SECCIÓN 7. Comparación de arquitecturas sobre un entorno común
# =============================================================================

def comparar_arquitecturas(parametros: ParametrosPractica) -> dict:
    """
    Ejecuta, de manera sucesiva, al agente reactivo y al agente
    basado en modelos, empleando en ambos casos la misma semilla
    aleatoria, con el fin de garantizar que la comparación se realice
    sobre entornos idénticos. El resultado es un diccionario que
    contiene la información necesaria para generar el reporte y las
    figuras correspondientes.
    """
    resultados = {}

    for nombre_arquitectura, clase_agente in [
        ("Reactivo", AgenteReactivo),
        ("Basado en modelos", AgenteBasadoEnModelos),
    ]:
        random.seed(parametros.semilla)
        entorno = Entorno(
            tamano=parametros.tamano_entorno,
            densidad_obstaculos=parametros.densidad_obstaculos,
            num_muestras=parametros.num_muestras,
            semilla=parametros.semilla,
        )
        # Se registra la disposición inicial del entorno antes de
        # ejecutar la simulación, dado que este se modifica conforme
        # las muestras son recolectadas.
        obstaculos = entorno.celdas_obstaculo()
        muestras_originales = set(entorno.muestras_restantes)

        agente = clase_agente(
            posicion_inicial=(0, 0), energia_maxima=parametros.energia_maxima
        )
        trayectoria, bitacora = ejecutar_episodio(agente, entorno, parametros.energia_maxima)

        muestras_recolectadas_en = {
            evento["posicion"] for evento in bitacora if evento["muestra_recolectada"]
        }

        resultados[nombre_arquitectura] = {
            "desempeno": agente.desempeno,
            "trayectoria": trayectoria,
            "bitacora": bitacora,
            "obstaculos": obstaculos,
            "muestras_originales": muestras_originales,
            "muestras_recolectadas_en": muestras_recolectadas_en,
            "tamano_entorno": parametros.tamano_entorno,
            "total_muestras": parametros.num_muestras,
            "puntaje": calcular_puntaje(agente.desempeno, parametros),
        }

    return resultados


def imprimir_comparacion(resultados: dict, parametros: ParametrosPractica) -> None:
    """Presenta en la terminal una tabla comparativa del desempeño de ambas arquitecturas."""
    print("=" * 78)
    print("COMPARACIÓN DE ARQUITECTURAS - PRÁCTICA 1: AGENTE EXPLORADOR")
    print(
        f"Entorno: {parametros.tamano_entorno}x{parametros.tamano_entorno}  |  "
        f"Obstáculos: {parametros.densidad_obstaculos:.0%}  |  "
        f"Muestras: {parametros.num_muestras}  |  "
        f"Energía: {parametros.energia_maxima}  |  Semilla: {parametros.semilla}"
    )
    print("=" * 78)

    encabezado = f"{'Métrica':<32}{'Reactivo':>18}{'Basado en modelos':>24}"
    print(encabezado)
    print("-" * 78)

    d_r = resultados["Reactivo"]["desempeno"]
    d_m = resultados["Basado en modelos"]["desempeno"]
    total_muestras = resultados["Reactivo"]["total_muestras"]

    # "Movimientos hacia celda ya conocida" cuantifica los pasos
    # invertidos en zonas previamente visitadas por el agente.
    revisitas_r = max(0, d_r.movimientos_efectivos - (d_r.celdas_exploradas - 1))
    revisitas_m = max(0, d_m.movimientos_efectivos - (d_m.celdas_exploradas - 1))

    filas = [
        ("Celdas exploradas", d_r.celdas_exploradas, d_m.celdas_exploradas),
        (f"Muestras recolectadas (de {total_muestras})", d_r.muestras_recolectadas, d_m.muestras_recolectadas),
        ("Energía consumida", d_r.energia_consumida, d_m.energia_consumida),
        ("Movimientos hacia celda ya conocida", revisitas_r, revisitas_m),
        ("Puntaje de desempeño", round(resultados["Reactivo"]["puntaje"], 1), round(resultados["Basado en modelos"]["puntaje"], 1)),
    ]

    for etiqueta, val_r, val_m in filas:
        print(f"{etiqueta:<32}{val_r:>18}{val_m:>24}")

    print("=" * 78)

    # Si un agente concluyó su episodio antes de agotar la energía
    # disponible, se debe a que dejó de tener acciones productivas
    # por realizar (véase la condición de paro anticipado documentada
    # en ejecutar_episodio). Se informa explícitamente para que no se
    # confunda con un error de ejecución.
    for nombre, datos in resultados.items():
        d = datos["desempeno"]
        if d.energia_consumida < parametros.energia_maxima:
            print(
                f"Nota: el agente {nombre} concluyó su episodio en el paso "
                f"{d.energia_consumida} (de {parametros.energia_maxima} disponibles); "
                "no le quedaban acciones productivas por realizar."
            )


def imprimir_bitacora(resultados: dict, max_eventos: int = 4) -> None:
    """
    Presenta los momentos más relevantes de la ejecución -no la
    totalidad del registro, con el fin de mantener la legibilidad del
    reporte-: las primeras decisiones de cada agente y cada evento de
    recolección de una muestra.
    """
    print("\nBITÁCORA DE EJECUCIÓN (eventos relevantes)")
    print("-" * 78)

    for nombre, datos in resultados.items():
        print(f"\n[{nombre}]")
        bitacora = datos["bitacora"]

        primeros = bitacora[:max_eventos]
        for evento in primeros:
            print(f"  Paso {evento['paso']:>3}: {evento['motivo']}")

        eventos_muestra = [e for e in bitacora if e["muestra_recolectada"]]
        if eventos_muestra:
            print("  (...)")
            for evento in eventos_muestra:
                print(f"  Paso {evento['paso']:>3}: Muestra recolectada en {evento['posicion']}.")
        else:
            print("  (...) no se recolectó ninguna muestra durante el episodio.")

    print("\nINTERPRETACIÓN")
    print("-" * 78)
    print(
        "Se espera que el agente basado en modelos presente un menor número de\n"
        "'movimientos hacia celda ya conocida' que el agente reactivo: al conservar\n"
        "un registro de las celdas ya visitadas, orienta su energía hacia territorio\n"
        "nuevo en lugar de desplazarse sin dirección definida. Esta diferencia es\n"
        "precisamente la que distingue a un programa de agente de reflejo simple de\n"
        "uno basado en modelos, conforme a lo revisado en la sesión introductoria\n"
        "del curso."
    )


# =============================================================================
# SECCIÓN 8. Generación de la figura comparativa
# =============================================================================

def generar_figura_comparativa(resultados: dict, parametros: ParametrosPractica) -> None:
    """
    Genera un archivo de imagen que muestra, para cada agente:
      - el entorno real, con los obstáculos señalados;
      - las muestras, distinguiendo las recolectadas de las no
        recolectadas;
      - un mapa de calor que indica la frecuencia con la que cada
        celda fue visitada nuevamente;
      - la trayectoria completa, coloreada según el orden temporal del
        recorrido, del inicio al final del episodio.

    Esta función requiere la biblioteca matplotlib. Si dicha
    biblioteca no se encuentra instalada, el programa continúa su
    ejecución sin generar la figura, e informa dicha situación.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")  # modo de generación de archivos sin interfaz gráfica
        import matplotlib.pyplot as plt
        from matplotlib.patches import Patch
        from matplotlib.lines import Line2D
    except ImportError:
        print("\nNota: la biblioteca matplotlib no está disponible; no se generó la figura comparativa.")
        return

    tamano = parametros.tamano_entorno
    fig, ejes = plt.subplots(1, 2, figsize=(13, 6.5))

    # "zip(ejes, resultados.items())" empareja cada uno de los dos
    # paneles de la figura (ejes) con los resultados de una
    # arquitectura, en el mismo orden, para dibujarlos juntos en cada
    # vuelta del bucle: primero el panel del reactivo con sus datos,
    # después el panel del basado en modelos con los suyos.
    for eje, (nombre, datos) in zip(ejes, resultados.items()):
        trayectoria = datos["trayectoria"]
        # Counter cuenta cuántas veces se repite cada posición dentro
        # de la lista trayectoria; es decir, cuántas veces el agente
        # pisó cada celda a lo largo de todo el episodio.
        conteo_visitas = Counter(trayectoria)

        # Mapa de calor de revisitas (capa de fondo).
        max_visitas = max(conteo_visitas.values())
        for (f, c), veces in conteo_visitas.items():
            intensidad = veces / max_visitas
            eje.scatter(
                c, f, marker="s", s=430, color=plt.cm.YlOrRd(0.25 + 0.65 * intensidad),
                alpha=0.85, linewidths=0, zorder=1,
            )

        # Obstáculos.
        if datos["obstaculos"]:
            of = [p[0] for p in datos["obstaculos"]]
            oc = [p[1] for p in datos["obstaculos"]]
            eje.scatter(oc, of, marker="s", s=430, color="#4B5563", zorder=2)

        # Trayectoria, coloreada según el orden temporal del recorrido.
        filas_tray = [p[0] for p in trayectoria]
        cols_tray = [p[1] for p in trayectoria]
        eje.plot(cols_tray, filas_tray, "-", linewidth=1.0, color="#1F2937", alpha=0.35, zorder=3)
        eje.scatter(
            cols_tray, filas_tray, c=range(len(trayectoria)), cmap="viridis",
            s=22, zorder=4, edgecolors="none",
        )

        # Muestras: marcador relleno si fue recolectada, hueco en caso contrario.
        for (f, c) in datos["muestras_originales"]:
            recolectada = (f, c) in datos["muestras_recolectadas_en"]
            eje.scatter(
                c, f, marker="*", s=380,
                color="#F59E0B" if recolectada else "white",
                edgecolors="#B45309", linewidths=1.3, zorder=5,
            )

        # Posiciones de inicio y fin del episodio.
        eje.scatter([cols_tray[0]], [filas_tray[0]], s=140, color="#16A34A", edgecolors="white", linewidths=1.5, zorder=6)
        eje.scatter([cols_tray[-1]], [filas_tray[-1]], s=140, color="#DC2626", marker="X", edgecolors="white", linewidths=1.5, zorder=6)

        # Resumen numérico de desempeño, ubicado como subtítulo por
        # ENCIMA de la cuadrícula (no sobre ella), para que ninguna
        # celda del mapa quede cubierta por el texto, sin importar en
        # qué parte del entorno se concentre la trayectoria.
        d = datos["desempeno"]
        texto = (
            f"Celdas exploradas: {d.celdas_exploradas}   "
            f"Muestras: {d.muestras_recolectadas}/{datos['total_muestras']}   "
            f"Energía consumida: {d.energia_consumida}   "
            f"Puntaje: {datos['puntaje']:.1f}"
        )
        eje.text(
            0.5, 1.02, texto, transform=eje.transAxes, fontsize=9,
            va="bottom", ha="center", family="monospace",
        )

        # "pad" separa el título del borde superior de la cuadrícula,
        # dejando espacio suficiente para el subtítulo con las
        # métricas, que se dibuja justo debajo del título.
        eje.set_title(nombre, fontsize=13, fontweight="bold", pad=32)
        eje.set_xlim(-1, tamano)
        eje.set_ylim(tamano, -1)
        eje.set_aspect("equal")
        eje.set_xticks([])
        eje.set_yticks([])
        # Líneas de cuadrícula, para delimitar con claridad cada celda del entorno.
        eje.set_xticks([x - 0.5 for x in range(tamano + 1)], minor=True)
        eje.set_yticks([y - 0.5 for y in range(tamano + 1)], minor=True)
        eje.grid(which="minor", color="#E5E7EB", linewidth=0.6)
        eje.tick_params(which="minor", bottom=False, left=False)
        for spine in eje.spines.values():
            spine.set_visible(False)

    # Los siguientes elementos (Patch y Line2D) no se dibujan sobre el
    # mapa: son únicamente muestras visuales que matplotlib utiliza
    # para construir el recuadro de leyenda de la figura, con la
    # combinación de forma y color que corresponde a cada elemento
    # real del mapa (obstáculo, muestra, inicio, fin, etc.).
    elementos_leyenda = [
        Patch(facecolor="#4B5563", label="Obstáculo"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor="#F59E0B", markeredgecolor="#B45309", markersize=14, label="Muestra recolectada"),
        Line2D([0], [0], marker="*", color="w", markerfacecolor="white", markeredgecolor="#B45309", markersize=14, label="Muestra no recolectada"),
        Patch(facecolor=plt.cm.YlOrRd(0.8), label="Celda con múltiples visitas"),
        Line2D([0], [0], marker="o", color="w", markerfacecolor="#16A34A", markersize=10, label="Inicio del episodio"),
        Line2D([0], [0], marker="X", color="w", markerfacecolor="#DC2626", markersize=10, label="Fin del episodio"),
    ]
    fig.legend(handles=elementos_leyenda, loc="lower center", ncol=6, fontsize=8.5, frameon=False, bbox_to_anchor=(0.5, -0.02))

    fig.suptitle(
        "Comparación de arquitecturas: agente reactivo frente a agente basado en modelos\n"
        "(color de la trayectoria: inicio del episodio en morado, final en amarillo)",
        fontsize=12,
    )
    fig.tight_layout(rect=[0, 0.05, 1, 0.90])

    ruta_absoluta = _ruta_junto_al_script(parametros.ruta_figura)
    fig.savefig(ruta_absoluta, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\nFigura comparativa generada correctamente. Ubicación:\n  {ruta_absoluta}")


# =============================================================================
# SECCIÓN 8b. Generación de la animación del recorrido
# =============================================================================

def generar_animacion(resultados: dict, parametros: ParametrosPractica, fps: int = 8) -> None:
    """
    Genera un archivo de animación (formato GIF) que reproduce, de
    manera secuencial, el desplazamiento de cada agente por el
    entorno completo: el recorrido acumulado, el instante exacto en
    que cada muestra es recolectada, y un contador del paso de
    simulación en curso. Ambos paneles se presentan sincronizados,
    dado que ambos agentes se ejecutan con la misma energía máxima.

    El parámetro fps ("cuadros por segundo") determina la velocidad de
    reproducción de la animación.

    Esta función requiere las bibliotecas matplotlib y Pillow. Si
    alguna de ellas no se encuentra instalada, el programa continúa su
    ejecución sin generar la animación, e informa dicha situación junto
    con la instrucción de instalación correspondiente.
    """
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        import matplotlib.animation as animation
    except ImportError:
        print("\nNota: la biblioteca matplotlib no está disponible; no se generó la animación.")
        return

    # La generación del archivo GIF requiere específicamente la
    # biblioteca Pillow, distinta de matplotlib. Se verifica su
    # disponibilidad antes de continuar, con el fin de informar con
    # precisión la causa de una eventual falla.
    try:
        # Esta importación solo sirve para comprobar que Pillow está
        # instalado; el módulo PIL en sí no se usa de forma directa
        # más adelante en el código (por eso se agrega el comentario
        # "noqa: F401", una indicación para herramientas de revisión
        # automática de que esta importación, aunque no se referencia
        # después, es intencional).
        import PIL  # noqa: F401
    except ImportError:
        print(
            "\nNota: no se generó la animación porque la biblioteca Pillow no está "
            "instalada.\nPara instalarla, ejecute: pip install pillow\n"
            "El reporte en terminal y la figura comparativa se generaron sin inconvenientes."
        )
        return

    tamano = parametros.tamano_entorno
    num_frames = parametros.energia_maxima + 1  # incluye la posición inicial (paso 0)

    fig, ejes = plt.subplots(1, 2, figsize=(13, 6.8))
    # Aquí guardamos, para cada panel, referencias a los elementos
    # gráficos que se irán actualizando cuadro a cuadro (en vez de
    # volver a dibujar todo desde cero en cada cuadro, lo cual sería
    # mucho más lento).
    referencias_por_eje = {}

    # Igual que en generar_figura_comparativa, zip empareja cada panel
    # con los resultados de una arquitectura, en el mismo orden.
    for eje, (nombre, datos) in zip(ejes, resultados.items()):
        # Elementos fijos: obstáculos.
        if datos["obstaculos"]:
            of = [p[0] for p in datos["obstaculos"]]
            oc = [p[1] for p in datos["obstaculos"]]
            eje.scatter(oc, of, marker="s", s=420, color="#4B5563", zorder=2)

        # Muestras: posición fija; el color se actualiza en cada cuadro.
        muestras_orden = list(datos["muestras_originales"])
        scatter_muestras = eje.scatter(
            [p[1] for p in muestras_orden], [p[0] for p in muestras_orden],
            marker="*", s=380, facecolors="white", edgecolors="#B45309",
            linewidths=1.3, zorder=5,
        )

        # Línea que representa el recorrido acumulado hasta el cuadro actual.
        (linea_rastro,) = eje.plot([], [], "-", linewidth=1.4, color="#2563EB", alpha=0.55, zorder=3)

        # Marcador de la posición actual del agente.
        marcador_agente = eje.scatter([], [], s=260, color="#2563EB", edgecolors="white", linewidths=1.8, zorder=6)

        # Marca fija del punto de partida.
        inicio = datos["trayectoria"][0]
        eje.scatter([inicio[1]], [inicio[0]], s=90, marker="o", facecolors="none", edgecolors="#16A34A", linewidths=2, zorder=6)

        # Recuadro de estado (paso, celdas exploradas, muestras
        # recolectadas), ubicado como subtítulo por ENCIMA de la
        # cuadrícula, para que no cubra ninguna celda del mapa
        # conforme el agente avanza por el entorno.
        texto_estado = eje.text(
            0.5, 1.02, "", transform=eje.transAxes, fontsize=9,
            va="bottom", ha="center", family="monospace",
        )

        eje.set_title(nombre, fontsize=13, fontweight="bold", pad=32)
        eje.set_xlim(-1, tamano)
        eje.set_ylim(tamano, -1)
        eje.set_aspect("equal")
        eje.set_xticks([])
        eje.set_yticks([])
        eje.set_xticks([x - 0.5 for x in range(tamano + 1)], minor=True)
        eje.set_yticks([y - 0.5 for y in range(tamano + 1)], minor=True)
        eje.grid(which="minor", color="#E5E7EB", linewidth=0.6)
        eje.tick_params(which="minor", bottom=False, left=False)
        for spine in eje.spines.values():
            spine.set_visible(False)

        referencias_por_eje[nombre] = {
            "scatter_muestras": scatter_muestras,
            "linea_rastro": linea_rastro,
            "marcador_agente": marcador_agente,
            "texto_estado": texto_estado,
            "muestras_orden": muestras_orden,
        }

    fig.suptitle("Simulación del recorrido, paso a paso", fontsize=13)
    fig.tight_layout(rect=[0, 0, 1, 0.90])

    def actualizar(frame):
        """
        Esta función se ejecuta una vez por cada cuadro de la
        animación. El parámetro frame corresponde al número de cuadro
        en curso (0, 1, 2, ...). En cada llamada se determina qué
        información corresponde mostrar hasta ese punto de la
        simulación, y se actualizan los elementos gráficos ya creados,
        en lugar de generarlos nuevamente en cada cuadro.
        """
        artistas = []
        for nombre, datos in resultados.items():
            ref = referencias_por_eje[nombre]
            trayectoria_hasta_ahora = datos["trayectoria"][: frame + 1]
            eventos_hasta_ahora = datos["bitacora"][:frame]

            filas = [p[0] for p in trayectoria_hasta_ahora]
            cols = [p[1] for p in trayectoria_hasta_ahora]
            ref["linea_rastro"].set_data(cols, filas)
            ref["marcador_agente"].set_offsets([[cols[-1], filas[-1]]])

            recolectadas_hasta_ahora = {
                e["posicion"] for e in eventos_hasta_ahora if e["muestra_recolectada"]
            }
            colores = [
                "#F59E0B" if pos in recolectadas_hasta_ahora else "white"
                for pos in ref["muestras_orden"]
            ]
            ref["scatter_muestras"].set_facecolor(colores)

            ref["texto_estado"].set_text(
                f"Paso: {frame}/{parametros.energia_maxima}   "
                f"Celdas visitadas: {len(set(trayectoria_hasta_ahora))}   "
                f"Muestras: {len(recolectadas_hasta_ahora)}/{datos['total_muestras']}"
            )

            artistas.extend([
                ref["linea_rastro"], ref["marcador_agente"],
                ref["scatter_muestras"], ref["texto_estado"],
            ])
        return artistas

    anim = animation.FuncAnimation(fig, actualizar, frames=num_frames, interval=1000 / fps, blit=False)

    ruta_absoluta = _ruta_junto_al_script(parametros.ruta_animacion)
    try:
        anim.save(ruta_absoluta, writer=animation.PillowWriter(fps=fps))
        print(f"Animación generada correctamente. Ubicación:\n  {ruta_absoluta}")
    except Exception as exc:
        print(
            f"\nNota: no fue posible generar la animación. Detalle del error:\n  {exc}\n"
            "Verifique que la biblioteca Pillow esté instalada (pip install pillow) "
            "y que se cuente con permisos de escritura en la carpeta del script."
        )
    finally:
        plt.close(fig)


# =============================================================================
# SECCIÓN 9. Punto de entrada del programa
# =============================================================================

# La expresión "if __name__ == '__main__':" es una convención estándar
# del lenguaje Python: indica que el bloque de código siguiente se
# ejecuta únicamente cuando este archivo se ejecuta de manera directa,
# y no cuando es incorporado como componente de otro programa. En la
# práctica, constituye el punto de inicio de la ejecución completa.
if __name__ == "__main__":
    parametros = ParametrosPractica()  # modifique los valores en la Sección 0

    carpeta_de_salida = os.path.dirname(os.path.abspath(__file__))
    print(f"Los archivos generados por esta ejecución se guardarán en:\n  {carpeta_de_salida}\n")

    resultados = comparar_arquitecturas(parametros)
    imprimir_comparacion(resultados, parametros)
    imprimir_bitacora(resultados)
    generar_figura_comparativa(resultados, parametros)
    generar_animacion(resultados, parametros)