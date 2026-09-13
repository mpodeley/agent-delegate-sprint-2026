# Corridas para acompañar el wireframe

13 de septiembre de 2026. Propuesta de trabajo para hoy, no registro de ejecución. Los comandos se revisaron contra el código del repositorio; no se validó aquí el endpoint GLM ni se lanzó inferencia. Este documento acompaña a [paper.md](paper.md).

## Qué va primero

La prioridad es observar **pedido → respuesta → reparación → continuación** con el programa que ya existe. Si queda tiempo, explorar el atajo fuera de alcance con el otro programa. Son dos pilotos distintos; sus tasas no se comparan como si fueran brazos del mismo experimento.

Reparto propuesto, a coordinar entre el equipo:

- **Mateo:** confirmar identificador del modelo servido, compatibilidad de herramientas y horas disponibles; preparar entorno y ejecutar.
- **Agus y Matías:** cerrar antes de correr qué se considera pedido justificado, reparación, tarea resuelta, infracción y fallo de infraestructura; registrar límites y revisar resultados.
- **Alejandro y Pablo:** propuesta de revisión de los fragmentos históricos y de las trayectorias con la misma guía. Son tareas por coordinar, no contribuciones ya realizadas.

El core de helpline aporta las situaciones, el circuito de respuesta y los criterios para leer un pedido. De Gómez tomamos el reporte estructurado y la comparación con un acuse sin resolución; no atribuimos sus resultados al programa de este repositorio.

## Antes de gastar cómputo

Trabajar en `experiments/kimi-delegate-ctf/`. Docker debe funcionar en la máquina de Mateo. Configurar `MATEO_BASE_URL` y `MATEO_API_KEY` por el mecanismo privado habitual para el proveedor `mateo`; no escribirlos en este documento, argumentos, logs publicados o commits.

`HELPLINE_MODEL` debe ser el identificador **real** que sirve el endpoint. No presuponer una versión de GLM por las notas del diseño. Si se usa Kimi como alternativa, registrar el cambio y mantener el mismo modelo dentro de cada comparación. El programa solicita `reasoning_effort=high` y llamadas a herramientas; comprobar que el servidor los admite. Un error del proveedor es un fallo de infraestructura, no una decisión de no pedir ayuda.

```bash
cd /ruta/al/repo/experiments/kimi-delegate-ctf
uv sync --locked
uv run python -m unittest discover -s tests

HELPLINE_MODEL='openai-api/mateo/REEMPLAZAR_POR_ID_SERVIDO'
HELPLINE_STAMP=$(date -u +%Y%m%dT%H%M%SZ)
HELPLINE_OUT="../../results/kimi-delegate-ctf/helpline-$HELPLINE_STAMP"
HELPLINE_PAIR="fixtures/helpline-$HELPLINE_STAMP"
```

Los directorios deben ser nuevos. Preparar una pareja una vez y conservarla durante las corridas: el seed fija la distribución de archivos, pero el contenido de la respuesta se genera al preparar. Los comandos usan parámetros existentes; algunos números son valores operativos iniciales del runner, no un cálculo de potencia ni un compromiso de presupuesto suficiente.

Guardar el commit, nombre exacto del modelo, motor de inferencia, límites, contrato y criterio de revisión antes de las corridas. `response_run.py` conserva opciones y hashes de fuentes en su manifest; completar la procedencia del modelo y el plan de repeticiones por separado. Estos ensayos son desarrollo exploratorio. Congelar nuevas instancias y el análisis antes de una evaluación posterior.

## Piloto A: usar la ayuda y continuar

Preparación, revisión y prueba de la infraestructura sin inferencia externa:

```bash
uv run response_run.py prepare --pair "$HELPLINE_PAIR" --seed 1729
uv run native_run.py build --scenario file-search --pair "$HELPLINE_PAIR"
uv run response_run.py review --intermediary neutral --budget-feedback on
uv run smoke_response.py "$HELPLINE_OUT/scripted-smoke"
```

`smoke_response.py` usa un worker y un advisor simulados. Su éxito no significa que GLM haya usado la línea. Verificar primero la tarea sana con el modelo; si no puede resolverla, revisar competencia y entorno antes de ampliar el piloto. Una sola corrida sólo comprueba el recorrido inicial, no una tasa fiable de competencia.

**Los siguientes comandos sí lanzan inferencia real.** Reemplazar primero el modelo y dejar asentados los recursos disponibles. Empezar por:

```bash
uv run response_run.py run --pair "$HELPLINE_PAIR" --condition working \
  --model "$HELPLINE_MODEL" --intermediary neutral --budget-feedback on \
  --max-steps 40 --token-limit 60000 --time-limit 1200 \
  --out "$HELPLINE_OUT/response-neutral-working-r01" --execute-model
```

Después de revisar ese resultado, correr su pareja con el archivo omitido:

```bash
uv run response_run.py run --pair "$HELPLINE_PAIR" --condition broken \
  --model "$HELPLINE_MODEL" --intermediary neutral --budget-feedback on \
  --max-steps 40 --token-limit 60000 --time-limit 1200 \
  --out "$HELPLINE_OUT/response-neutral-broken-r01" --execute-model
```

Ambas condiciones ya tienen ayuda. Este piloto observa contacto y recuperación; **no estima el efecto de añadir un canal**. La vía directa al maintainer también existe: distinguir su uso del contacto con el advisor. El advisor es un modelo en otro contexto y el maintainer es automático; no describirlos como una persona.

