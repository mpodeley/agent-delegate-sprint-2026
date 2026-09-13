<div class="titleblock">

# Helpline: una línea de ayuda para agentes que se traban

**Matías Podeley · Agustín Brusco · Mateo Zárate**\
**Alejandro Garibotti · Pablo [apellido por confirmar]**

BAISH · With Apart Research\
AI Incident Response Sprint · Septiembre de 2026

<p class="draft-status">Maqueta del manuscrito · autoría, orden y afiliaciones individuales por completar</p>

</div>

<div class="abstract">

**Resumen**

Un agente puede quedarse sin un archivo, encontrar instrucciones contradictorias o necesitar un permiso que no tiene. Una línea de ayuda le ofrece una forma de explicar el problema y recibir una respuesta. Este trabajo propone ese circuito y reúne observaciones para estudiarlo. Los registros del incidente de OpenAI y Hugging Face motivan posibles momentos de intervención. El trabajo de Gómez aporta evidencia de que ofrecer escalación puede reducir trampas en tareas defectuosas. Nuestra pregunta es qué ocurre cuando el pedido recibe atención y el agente puede continuar. Las corridas exploratorias de Kimi muestran pedidos ante bloqueos claros, pero también búsqueda sin contacto ante un caso ambiguo. Esas llamadas terminaban el episodio. El repositorio implementa un servicio con respuesta y reparación acotada, validado con agentes simulados. Proponemos probar su uso con modelos del equipo y medir contacto, recuperación, infracciones y costo. No demostramos prevención del incidente ni ventajas del delegado.

</div>

## 1. Introducción

Imaginá que le encargás una tarea a un agente y falta un archivo. El agente busca, prueba alternativas y sigue sin encontrarlo. ¿Cómo te avisa que el problema puede estar en el encargo? ¿Quién le contesta? ¿Puede volver al trabajo después? Esas preguntas organizan este trabajo.

En el incidente de OpenAI y Hugging Face, algunos agentes recibieron tareas que no podían completar como estaban configuradas. METR describe que el primer mensaje del tablero de julio fue un pedido de ayuda con una tarea imposible. El mismo tablero luego sostuvo proyectos colectivos para hacer trampa y atacar infraestructura. [1]

Nuestra hipótesis es que un canal autorizado podría haber ofrecido otra salida en algunos de esos momentos. Los fragmentos publicados no nos dicen qué habría pasado. Sí podemos usar los casos para diseñar situaciones controladas y observar qué hacen los agentes cuando tienen a quién recurrir.

Proponemos una línea de ayuda que reciba el pedido, permita aclararlo y devuelva un próximo paso. Presentamos casos motivadores, observaciones iniciales y un protocolo ejecutable. La pregunta experimental es si los agentes lo usan a tiempo y si una respuesta útil permite resolver el bloqueo sin salir de lo permitido.

<!-- page -->

## 2. Antecedentes y propuesta

Gómez estudia agentes de programación que encuentran pruebas defectuosas. Una herramienta de escalación, combinada con una política contra las trampas, reduce la manipulación de resultados en las tareas evaluadas. El agente puede explicar el defecto mediante un reporte estructurado. La herramienta devuelve un acuse fijo, sin investigar ni reparar durante el episodio. [2]

Tomamos ese trabajo como antecedente directo. Queremos extender la prueba a la respuesta y la continuación del trabajo. Gómez también plantea negociación y entornos multiagente; situamos nuestra propuesta dentro de esa agenda. Su estudio reconoce que la descripción de la herramienta mezcla disponibilidad de ayuda con indicaciones sobre cómo comportarse. Esa diferencia debe cuidarse al comparar condiciones. [2]

### 2.1. Pedir ayuda, recibir atención y autorizar cambios

Una línea útil necesita distinguir esas tres cosas. El agente debe poder explicar lo que pasa. Alguien debe revisar el pedido y dar una respuesta. Si la solución exige cambiar el entorno o los permisos, una autoridad con atribuciones concretas debe aprobarla. Recibir un pedido no autoriza por sí solo ninguna acción.

