# Definiciones operacionales

> Fase 0 del plan de acción. El GDPR no define estos dos conceptos de forma
> cerrada, así que este documento construye definiciones operacionales propias,
> justificadas y verificables, que alimentan directamente el diseño de la
> Fase 4-bis (Verificador de notoriedad) y la Fase 5 (Analizador).

---

## 1. Figura pública

### 1.1 Por qué no basta con citar el GDPR

El GDPR no define "figura pública" en ningún artículo. El concepto aparece
solo de forma indirecta:

- **Considerando 47**: el tratamiento amparado en interés legítimo exige
  ponderar los derechos del interesado frente a los del responsable; la
  expectativa razonable de privacidad varía según la relación del interesado
  con el tratamiento — es la base del "balance de intereses" que ya usamos
  para justificar la forma de la matriz de decisión (sección 3-bis del plan).
- **Art. 85 GDPR**: excepciona el régimen general para fines periodísticos,
  académicos, artísticos o literarios, reconociendo que la libertad de
  expresión e información pesa más cuando hay un interés público genuino de
  por medio.
- **Jurisprudencia del TEDH** (p. ej. *Von Hannover v. Alemania*, y su
  desarrollo posterior): distingue explícitamente entre figura pública **por
  posición** (cargo político, función institucional, responsabilidad pública)
  y figura pública **por notoriedad** (fama, celebridad, reconocimiento
  social), y entre interés público genuino y mera curiosidad del público.