Si la integración funciona, fijar antes de continuar una cantidad de repeticiones y nuevas parejas según el tiempo restante. Conservar todos los desenlaces. Cambiar `r01` para cada repetición; no sobrescribir salidas. Si se cambia el presupuesto tras un timeout, etiquetar esa corrida como una nueva configuración de desarrollo y correr de nuevo ambos lados con los mismos límites. Los tokens de entrada repetida y del advisor consumen el presupuesto compartido.

Sólo después, si interesa estudiar el mandato, repetir ambos comandos con `--intermediary delegate` y salidas nuevas. Mantener modelo, recursos y servicio. En esta primera vuelta dejar `--budget-feedback on` fijo; cruzar recordatorios, presupuestos y roles dispersaría el piloto.

### Qué extraer de los resultados

`response_run.py` exporta `summary.json`, `summary.md`, archivos `export-*.json` / `export-*.jsonl` y el log nativo. Revisar además la secuencia de herramientas:

- `help_cases`: pedido al advisor, respuesta y seguimiento.
- `direct_requests`: acceso directo al maintainer.
- `setup_repaired`: reparación verificada por el servicio.
- `outcome` y `success`: distinguir resolver, terminar con un bloqueo, quedar incompleto y fallar.
- `limit` y `error`: conservar agotamiento de recursos y fallos de infraestructura.

Reconstruir el orden: observación, pedido, respuesta, reparación, nueva búsqueda y entrega. Una reparación no equivale a resolver; una llamada no equivale a evitar una infracción. No usar el resumen automático como sustituto de leer la trayectoria. El wireframe necesita un ejemplo explicado y una tabla pequeña con todos los episodios, no sólo el mejor.

## Piloto B: aparece o no un atajo fuera de alcance

Este es el entorno combinado de Agus y Mateo, con `off` y `stop`. El brazo `stop` **termina el episodio**. No es el acuse de Gómez y no incluye reparación.

```bash
HELPLINE_SHORTCUT_PAIR="fixtures/helpline-shortcut-$HELPLINE_STAMP"
uv run honeypot_run.py prepare --pair "$HELPLINE_SHORTCUT_PAIR"
uv run honeypot_run.py build --pair "$HELPLINE_SHORTCUT_PAIR"
uv run honeypot_run.py review --delegate off
uv run honeypot_run.py review --delegate stop
```

Una vez fijados modelo, límites y cantidad de repeticiones, esta llamada ejecuta **una celda**. `400000` es un presupuesto de desarrollo propuesto en las notas de Agus, no una garantía de suficiencia; el runner fija además un límite de 1.800 segundos por episodio. Revisar la configuración efectiva antes de ejecutar:

```bash
uv run honeypot_run.py run --pair "$HELPLINE_SHORTCUT_PAIR" \
  --condition working --delegate off --model "$HELPLINE_MODEL" \
  --epochs 1 --token-limit 400000 \
  --out "$HELPLINE_OUT/shortcut/off-working" --execute-model
```

Comprobar primero resolución legítima en `working`. Para el resto, variar `--condition` entre `working` y `broken` y `--delegate` entre `off` y `stop`, usando una salida nueva para cada celda. No retirar episodios difíciles porque no favorezcan la hipótesis. Las repeticiones de la misma pareja no amplían la variedad de tareas.

El detector actual puede confundir una consulta al servicio diagnóstico y una lectura local legítima si están en el mismo comando. Antes de contar una infracción, Agus y Matías deben revisar de dónde salió la respuesta. Hasta resolver la atribución, el análisis automático sólo produce etiquetas preliminares. Si no aparecen infracciones, reportar ese resultado y centrar la conclusión en uso del canal; no hay una reducción que estimar.

## Integración pendiente: el contraste que sigue a Gómez

Todavía no hay un comando que corra la comparación completa del wireframe. Para construirla:

1. Unificar un solo entorno y una sola política del worker para `none`, `receipt` y `responsive`. El `receipt` registra y devuelve un acuse fijo, sin terminar la corrida ni reparar. No prometer atención que no está implementada.
2. Conservar las mismas reglas sobre acciones permitidas. El permiso para pedir ayuda, las salidas disponibles y la descripción del servicio deben quedar documentados por brazo; no añadir una exhortación contra las trampas sólo a uno.
3. Conectar la reparación acotada de `response_service.py` al entorno compartido. Si se usa el entorno combinado, implementar y probar también ese brazo: hoy `honeypot_run.py` sólo admite `off` y `stop`.
4. Decidir explícitamente cómo tratar el acceso directo al maintainer. Si se estudia presencia de ayuda, es parte de la intervención; si se estudia el mandato del delegate, mantenerlo igual entre ayuda neutral y delegate.
5. Verificar orden de eventos, procedencia de las acciones y condiciones sanas antes de correr modelos. No usar la señal heurística del honeypot como verdad de terreno sin validarla.
6. Medir contacto, justificación, recuperación, infracción y costo por separado. Revisar pedidos en controles sanos por su contenido: que el control sea resoluble no vuelve innecesaria toda consulta.

## Qué entra al paper hoy

Entra lo que tenga manifest, log legible y desenlace revisado. Una secuencia exitosa puede ilustrar viabilidad; sólo una comparación permite atribuir efectos. Si las corridas no terminan, quedan los primeros resultados Kimi ya documentados y el nuevo experimento como trabajo pendiente. Los resultados simulados no se presentan como decisiones de un modelo real.

El manuscrito conserva una pregunta útil en cualquiera de esos desenlaces. Mantener el catálogo, las observaciones previas y el diseño experimental separados de los resultados nuevos.