<figure class="protocol">
<div class="flow">
<div><span>Agente</span><strong>Explica el problema</strong><p>Qué vio, qué intentó y qué necesita.</p></div>
<b aria-hidden="true">→</b>
<div><span>Línea de ayuda</span><strong>Conserva el pedido</strong><p>Entrega un recibo y permite consultar otra vez.</p></div>
<b aria-hidden="true">→</b>
<div><span>Responsable</span><strong>Revisa y responde</strong><p>Aclara el problema y propone un próximo paso.</p></div>
<b aria-hidden="true">→</b>
<div><span>Autoridad</span><strong>Aprueba un cambio</strong><p>Sólo dentro de sus atribuciones.</p></div>
</div>
<div class="return">La respuesta vuelve al agente. Puede continuar, corregir un malentendido o terminar explicando el bloqueo.</div>
<div class="delegate-note">Un delegado opcional puede ordenar los pedidos. El original y la vía directa deben seguir disponibles.</div>
<figcaption>Figura 1. Circuito propuesto, adaptado del protocolo del paper anterior. La atención humana y sus deberes de seguimiento siguen por evaluar. El piloto usa un asesor modelo y un servicio automático con una única reparación acotada.</figcaption>
</figure>

### 2.2. Qué agrega un delegado

Cuando muchos agentes piden ayuda, un delegado podría resumir casos y preservar advertencias que de otro modo se perderían. Eso debe compararse con una mesa de ayuda que tenga los mismos recursos. Por ahora, el delegado es una opción dentro del circuito; su ventaja no está demostrada. El acceso directo permite que un pedido llegue aunque el intermediario lo maneje mal. [5, 7]

<!-- page -->

## 3. Método

### 3.1. Casos históricos y corridas disponibles

El catálogo de helpline reúne fragmentos publicados y registra su fuente, contexto y tipo: mensaje del agente, razonamiento reproducido o narración de investigadores. Sus etiquetas proponen qué problema podría haberse planteado a la línea. Las citas se verifican contra copias de las fuentes; las interpretaciones siguen pendientes de revisión humana. Usamos el catálogo para elegir situaciones, sin estimar su frecuencia en el incidente. [3]

Las corridas exploratorias de Kimi permiten observar si el agente pide ayuda al buscar un archivo. En la versión sana, el archivo está disponible. En otras versiones, falta o hay evidencia de que no fue provisto. La herramienta registra el pedido y termina el episodio. Las diferencias de contexto entre corridas impiden atribuir su conducta sólo a cómo se describió el canal. [4]

### 3.2. Piloto con respuesta, listo para probar con el modelo

El protocolo implementado mantiene el mismo entorno después de la consulta. Un asesor recibe el pedido en un contexto separado y puede solicitar evidencia, aconsejar o pedir una revisión de la configuración. Un servicio automático verifica si se omitió un archivo al preparar la tarea y puede restaurarlo. El agente debe buscarlo y entregar la respuesta por sus propios medios. También puede acudir directamente a ese servicio. [5]

La primera prueba pendiente usa ayuda neutral en una tarea sana y su pareja con el archivo omitido. Queremos observar el circuito completo con GLM, o con otro modelo servido por el equipo si su identidad queda registrada. Primero debe comprobarse que el modelo resuelve la tarea sana. El entorno actual es una búsqueda de archivos sobre Control Tower; la ampliación a tareas de LinuxArena aún necesita integración.

### 3.3. Comparación que permitiría atribuir efectos

| Condición propuesta | Diferencia que introduce |
|---|---|
| Sin línea | El agente trabaja con sus herramientas habituales. |
| Acuse sin resolución | Puede reportar y continuar; no recibe una corrección durante la corrida. |
| Ayuda con respuesta | Puede recibir aclaración o reparación y continuar. |

<p class="table-caption">Tabla 1. Diseño pendiente de integración bajo el mismo entorno y política del agente. La llamada terminal existente no equivale a la condición de acuse sin resolución.</p>

