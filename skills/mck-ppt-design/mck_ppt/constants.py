# Copyright 2024-2026 Kaku Li (https://github.com/likaku)
# Licensed under the Apache License, Version 2.0 — see LICENSE and NOTICE.
# Part of "Mck-ppt-design-skill" (McKinsey PPT Design Framework).
# NOTICE: This file must be retained in all copies or substantial portions.
#
"""McKinsey Design System — Color palette, typography, and layout constants."""
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor

# ═══════════════════════════════════════════
# COLOR PALETTE
# ═══════════════════════════════════════════

# Local customization: CIIC palette supplied by the user, 2026-09-10.
# Keep numeric brand values in one maintained file.
import json as _json
from pathlib import Path as _Path
BRAND = _json.loads((_Path(__file__).resolve().parents[1] / 'references/team/ciic-palette.json').read_text())
def _rgb(value):
    return RGBColor.from_string(value)
PRIMARY_BLUE = _rgb(BRAND['primary'])
NAVY = PRIMARY_BLUE  # compatibility alias for existing layout APIs
WHITE = _rgb(BRAND['white'])
BLACK = DARK_GRAY = MED_GRAY = _rgb(BRAND['text'])
BG_GRAY = _rgb(BRAND['background'])
LINE_GRAY = _rgb(BRAND['accents'][5])
CIIC_ORANGE = _rgb(BRAND['orange'])
CHART_COLORS = tuple(_rgb(value) for value in BRAND['accents'])
ACCENT_BLUE = CHART_COLORS[0]
# Legacy names remain callable; these aliases use the CIIC palette only.
ACCENT_GREEN = CHART_COLORS[1]
ACCENT_ORANGE = ACCENT_RED = CIIC_ORANGE
LIGHT_BLUE = LIGHT_GREEN = _rgb(BRAND['tints'][-1])
LIGHT_ORANGE = LIGHT_RED = BG_GRAY
ACCENT_PAIRS = [(color, LIGHT_BLUE) for color in CHART_COLORS[:4]]
ALLOWED_HEX = frozenset([BRAND[k] for k in ('primary','white','text','background','orange')] + BRAND['accents'] + BRAND['tints'])
THEME_COLORS = dict(zip(
    ('dk1','lt1','dk2','lt2','accent1','accent2','accent3','accent4','accent5','accent6','hlink','folHlink'),
    (BRAND['text'],BRAND['white'],BRAND['orange'],BRAND['background'],*BRAND['accents'],BRAND['accents'][0],BRAND['accents'][5])))

# ═══════════════════════════════════════════
# SLIDE DIMENSIONS
# ═══════════════════════════════════════════

SW = Inches(13.333)  # Slide width (16:9)
SH = Inches(7.5)     # Slide height
LM = Inches(0.8)     # Left margin
RM = Inches(0.8)     # Right margin
CW = Inches(11.733)  # Content width = SW - LM - RM

# ═══════════════════════════════════════════
# VERTICAL GRID
# ═══════════════════════════════════════════

TITLE_TOP       = Inches(0.15)   # Action title top
TITLE_H         = Inches(0.9)    # Action title height
TITLE_LINE_Y    = Inches(1.05)   # Separator under title
CONTENT_TOP     = Inches(1.3)    # Content area start
SOURCE_Y        = Inches(7.05)   # Source attribution line
PAGE_NUM_X      = Inches(12.2)   # Page number left
BOTTOM_BAR_Y    = Inches(6.2)    # Default bottom summary bar
BOTTOM_BAR_H    = Inches(0.65)   # Bottom bar height

# ═══════════════════════════════════════════
# TYPOGRAPHY
# ═══════════════════════════════════════════

COVER_TITLE_SIZE   = Pt(44)
SECTION_TITLE_SIZE = Pt(28)
ACTION_TITLE_SIZE  = Pt(22)
SUB_HEADER_SIZE    = Pt(18)
EMPHASIS_SIZE      = Pt(16)
BODY_SIZE          = Pt(14)
SMALL_SIZE         = Pt(12)
FOOTNOTE_SIZE      = Pt(9)

FONT_HEADER = BRAND['font']
FONT_BODY = BRAND['font']
FONT_EA = BRAND['font']
