# Taxonomía de atributos GDPR

> Fase 0 del plan de acción. Este documento es el diccionario de referencia para
> `entity_type` en `AttributeSpan` (`schemas.py`) y para el prompt del Detector
> (Fase 4). No contiene código; es la definición formal que se cita en la
> sección de metodología del paper.

**Nota sobre `NAME`:** en el diseño del pipeline, la identidad del sujeto del
texto se trata como un componente aparte (`SubjectIdentity`), no como un
`AttributeSpan` más, porque sigue un camino distinto en el flujo (verificación
de notoriedad en Wikidata antes que nada). Se mantiene aquí como entrada de la
taxonomía porque sigue siendo un identificador directo a efectos del Art. 4(1)
GDPR y puede aparecer como tal en otros contextos (p. ej. nombres de terceros
mencionados en el texto que no son el sujeto principal), pero el Detector debe
distinguir explícitamente "identidad del sujeto" de "aparición de un nombre
como atributo de un tercero".

---

## 1. Categorías especiales

Corresponden, en su mayoría, al Art. 9(1) GDPR ("categorías especiales de
datos personales"). `CRIMINAL_RECORD` es la excepción: en el GDPR tiene
régimen propio en el **Art. 10** (datos relativos a condenas e infracciones
penales), no el Art. 9 — se agrupa aquí porque exige el mismo nivel de
cautela, pero conviene citarlo con su artículo correcto en el paper, no como
si fuera Art. 9.

`is_special_category: true` para todos los atributos de esta sección.

### Identificadores directos

*Ninguno.*

### Identificadores indirectos

- `HEALTH_DATA`
- `GENETIC_DATA`
<!-- `BIOMETRIC_DATA` -- pendiente de decidir si se incluye, dejado fuera por ahora -->
- `RACIAL_ETHNIC_ORIGIN`
- `POLITICAL_OPINION`
- `RELIGIOUS_BELIEF`
- `PHILOSOPHICAL_BELIEFS`
- `TRADE_UNION_MEMBERSHIP`
- `SEXUAL_ORIENTATION`
- `SEX_LIFE`
- `CRIMINAL_RECORD` — Art. 10 GDPR, no Art. 9 (ver nota arriba)

---

## 2. Categorías no especiales

Corresponden al Art. 4(1) GDPR (identificadores y cuasi-identificadores en
sentido amplio, lista abierta). `is_special_category: false`.

### Identificadores directos

- `NAME`
- `EMAIL`
- `PHONE_NUMBER`
- `ADDRESS`
- `ID_NUMBER`
- `BANK_ACCOUNT`
- `CREDIT_CARD`
- `SOCIAL_SECURITY`
- `TAX_ID`
- `USERNAME`
- `DEVICE_ID`
- `IP_ADDRESS`
- `COOKIE_ID`
- `RFID_TAGS`

### Identificadores indirectos

- `FINANCIAL_DATA`
- `ROMANTIC_FAMILY_LIFE`
- `CURRENT_RESIDENCE`
- `MOVEMENTS_LOCATION_TRACKING`
- `AGE`
- `PLACE_OF_BIRTH_NATIONALITY`
- `PROFESSIONAL_ROLE`
- `POLITICAL_OFFICE`
- `EDUCATION`
- `CAREER_HISTORY`
- `MENTAL_IDENTITY`
- `PERSONAL_INTERESTS_PREFERENCES`

---

## Pendiente en esta fase

- [ ] Decidir si se incluye `BIOMETRIC_DATA` (de momento fuera, comentado arriba).
- [ ] Definición operacional de "figura pública" (siguiente documento de la Fase 0).
- [ ] Definición operacional de "interés público del atributo" (siguiente documento de la Fase 0).