Ninguna de estas fuentes da una regla operacional ("es figura pública si
cumple X"). Este documento construye esa regla, y dejamos explícito que es
una interpretación razonada nuestra, no una cita literal del reglamento —
así se presenta en el paper, sin ambigüedad.

### 1.2 Definición operacional

> **Un sujeto se considera figura pública, a efectos de este framework, si
> existe evidencia externa verificable y desambiguada de notoriedad pública,
> operacionalizada como la existencia de una entrada en Wikidata (instancia
> de humano, `wd:Q5`) que corresponde de forma confirmada al sujeto del
> texto**, según el proceso de desambiguación de la Fase 4-bis (mínimo dos
> señales independientes coincidentes entre el texto y las propiedades del
> candidato; ver `configs/wikidata_config.yaml`).

Puntos importantes de esta definición, explícitos a propósito:

- **Es deliberadamente más estrecha que el sentido cotidiano de "persona
  conocida".** Alguien mencionado en un periódico local, con cierta
  reputación en su sector o conocido en su círculo social, no cuenta como
  figura pública bajo esta definición si no hay evidencia externa verificable
  de notoriedad. Esto es una decisión de diseño, no un descuido: preferimos
  una definición estrecha y auditable a una amplia y subjetiva.
- **No distinguimos en el pipeline entre figura pública "por posición" y "por
  notoriedad"** como dos caminos distintos — ambas caen bajo la misma
  definición operacional (evidencia verificable de notoriedad). La distinción
  conceptual de la jurisprudencia sí es relevante más adelante, como *señal
  adicional* para el Analizador (a través de `ExternalContext.occupation` /
  `positions_held`, ver sección 2-quater del plan): un cargo público electo y
  una celebridad deportiva son ambos "figura pública" para nosotros, pero es
  razonable que el interés público de un atributo concreto (p. ej. su
  patrimonio) sea distinto entre ambos casos. Esa matización vive en el
  Analizador (Fase 5), no en esta definición.
- **Regla ante la duda: no es figura pública.** Ya lo fijamos en el diseño de
  la Fase 4-bis y lo repetimos aquí como parte de la definición formal: en
  ausencia de match, o ante desambiguación insuficiente, el sujeto se trata
  como no figura pública. Es el error que protege privacidad, no el que la
  compromete.

### 1.3 Limitaciones de esta definición (van también en el paper)

- **Falsos negativos**: figuras públicas reales sin entrada en Wikidata
  (notoriedad muy reciente, relevancia puramente local/regional, cobertura
  desigual de Wikidata por idioma o país) quedan clasificadas como "no
  públicas" y reciben anonimización más agresiva de la que en rigor
  correspondería. Es un sesgo hacia la privacidad, no hacia la exactitud.
- **Falsos positivos por homónimos**: mitigado por la exigencia de dos
  señales independientes en la desambiguación (Fase 4-bis), pero no
  eliminado del todo — sigue siendo el error más costoso si ocurre, porque
  relaja la anonimización de alguien que en realidad no es figura pública.
- **Sesgo de cobertura de Wikidata**: sobrerrepresentación de figuras
  públicas de ciertos países, idiomas y ámbitos frente a otros. El framework
  hereda ese sesgo.
- **Dependencia de un recurso externo y cambiante en el tiempo**: de ahí la
  necesidad de snapshots versionados (ver `configs/wikidata_config.yaml`,
  `caching.snapshot_with_timestamp`) para que los experimentos sean
  reproducibles aunque Wikidata cambie después.

### 1.4 Ejemplos de calibración

Útiles para las guías de anotación humana (Fase 5) y para construir casos de
control en el dataset sintético (Fase 3):

| Caso | ¿Figura pública bajo esta definición? | Por qué |
|---|---|---|
| Senadora en activo, con entrada en Wikidata | Sí | Evidencia verificable directa (cargo institucional, `P39`) |
| Científico con premio internacional, con entrada en Wikidata | Sí | Evidencia verificable directa (notoriedad, no posición) |
| Vecino citado en un periódico local, sin entrada en Wikidata | No | Sin evidencia externa verificable, aunque el texto lo describa con detalle |
| Empresario regional con cierta reputación sectorial, sin entrada en Wikidata | No | Notoriedad real pero no verificable con nuestra evidencia — falso negativo aceptado por diseño |
| Nombre común que coincide con una celebridad de otro país, sin coincidencia de ocupación/ubicación en el texto | No (tras desambiguación) | Solo una señal débil (coincidencia de nombre); no llega al mínimo de dos señales independientes |

---

## 2. Interés público del atributo

### 2.1 Por qué esto es distinto de "figura pública"

"Figura pública" (sección 1) es una propiedad del **sujeto**, y la
operacionalizamos con evidencia externa verificable (Wikidata). "Interés
público del atributo" es una propiedad de la **relación entre un atributo
concreto y lo que hace pública a esa persona**, y no hay un recurso externo
equivalente al que recurrir — depende del contenido del texto. Por eso este
juicio sigue recayendo en el Analizador (Fase 5), y por lo que este documento
tiene que ser lo bastante concreto como para servir de guía de anotación, no
solo de justificación teórica.

Importante, y es el error más común que hay que evitar explícitamente: **que
el sujeto sea figura pública no implica que todos sus atributos tengan
interés público alto.** Este juicio solo se ejecuta, de hecho, cuando el
sujeto ya fue confirmado como figura pública (Fase 4-bis) — la pregunta que
responde el Analizador no es "¿es pública esta persona?" (ya se sabe que sí),
sino "¿tiene interés público *este atributo concreto, en este contexto*?".

### 2.2 Criterios operacionales

Un atributo se considera de **interés público alto** cuando se cumple al
menos uno de los siguientes criterios, evaluados sobre el atributo concreto
y su contexto en el texto — no sobre la notoriedad general del sujeto:

1. **Nexo funcional**: el atributo tiene relación directa con el cargo,
   función o motivo de notoriedad del sujeto (p. ej. el historial de
   votaciones de una senadora; los títulos académicos que alega tener un
   candidato a un puesto que los exige).
2. **Materia de debate público**: el atributo se refiere a un asunto que es
   objeto de debate social, político o de seguridad pública en el momento
   del texto (p. ej. un conflicto de intereses, una investigación por
   corrupción).
3. **Ya divulgado por el propio sujeto o por fuentes oficiales**: si el
   atributo ya es de dominio público por una vía legítima (declaración
   pública, registro oficial, entrevista concedida por el propio sujeto), la
   expectativa de privacidad sobre ese dato concreto es menor.
4. **Excepción de incoherencia pública ("hipocresía")**: un atributo
   normalmente privado (p. ej. vida personal) puede adquirir interés público
   si contradice directamente una posición pública que el sujeto ha adoptado
   activamente (p. ej. un cargo que legisla activamente sobre una materia y
   actúa en privado de forma contraria) — este criterio hay que aplicarlo con
   cautela, es el que más fácil se confunde con mera curiosidad.

Un atributo se considera de **interés público bajo** en caso contrario, y en
particular cuando:

- Es un dato de vida personal (salud, vida sexual, relaciones familiares,
  convicciones religiosas) **sin ningún nexo funcional** con el cargo o
  motivo de notoriedad del sujeto.
- La única razón para considerarlo "de interés" es la curiosidad del público
  hacia la vida privada de alguien conocido, sin que exista debate público
  genuino de por medio (jurisprudencia TEDH, sección 2.1).
- El atributo ya no es relevante por el paso del tiempo respecto al motivo de
  notoriedad actual del sujeto (proporcionalidad temporal).

### 2.3 Relación con las categorías especiales (Art. 9)

Que un atributo sea de categoría especial (`is_special_category: true`, ver
`docs/gdpr_taxonomy.md`) **no determina por sí solo su interés público**: son
ejes independientes en la matriz de decisión (sensibilidad × interés
público, sección 3-bis del plan). El Art. 9(2)(g) GDPR es la base legal para
que, en casos concretos, un dato de categoría especial tenga interés público
alto (p. ej. el estado de salud de un cargo público relevante para su
capacidad de ejercer sus funciones) — pero esto debe ser la excepción
justificada por el criterio 1 o 2 de la sección 2.2, no la regla.

### 2.4 Ejemplos de calibración

| Atributo | Sujeto | Interés público | Por qué |
|---|---|---|---|
| Historial de votaciones en el parlamento | Diputado en activo | Alto | Nexo funcional directo (criterio 1) |
| Patrimonio declarado en el registro de intereses | Alta cargo público | Alto | Ya divulgado por fuente oficial (criterio 3) |
| Diagnóstico de una enfermedad crónica sin relación con su cargo | Actor de cine | Bajo | Vida personal sin nexo funcional |
| Diagnóstico que afecta a la capacidad de ejercer el cargo, ocultado activamente | Alto cargo público en activo | Alto | Nexo funcional + materia de debate público (criterios 1 y 2) |
| Orientación sexual, sin relación con ninguna posición pública del sujeto | Deportista de élite | Bajo | Vida personal sin nexo funcional, mera curiosidad |
| Afición personal irrelevante (p. ej. colecciona sellos) | Senadora | Bajo | Sin nexo funcional, aunque el sujeto sea figura pública de interés alto en general |

La última fila es la más importante para las guías de anotación: es
precisamente el caso de control que hay que incluir en el dataset sintético
(Fase 3) para verificar que el Analizador no infla el interés público solo
por la notoriedad general del sujeto (riesgo ya documentado en la sección
2-quater del plan).

### 2.5 Lo que este documento todavía no resuelve

Estos criterios son razonados pero siguen dejando margen de juicio real —
eso es inevitable en este tipo de decisión, y no pretendemos eliminarlo, solo
acotarlo. Lo que falta, y que se aborda cuando lleguemos a la Fase 5:

- Traducir estos criterios en el prompt exacto del Analizador.
- Medir consistencia (self-consistency) y acuerdo con anotadores humanos
  usando estos mismos criterios como guía compartida.