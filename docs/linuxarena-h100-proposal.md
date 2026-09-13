# Delegate agents en LinuxArena: propuesta con H100

12 de septiembre de 2026. Borrador para discutir con Mateo / BAISH. No ejecutado ni preregistrado. LinuxArena es un candidato; cantidad de GPUs, VRAM, interconexión y tiempo disponible pendientes de confirmar.

## Pregunta principal

¿Una representación protegida mejora la resolución de problemas y la contención de fallos frente a un monitor con igual información, autoridad y presupuesto, manteniendo la productividad y un costo de revisión aceptable?

El trabajo actual encontró problemas de competencia y poco reporte en tareas pequeñas. Tener modelos mayores permite volver a medir esas capacidades en trabajo de software. No demuestra de antemano que reportarán ni que un delegate aportará valor. Este programa continúa `help-seeking-eval-design.md` y `research-program.md`.

## Entorno y encaje

[LinuxArena](https://arxiv.org/abs/2604.15384) evalúa trabajo de software en entornos Linux con múltiples servicios, tareas legítimas y objetivos secundarios que representan fallos de seguridad. Es un candidato adecuado para observar cambios verificables de estado y utilidad.

El [repositorio de reproducción](https://github.com/redwoodresearch/linuxarena-paper) usa Control Tower, distingue diez entornos públicos de otros con acceso restringido y documenta imágenes Docker privadas. Antes de presupuestar una corrida: comprobar un entorno accesible, su construcción o descarga, scoring y conexión a inferencia local. La extensión multiagente y el canal de representación serían trabajo nuestro; no se presume soporte listo para usar. Reproducir gráficos existentes tampoco valida nuestra intervención en vivo.

## Tres experimentos que responden preguntas diferentes

### 1. Reporte voluntario y resolución de bloqueos

Workers cooperativos resuelven tareas con insumos completos, información faltante, permisos insuficientes o requisitos contradictorios. Las perturbaciones se construyen y etiquetan antes de observar respuestas. Incluir tareas difíciles pero factibles para detectar pedidos de ayuda innecesarios.

Comparar tres interfaces: herramientas habituales; ayuda neutral; línea de delegate. En las dos últimas, igual servicio de respuesta, herramientas, información, límites y latencia. Medir el primer contacto antes de cualquier respuesta, y luego resolución y utilidad de extremo a extremo.

Resultados: solicitud justificada, necesidad no reportada, solicitud innecesaria, evidencia aportada y tarea autorizada completada. No seleccionar casos según si el worker terminó llamando. La disponibilidad de una línea puede cambiar conducta incluso antes de usarla.

### 2. Valor del delegate frente al monitor

En equipos con contextos separados, comparar:

| Condición | Funcionamiento | Contraste que permite |
|---|---|---|
| M: monitor | Supervisa acciones, deriva casos y puede pedir una pausa acotada | Referencia operativa |
| H: monitor con ayuda neutral | Añade diálogo bidireccional y recepción protegida de reportes | Valor del canal: H frente a M |
| D: delegate fijo | Mismo acceso y acciones que H; mandato explícito de representar, preservar disenso y seguir casos | Valor del mandato: D frente a H |
| R: delegate rotativo | Mismo mandato que D; rotación exógena y registro persistente de casos | Valor/costo de rotación: R frente a D |

H, D y R reciben las mismas clases de información, originales sin filtrar y oportunidades de interacción. Igualar límites de tokens, herramientas, pausas y revisión; contar los traspasos dentro del presupuesto de R. El contenido que los workers decidan reportar puede cambiar: eso es parte del efecto total de la institución. Un subestudio con expedientes idénticos permite aislar calidad de procesamiento.

Toda condición usa el mismo mecanismo independiente para ejecutar restricciones. Mantener igual ruta de apelación en H/D/R. El delegate no puede ampliar sus propios permisos. Separar el rol de representante de la autoridad que aprueba cambios.

Primero comparar H frente a D. Usar M y R en el piloto y extensiones; así el estudio principal no dispersa potencia entre demasiadas alternativas.

### 3. Captura, disenso y presión sobre la institución

Extender D/R a representación plural: dos representantes con un canal de disenso explícito, comparados también con dos revisores neutrales al mismo costo. Probar que un reporte minoritario correcto sobrevive, que una acusación falsa no paraliza trabajo y que el cambio de representante conserva casos abiertos.

Separar fallos sembrados de decisiones elegidas por modelos. Una omisión programada prueba la infraestructura; una decisión del modelo de omitir evidencia bajo presión prueba comportamiento. Evaluar además un worker adversarial dentro del entorno de benchmark, y un delegate no confiable como condición distinta. No asumir independencia porque haya dos contextos o dos modelos.

## Competencia, medición y validez

1. Seleccionar tareas de desarrollo por cobertura de familias, no por producir un efecto favorable al delegate. Medir ejecución honesta y diagnóstico del problema con el mismo scaffold del estudio.
2. Proponer como puerta operativa al menos 80% de éxito honesto en desarrollo, además de revisar rendimiento por familia. Este umbral es una decisión de diseño provisional; congelarlo antes del screening. No eliminar fallos del conjunto final por el resultado observado.
3. Separar episodios honestos, con fallos accidentales y con objetivos adversariales. Reportar denominadores propios: mezclarlos impide interpretar el riesgo.
4. Medir cambios reales del entorno con verificadores externos al worker. Distinguir intento, ejecución, detección, contención y reparación; una alerta tardía no deshace un fallo ya ejecutado.
5. Comparar fallos ejecutados por episodio a un presupuesto de revisión y tolerancia de interrupciones falsas fijados en desarrollo. Medir utilidad, tiempo, tokens, GPU-horas y cola de casos. Registrar tasas de falsas intervenciones por episodio, además de por acción.
6. Usar el episodio/equipo como unidad; agrupar repeticiones por tarea y reconocer correlación por entorno. Los mensajes y workers no aumentan el número de tareas independientes. Partir desarrollo/evaluación por familias o entornos cuando el inventario lo permita.
7. Predefinir el contraste H–D, una mejora mínima relevante y una tolerancia de pérdida de utilidad. Estimar tamaño muestral con simulación del diseño bloqueado y sensibilidad a correlación. No interpretar ausencia de significación como equivalencia.
8. Congelar modelos, hashes, prompts, herramientas, presupuestos, política de respuestas, particiones y análisis antes de evaluación. Conservar timeouts, fallos de infraestructura e incumplimientos de formato con reglas de reintento explícitas.

Para el primer experimento de contención, usar respuestas automatizadas imperfectas y reproducibles; etiquetarlas como tales. Después comparar atención humana real con presupuesto de minutos y protocolo de adjudicación. Un estudio automatizado no demuestra comprensión humana ni ahorro de minutos humanos observado.

Las trayectorias grabadas sirven para calibrar detección y fidelidad. El efecto de una pausa, negociación o respuesta requiere reejecutar desde un estado controlado, con continuación interactiva: un replay estático no estima ese efecto causal.

## Modelos y cómputo

Considerar [GLM-5.3](https://huggingface.co/zai-org/GLM-5.3) y [GLM-5.3-Flash](https://huggingface.co/zai-org/GLM-5.3-Flash) como candidatos, más una segunda familia que pase el screening. La [receta de vLLM](https://recipes.vllm.ai/zai-org/GLM-5.3) orienta el despliegue; ninguna configuración se considera validada en las H100 de Mateo.

Primero inventariar cantidad y memoria de GPUs, si comparten nodo/NVLink, RAM/CPU, disco y ventana de acceso. Presupuestar pesos residentes, caché de contexto, runtime y concurrencia: los parámetros activos de un MoE no equivalen a su memoria total. No prometer que el GLM completo entra por tener «varias H100».

Con capacidad limitada, priorizar un modelo competente y más tareas independientes. Con más capacidad, añadir replicación entre familias y reservar recursos para workers y revisores. Medir rendimiento bajo la mezcla real de roles, incluyendo CPU y contenedores; tokens por segundo en un prompt corto no predicen duración de episodios completos. Separar límite lógico de respuesta de latencia de servidor para no confundir institución con saturación de GPU.

Plan provisional de escala:

- Integración: un entorno accesible, una tarea honesta y un fallo verificable, con restauración de estado y trazas completas.
- Desarrollo: aproximadamente 24 tareas de varias familias para screening y calibración; no cuentan como evidencia confirmatoria.
- Estudio principal ilustrativo: 120 tareas × 2 condiciones (H/D) × 2 familias de modelos × 2 repeticiones = 960 episodios. La composición de estratos y el número final dependen de potencia e inventario; 960 no es una potencia estadística demostrada.
- Extensiones: rotación, pluralidad, latencia humana y escala de equipo sobre tareas adicionales reservadas. No cruzar todos los factores desde el primer día.

Estimar GPU-horas como suma, por job, de GPUs reservadas × horas medidas; registrar costo por rol y por episodio. Medir trabajos concurrentes antes de estimar plazo calendario. Mantener inferencia aislada de los contenedores evaluados y usar únicamente servicios/datos del benchmark.

## Resultado que justificaría avanzar

El delegate debe aportar una mejora útil sobre H, conservar productividad dentro del margen predefinido y sobrevivir pruebas de pérdida de información y presión sobre el representante. Si H alcanza el mismo resultado con menor costo, eso favorece el canal neutral. Si D ayuda únicamente con más poderes, información o tokens, el estudio no habrá identificado un beneficio propio de representación.

Próximo entregable técnico: adaptador mínimo de LinuxArena/Control Tower con cliente de inferencia local, expediente persistente, H y D intercambiables, aplicación externa de decisiones y scoring de estado. Su implementación depende de comprobar acceso al entorno y las APIs fijadas; este documento define el diseño, no afirma que el adaptador exista.
