"""
Country registry for the multi-country synthetic patient generator.

Each module exposes a CONFIG dict. REGISTRY maps ISO-ish country code -> CONFIG.
Order here is the display order used in the dashboard's country picker.
"""

from . import br, uy, py, tt, cu, dj, er, tz, ml

REGISTRY = {
    cfg["code"]: cfg
    for cfg in (
        br.CONFIG, uy.CONFIG, py.CONFIG, tt.CONFIG, cu.CONFIG,
        dj.CONFIG, er.CONFIG, tz.CONFIG, ml.CONFIG,
    )
}

# code -> display name, in registry order
COUNTRY_NAMES = {code: cfg["name"] for code, cfg in REGISTRY.items()}
