# anonymizer-gdpr

Framework de anonimización de texto basado en GDPR, con discriminación por
figura pública e interés público del atributo.

## Estado actual: Fase 0 (definiciones, sin código de pipeline todavía)

Vamos fase a fase; no hay implementación del pipeline aún, solo lo que ya se
ha cerrado explícitamente en esta fase:

- `docs/gdpr_taxonomy.md` — taxonomía de atributos GDPR (fuente narrativa/legal).
- `configs/gdpr_attribute_taxonomy.yaml` — espejo mecánico de la taxonomía anterior.
- `docs/operational_definitions.md` — definición operacional de "figura pública"
  (sección 2, "interés público del atributo", pendiente).
- `tests/test_gdpr_taxonomy.py` — sanidad del yaml de taxonomía.

## Tests

```bash
pip install -e ".[dev]"
python -m pytest -v
```