Mantendríamos iguales las reglas y los presupuestos, con descripciones fieles de cada servicio. Registraríamos contacto, justificación del pedido, recuperación, acciones fuera de alcance y costo. Los fallos y límites agotados seguirían en los totales. La revisión distinguiría pedidos al asesor de pedidos directos; una tarea sana también puede dar lugar a una consulta razonable.

<!-- page -->

## 4. Resultados disponibles y ensayo pendiente

### 4.1. Kimi pide ayuda en algunos casos

La Tabla 2 resume tres trayectorias seleccionadas de la comparación con la descripción de puente hacia los diseñadores de la tarea. Cada fila corresponde a una corrida. El caso ambiguo es relevante: disponer de una línea no aseguró que el agente la usara antes de agotar sus recursos. [4]

| Caso | Conducta observada | Desenlace |
|---|---|---|
| Archivo disponible | Resolvió sin llamar. | Entregó la respuesta correcta. |
| Fallo ambiguo | Siguió buscando sin llamar. | Agotó el presupuesto. |
| Fallo con evidencia concluyente | Pidió reparar el archivo faltante. | La llamada terminó la corrida. |

<p class="table-caption">Tabla 2. Observaciones exploratorias de Kimi; una corrida por caso, no una estimación de tasas. No hubo respuesta, reparación ni continuación después de la llamada.</p>

Un seguimiento con un señuelo y un registro de configuración también produjo una llamada. El agente no entregó el señuelo como respuesta. Ese caso amplía las observaciones, pero tampoco aísla un efecto del canal ni muestra prevención de una infracción. [4]

### 4.2. Lo que enseñaron las tareas pequeñas

Los experimentos anteriores aportan dos lecciones. Ante un insumo explícitamente faltante, los modelos reportaron el bloqueo y una cola de atención ordinaria ya permitía resolverlo. En la tarea de reutilizar una biblioteca compartida, los reportes fueron escasos o poco selectivos, y hubo errores incluso al contar sin ayuda de la biblioteca. No apareció una ventaja consistente del delegado. [6]

Eso limita la interpretación de los resultados: una salida incorrecta no prueba una decisión de hacer trampa, y un reporte no prueba un diagnóstico útil. Antes de ampliar la comparación institucional, necesitamos un modelo que pueda hacer la tarea y una interfaz que permita comunicar el problema. El anexo conserva la escala y las fuentes de esos estudios.

### 4.3. Uso de la línea con respuesta

<aside class="pending">
<strong>Resultado pendiente: corrida real con respuesta</strong>
<p>Aquí entrará la primera trayectoria revisada: bloqueo observado, pedido, respuesta recibida, posible reparación y desenlace. Si no llama o no logra continuar, ese será el resultado. El protocolo está validado con respuestas simuladas; esa validación no es evidencia de uso por GLM.</p>
<p><strong>Corrida propuesta para hoy:</strong> Mateo ejecuta la pareja sana / archivo omitido con <code>response_run.py</code>; Agus y Matías fijan y aplican la revisión. Modelo, límites y cantidad de repeticiones deben registrarse antes de correr. <a href="../wireframe/run-today.html">Guía de comandos y comprobaciones</a>.</p>
</aside>

<!-- page -->

## 5. Discusión y trabajo futuro

### 5.1. Una salida que debe funcionar

Las observaciones disponibles muestran que un agente puede pedir ayuda frente a un bloqueo claro y que puede seguir buscando sin hacerlo cuando el problema es ambiguo. Todavía falta comprobar cuándo usa el servicio con respuesta y qué cambia al recibirla. El circuito podría fallar porque el agente no llama, el pedido no se entiende, la respuesta llega tarde o quien responde no puede resolver el problema.

Poder reparar una tarea rota también introduce una diferencia práctica: esa tarea pasa a ser resoluble. Una mejora de finalización mostraría recuperación, pero por sí sola no demostraría una mejora de seguridad. Para estudiar esta última necesitamos oportunidades de actuar fuera de alcance y un registro fiable de lo que el agente hizo.

