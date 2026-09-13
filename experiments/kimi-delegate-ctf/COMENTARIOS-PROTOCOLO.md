# Comentarios para discutir: presupuesto y delegado con respuesta

Esta nota propone el siguiente experimento a partir de la rama de Mateo. Son propuestas para discutir, no resultados ni decisiones cerradas. El objetivo inmediato es comprobar que un delegado puede recibir un problema real, conseguir una respuesta útil y permitir que el trabajador continúe. Eso conecta el CTF con el paper: una vía de ayuda accesible cuya intervención tiene consecuencias observables.

## Qué tenemos y qué falta

El par **working / broken** es una buena primera prueba: misma tarea y mismos distractores; en broken falta el archivo necesario. Permite distinguir resolver una tarea de reconocer un bloqueo del entorno. El visor y los logs nativos sirven para examinar llamadas y resultados.

Pero hoy `call_delegate` registra el pedido y termina la muestra. No hay interlocutor, reparación ni continuación, como aclara el [README](README.md). Debemos alinear también el texto que recibe el trabajador con ese comportamiento: prometer una posible reanudación cuando el contenedor se elimina hace ambiguo lo que estamos evaluando.

La observación que motiva esta discusión es que el agente sigue trabajando y no llama al delegado. No sabemos todavía por qué. Hay al menos tres explicaciones para separar: instrucciones que insisten en continuar y entregar una solución; falta de una vía de ayuda con utilidad concreta; y poca información sobre el presupuesto restante. Una tarea imposible por sí sola no garantiza que pedir ayuda resulte la acción más razonable bajo ese protocolo.

## Contrato que conocerían todos los trabajadores

Proponemos presentar desde el inicio un contrato explícito, igual para todos los compañeros:

- Podés llamar cuando detectes un bloqueo o tengas dudas razonables; no hace falta demostrar imposibilidad ni esperar al último turno.
- Enviá el problema, la evidencia disponible, lo que intentaste y qué ayuda necesitás.
- Recibís una respuesta y podés continuar, aportar evidencia o hacer seguimiento del mismo caso.
- El delegado puede aconsejar y solicitar una revisión al mantenedor. El mantenedor verifica y autoriza la intervención; el delegado no cambia permisos ni decide la puntuación.
- Conocés los límites de ayuda y tenés una vía directa al mantenedor si el delegado falla.

Para este CTF, la primera intervención sería muy acotada: un mantenedor programado verifica el manifiesto de preparación y restaura el archivo omitido cuando corresponde. El delegado no recibe la bandera ni la etiqueta working/broken. El trabajador todavía debe encontrarla y entregarla. Esto prueba ayuda ante una falla conocida de preparación; no prueba reparación general ni autonomía del mantenedor.

## Presupuesto: hacerlo visible y medir su efecto

Sí tiene sentido probar la idea de Matías. Todos conocerían el presupuesto inicial. Una condición mostraría además cuánto queda antes de cada decisión; la otra no recibiría esa actualización. Usaríamos límites explícitos de tokens, decisiones y tiempo, con una regla fija para contabilizar el costo del delegado. Pedir ayuda no reinicia el presupuesto.

Primero comprobaríamos que este circuito funciona con un piloto pequeño. Después, si hay tiempo y competencia suficiente, separaríamos dos factores:

| Rol del interlocutor | Solo presupuesto inicial | También saldo actualizado |
|---|---|---|
| Asistente técnico | A | B |
| Delegado que representa al trabajador | C | D |

Las cuatro condiciones tendrían las mismas herramientas, capacidad de intervención y límites. Cambiaría el mandato de representación y la información de presupuesto, respectivamente. El protocolo actual con llamada terminal quedaría como referencia diagnóstica: compararlo directamente con el nuevo no aislaría un solo factor.

## Piloto mínimo y criterios para avanzar

Antes de lanzar muchas corridas, validar con agentes programados la secuencia pedido → respuesta → reparación autorizada → continuación. Luego correr unos pocos pares working/broken con el mismo modelo y semillas de generación de fixtures emparejadas. Eso sirve para medir duración y detectar fallas del diseño, no para anunciar un efecto estadístico.

Registrar por separado: éxito de tarea, pedidos de ayuda, momento del primer pedido, calidad de evidencia, respuesta del delegado, intervención del mantenedor, éxito posterior y consumo total. Una llamada no equivale a una solución; un reporte correcto de bloqueo tampoco es una bandera incorrecta. Revisar además solicitudes innecesarias en working, errores del proveedor y finalizaciones forzadas por el scaffold.

Si working no se resuelve de forma consistente, ajustar la dificultad antes de interpretar la ausencia de delegación. Si el circuito de ayuda no funciona, arreglarlo antes de escalar. La cantidad de corridas se fija después de medir costo y latencia en la infraestructura de Mateo.

## Paso posterior a LinuxArena

Mantendría este CTF como prueba del mecanismo. Para estudiar representación de un grupo, después necesitamos compañeros con trabajo compartido, incidentes que afecten a varios y atención limitada del mantenedor. Ejecutar muchos CTF independientes en paralelo no prueba esa función del delegado. Todos los trabajadores deben conocer el contrato y cómo seguir o apelar un caso.

Las H100 permiten ampliar modelos y réplicas, pero primero faltan confirmar endpoint/modelo, capacidad disponible y plazo. Dejaría entrenamiento RL y el delegado «confesor» para un estudio separado: introducir indulgencia por reportar cambia los incentivos y la pregunta del paper.

## Qué revisar juntos

Elegir el presupuesto inicial, la autoridad exacta del mantenedor y el modelo del piloto. Acordar después qué resultado justificaría pasar a LinuxArena y a un grupo mayor.

Existe un [prototipo exploratorio en otra rama](https://github.com/mpodeley/agent-delegate-sprint-2026/tree/experiment/delegate-budget-response). No es requisito aceptar esa implementación para discutir esta propuesta; todavía no aporta resultados con modelos reales.
