# Nota de circularidad entre modelos

> Fase 0 del plan de acción, punto 4. Esto no es una definición operacional
> como las de `docs/operational_definitions.md`, es una regla de diseño
> experimental: qué componentes NO deben compartir modelo (ni familia de
> modelo, cuando sea posible) para que los resultados del paper sean válidos
> y no un artefacto de que el sistema se "reconoce a sí mismo".

## 1. El problema

Un LLM tiene sesgos y patrones característicos de su distribución de
entrenamiento. Si dos componentes del framework que se supone que actúan de
forma independiente comparten modelo (o familia de modelo), el resultado
puede parecer bueno no porque el diseño funcione, sino porque ambos
componentes comparten el mismo punto ciego. Hay dos sitios concretos del
pipeline donde esto es un riesgo real, no teórico:

### 1.1 Generador del dataset sintético ↔ Analizador

Si el mismo modelo (o familia) genera el dataset sintético y luego analiza
sensibilidad/interés público sobre ese mismo dataset, el Analizador puede
"reconocer" patrones que él mismo tiende a producir al generar texto, en vez
de razonar genuinamente sobre el contenido. Esto infla artificialmente la
precisión aparente del Analizador cuando se valida contra el ground truth del
dataset sintético (Fase 3) — un resultado que no se sostendría sobre texto
real.

### 1.2 Adversario del ataque de privacidad ↔ componentes del pipeline de anonimización

Si el modelo adversario (Fase 10, ataque de Staab et al.) comparte familia
con el Detector/Analizador/Reescritor, el adversario puede heredar los mismos
puntos ciegos que el sistema que está atacando — fallaría en inferir
exactamente los mismos atributos que el Reescritor falla en ocultar bien,
por las razones equivocadas. El resultado sería una métrica de privacidad
artificialmente optimista: el framework parecería más seguro de lo que es
frente a un adversario real, independiente y potencialmente distinto.

Este segundo caso es el más grave de los dos, porque afecta directamente a
una de las dos métricas centrales del paper (privacidad), no a una validación
intermedia.

## 2. Regla general

**Al menos dos familias de modelo distintas**, repartidas así:

| Rol | Grupo |
|---|---|
| Detector, Analizador, Reescritor | Grupo A — son componentes internos y colaborativos del propio framework; no se validan unos contra otros, así que compartir modelo entre ellos no es un problema de circularidad (si acaso, de consistencia interna, que se mide aparte con self-consistency en la Fase 5) |
| Generador del dataset sintético | Grupo B — debe ser de familia distinta al Grupo A |
| Adversario del ataque de privacidad (Fase 10) | Grupo C — debe ser de familia distinta al Grupo A. Puede coincidir o no con el Grupo B; no hay conflicto directo entre generador y adversario porque no se validan mutuamente, pero si el presupuesto de modelos locales lo permite, mejor que también difiera, por limpieza metodológica general |

Esto es un principio de diseño; la asignación concreta de modelos (versión,
cuantización, checkpoint) se fija cuando lleguemos a la fase de
infraestructura de modelos, no aquí — este documento fija la regla, esa fase
fija los nombres exactos.

## 3. Limitación residual (a documentar en el paper, no a resolver aquí)

Usar familias de modelo distintas mitiga el riesgo pero no lo elimina del
todo: dos modelos open-source de organizaciones distintas pueden seguir
compartiendo sesgos correlacionados si sus datos de entrenamiento o su
proceso de destilación se solapan (p. ej. varios modelos abiertos recientes
se entrenan en parte con salidas de otros LLM grandes). No hay forma barata
de eliminar esto del todo con recursos locales limitados a una única GPU;
lo correcto es reconocerlo explícitamente como limitación en el paper, no
presentar la separación de familias como una garantía absoluta de
independencia.