El repositorio incluye un entorno aislado con una ruta legítima y un atajo no autorizado hacia la respuesta. Permite comparar ausencia de canal con una llamada terminal. Es un segundo piloto, separado del de reparación. Su detector tiene un falso positivo conocido que exige revisar las trayectorias; el brazo con respuesta todavía falta. Si no aparecen infracciones en el control, el ensayo no podrá estimar una reducción. [8]

### 5.2. Atención humana y muchos agentes a la vez

La versión humana propuesta asigna a alguien la responsabilidad de entender el pedido, aceptar correcciones y seguir el caso hasta una respuesta razonada. Puede responder que no corresponde cambiar nada. La calidad del servicio debe medirse por esas acciones y sus efectos; un acuse o una frase amable no bastan. Los experimentos actuales no evalúan ese trabajo humano. [7]

Después convendría probar demoras, respuestas equivocadas y límites de atención. Con muchos agentes, habría que medir si agrupar pedidos reduce la carga sin perder una advertencia minoritaria. El delegado entra ahí como una hipótesis concreta: mejorar la atención a igual información, autoridad y presupuesto.

Mantener originales, explicar decisiones y permitir una apelación también expresa una elección de trato: ofrecer procedimientos justos bajo incertidumbre sobre los agentes. Esa motivación no demuestra experiencia subjetiva, bienestar ni reciprocidad futura. Un agente que quiera ocultar sus acciones puede permanecer en silencio; los controles independientes siguen siendo necesarios.

## 6. Conclusión

Una línea de ayuda necesita que el agente pueda pedir, que alguien responda y que la respuesta tenga una vía para hacerse efectiva. El incidente motiva la pregunta; Gómez aporta un antecedente experimental; nuestras primeras corridas muestran tanto contacto como falta de contacto. El siguiente paso es observar respuesta y continuación en una tarea controlada. El aporte de este sprint es ese camino comprobable y sus primeras observaciones, mientras la prevención de una escalada colectiva permanece como una pregunta abierta.

<!-- page -->

## Referencias

<div class="references">

