"""Test de sanidad de la taxonomía GDPR (Fase 0 del plan).

No valida contenido legal (eso lo hacéis vosotros al escribir el .md), solo que
el .yaml que usará el Detector está bien formado: carga, no tiene duplicados,
y no hay ningún entity_type que aparezca a la vez como especial y no especial.
"""

from pathlib import Path

import yaml

_TAXONOMY_PATH = Path(__file__).resolve().parents[1] / "configs" / "gdpr_attribute_taxonomy.yaml"


def _load_taxonomy():
    with _TAXONOMY_PATH.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _all_special_types(taxonomy):
    especiales = taxonomy["categorias_especiales"]
    return especiales["identificadores_directos"] + especiales["identificadores_indirectos"]


def _all_non_special_types(taxonomy):
    no_especiales = taxonomy["categorias_no_especiales"]
    return no_especiales["identificadores_directos"] + no_especiales["identificadores_indirectos"]


def test_taxonomy_loads():
    taxonomy = _load_taxonomy()
    assert "categorias_especiales" in taxonomy
    assert "categorias_no_especiales" in taxonomy


def test_no_special_direct_identifiers():
    # Confirmado explícitamente en docs/gdpr_taxonomy.md: ninguno.
    taxonomy = _load_taxonomy()
    assert taxonomy["categorias_especiales"]["identificadores_directos"] == []


def test_no_duplicate_entity_types_within_taxonomy():
    taxonomy = _load_taxonomy()
    special = _all_special_types(taxonomy)
    non_special = _all_non_special_types(taxonomy)
    all_types = special + non_special
    assert len(all_types) == len(set(all_types)), "Hay entity_type duplicados en la taxonomía"


def test_no_overlap_between_special_and_non_special():
    taxonomy = _load_taxonomy()
    special = set(_all_special_types(taxonomy))
    non_special = set(_all_non_special_types(taxonomy))
    assert special.isdisjoint(non_special), (
        "Un mismo entity_type no puede ser especial y no especial a la vez"
    )


def test_criminal_record_present_and_flagged_for_special_footnote():
    # No es Art. 9 (es Art. 10), pero se agrupa con las categorías especiales
    # por nivel de cautela — ver nota en docs/gdpr_taxonomy.md.
    taxonomy = _load_taxonomy()
    assert "CRIMINAL_RECORD" in _all_special_types(taxonomy)
