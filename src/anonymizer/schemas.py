"""
Contratos de datos del framework de anonimización.

Ver documentación de la Fase 0:
- docs/gdpr_taxonomy.md (taxonomía de entity_type / is_special_category)
- docs/operational_definitions.md (figura pública, interés público del atributo)

Estas clases son la base de todo el pipeline: Detector, Verificador de
notoriedad, Analizador, Matriz y Anonimizadores se comunican exclusivamente
a través de estas estructuras.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal, Optional

# --- Tipos controlados (evitan strings "mágicos" sueltos por el código) ---

Sensitivity = Literal["high", "medium", "low"]
PublicInterest = Literal["high", "low"]
Technique = Literal["generalization", "rewriting", "suppression", "no_change"]


# --- Identidad del sujeto (se trata aparte de los atributos, ver docs/gdpr_taxonomy.md) ---


@dataclass
class SubjectIdentity:
    """La entidad de la que habla el texto (a quien se asocian los atributos sensibles).

    No es un AttributeSpan más: sigue su propio camino en el pipeline
    (verificación de notoriedad antes que nada, ver NotorietyCheckResult).
    """

    text: str
    spans: list[tuple[int, int]] = field(default_factory=list)  # puede repetirse en el texto
    notoriety: Optional["NotorietyCheckResult"] = None


# --- Verificador de notoriedad (Wikidata) ---


@dataclass
class ExternalContext:
    """Contexto factual recuperado (Wikidata/Wikipedia) para el Analizador.

    IMPORTANTE: este objeto solo debe llegar al Analizador. NUNCA pasarlo al
    Reescritor ni al Generalizador, o el framework acabaría añadiendo
    información nueva al texto anonimizado que no estaba en el original.
    """

    occupation: list[str] = field(default_factory=list)
    positions_held: list[str] = field(default_factory=list)
    field_of_work: list[str] = field(default_factory=list)
    notability_signal: int = 0  # nº de sitelinks Wikidata, proxy de magnitud de notoriedad
    short_biographical_extract: str = ""
    retrieved_at: str = ""  # timestamp/versión — snapshot para reproducibilidad


@dataclass
class NotorietyCheckResult:
    """¿Es esta identidad una figura pública verificable? (ver docs/operational_definitions.md, sección 1)"""

    is_public_figure: bool
    confidence: float  # 0.0-1.0
    wikidata_id: Optional[str] = None
    candidate_entities: list[str] = field(default_factory=list)  # candidatos descartados, para auditar
    disambiguation_evidence: str = ""
    external_context: Optional[ExternalContext] = None  # solo si is_public_figure=True


# --- Atributos sensibles detectados ---


@dataclass
class AttributeSpan:
    text: str
    entity_type: str  # ver configs/gdpr_attribute_taxonomy.yaml (NO incluye la identidad)
    start: int
    end: int
    is_special_category: bool = False  # ¿categoría especial Art. 9 GDPR?


# --- Juicio del Analizador (solo si is_public_figure=True) ---


@dataclass
class AttributeAssessment:
    """Ver docs/operational_definitions.md, sección 2, para el criterio de public_interest."""

    attribute: AttributeSpan
    sensitivity: Sensitivity
    public_interest: PublicInterest
    rationale: str = ""  # justificación del LLM — imprescindible para auditar errores


# --- Salida de la Matriz de decisión ---


@dataclass
class AnonymizationDecision:
    attribute: AttributeAssessment
    technique: Technique
    generalization_level: Optional[int] = None