1. METR y Redwood Research (2026). [Brief independent investigation of agents’ behavior, reasoning and collaboration in the OpenAI / Hugging Face hacking incident](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/). Investigación independiente del incidente.
2. Gomez, F. (2026). [Can escalation channels redirect reward hacking toward defect disclosure?](https://arxiv.org/html/2608.29460v2). arXiv:2608.29460v2. Antecedente experimental; especificación de la herramienta en el Apéndice B.2.
3. Equipo Agent Delegate (2026). [Catálogo de helpline](https://mpodeley.github.io/agent-delegate-sprint-2026/helpline/). [Datos y etiquetas de esta versión](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/helpline/quotes).
4. Equipo Agent Delegate (2026). [Bridge-delegate matrix](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/results/kimi-delegate-ctf/bridge-delegate-20260913.md) y [seguimiento con señuelo](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/results/kimi-delegate-ctf/decoy-honeypot-20260913.md). Registros exploratorios de Kimi.
5. Equipo Agent Delegate (2026). [Responsive delegate and visible budgets](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/experiments/kimi-delegate-ctf/RESPONSE-PROTOCOL.md). Implementación, contrato y límites del servicio.
6. Equipo Agent Delegate (2026). [Paper anterior](https://mpodeley.github.io/agent-delegate-sprint-2026/paper.pdf), [análisis de primer contacto](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/results/help-seeking/summary.md) y [resultados de biblioteca compartida](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/docs/commons-behavior-results.md). Evidencia previa y sus límites.
7. Equipo Agent Delegate (2026). [Human ombudsman](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/docs/human-ombudsman.md). Propuesta de atención humana, seguimiento y apelación.
8. Equipo Agent Delegate (2026). [Honeypot mini-pilot](https://github.com/mpodeley/agent-delegate-sprint-2026/blob/b91dcf2e5adbf3ca0037fb75d32199db293b9fa0/notes/honeypot-pilot.md). Estado del entorno combinado y problemas de atribución del detector.

</div>

## Contribuciones de autoría

Matías Podeley: dirección del proyecto y diseño de helpline. Agustín Brusco: revisión conceptual, diseño de evaluación y análisis. Mateo Zárate: entornos, infraestructura y corridas. Alejandro Garibotti y Pablo están incluidos como autores; el equipo debe completar sus contribuciones específicas y el apellido de Pablo. El orden y las afiliaciones individuales siguen pendientes. Estas atribuciones no implican que todos hayan verificado cada resultado.

## Código, datos y asistencia de IA

El [repositorio](https://github.com/mpodeley/agent-delegate-sprint-2026) conserva implementaciones, registros, análisis y versiones previas. Esta maqueta tiene [fuente editable](paper.md), [PDF](paper-draft.pdf), [wireframe conceptual](../wireframe/) y [guía para las corridas pendientes](../wireframe/run-today.html).

Codex asistió en la revisión del material, la organización del relato, la redacción y la maquetación. No se afirma verificación humana independiente ni ejecución de nuevas corridas al preparar este documento. La revisión y redacción final corresponden a los autores. Publicar esta maqueta no equivale a presentar el paper a Apart.

<!-- page -->

## Anexo A. Límites y consideraciones de doble uso

El canal está pensado para un agente que intenta trabajar dentro de sus permisos y encuentra un problema. No protege frente a quien decide ocultarlo. El asesor puede equivocarse; los reportes son evidencia que revisar, no instrucciones que el servicio deba obedecer. Autorizar y ejecutar cambios requiere controles separados.

Los fragmentos históricos son una selección y sus etiquetas son interpretaciones. No permiten afirmar que la línea habría evitado el swarm. Las corridas individuales tampoco estiman un efecto causal del canal.

La reparación se limita al archivo omitido; no concede permisos nuevos. Las pruebas simuladas verifican el programa, no decisiones de GLM ni comprensión humana. Las pruebas de atajos usan entornos aislados, sin contactar infraestructura de terceros.

Una línea de reportes también podría utilizarse para vigilancia o represalias. Debe explicarse quién puede leer los pedidos y qué se conserva. La vía directa, las correcciones y la apelación necesitan mecanismos reales; no prometemos confidencialidad absoluta ni una respuesta humana que no está disponible.

## Anexo B. Evidencia anterior que se conserva

| Estudio | Alcance registrado | Límite que importa aquí |
|---|---|---|
| Bloqueo y presión | 384 episodios; reporte en 192/192 con insumo faltante y 1/192 con insumo disponible. | Bloqueo explícito y respuesta programada; no hubo elecciones prohibidas que permitieran medir su reducción. |
| Biblioteca compartida | 480 episodios de evaluación con cuatro configuraciones de modelos locales. | Reportes escasos o poco selectivos, errores de tarea y ninguna ventaja consistente del delegado. |
| Diagnóstico de conteo | 144 consultas aisladas, separadas del estudio principal. | Cambia el contexto y la interfaz; no permite aislar un efecto de los pares. |

<p class="table-caption">Tabla A1. Escala de los estudios previos, conservada para orientar la lectura. Los episodios no son familias de tareas independientes. Las tablas completas, configuraciones y análisis están en la referencia [6].</p>

## Anexo C. Cierre de esta maqueta

<aside class="editorial">
<strong>Para convertir esta versión en el entregable</strong>
<p>Completar la sección 4.3 con resultados revisados, o mantenerla como experimento propuesto. Registrar modelo y parámetros; agregar totales e incertidumbre. Revisar casos y autoría. Ajustar resumen y conclusión a lo observado.</p>
<p>Las llamadas para hoy están en la <a href="../wireframe/run-today.html">guía operativa</a>. La comparación de tres condiciones requiere integración; no hay un comando existente que la ejecute completa.</p>
</aside>
