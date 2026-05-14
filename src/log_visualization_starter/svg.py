from __future__ import annotations

from html import escape


def line_chart_svg(title: str, series: list[tuple[str, float]], width: int = 760, height: int = 320) -> str:
    pad_left = 58
    pad_top = 38
    pad_right = 24
    pad_bottom = 44
    inner_w = width - pad_left - pad_right
    inner_h = height - pad_top - pad_bottom
    values = [value for _, value in series]
    if not values:
        points = ""
        min_value = max_value = 0.0
    else:
        min_value = min(values)
        max_value = max(values)
        span = max(max_value - min_value, 1e-9)
        points = " ".join(
            f"{pad_left + (inner_w * idx / max(len(values) - 1, 1)):.2f},"
            f"{pad_top + inner_h - ((value - min_value) / span * inner_h):.2f}"
            for idx, value in enumerate(values)
        )

    first_label = escape(series[0][0]) if series else ""
    last_label = escape(series[-1][0]) if series else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{pad_left}" y="24" font-family="Arial, sans-serif" font-size="18" font-weight="700" fill="#172026">{escape(title)}</text>
  <line x1="{pad_left}" y1="{pad_top}" x2="{pad_left}" y2="{pad_top + inner_h}" stroke="#9aa8b2"/>
  <line x1="{pad_left}" y1="{pad_top + inner_h}" x2="{pad_left + inner_w}" y2="{pad_top + inner_h}" stroke="#9aa8b2"/>
  <text x="8" y="{pad_top + 4}" font-family="Arial, sans-serif" font-size="12" fill="#49545c">{max_value:.4g}</text>
  <text x="8" y="{pad_top + inner_h}" font-family="Arial, sans-serif" font-size="12" fill="#49545c">{min_value:.4g}</text>
  <polyline points="{points}" fill="none" stroke="#0f6b70" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round"/>
  <text x="{pad_left}" y="{height - 14}" font-family="Arial, sans-serif" font-size="11" fill="#49545c">{first_label}</text>
  <text x="{pad_left + inner_w}" y="{height - 14}" text-anchor="end" font-family="Arial, sans-serif" font-size="11" fill="#49545c">{last_label}</text>
</svg>
"""

