"""SVG frame shared by one card. The dot grid never sets body copy."""

from datetime import datetime, timedelta, timezone

from nothing import GLYPHS, theme


# A glass disc holds the rank. Two arms cradle its lower half and stand on a flat base.
# A double grade adds a smaller letter on the right. A triple grade adds one on each
# side. The rank is centered in the disc, and the shorter letters share its baseline.
RANKS = ("SSS", "SS", "S", "AAA", "AA", "A", "B", "C")


def trophy(x, y, scale, rank, colors, ink=None):
    text = rank if rank in RANKS else ""
    letter = text[:1]
    count = len(text)
    step = scale + 1.1
    frame = colors["fg"] if text else colors["muted"]
    # A reversed theme passes the cup color so the letters stay unaccented.
    ink = ink or colors["mark"]
    parts = []

    def dot(origin_x, origin_y, col, row, size, fill, radius=None):
        stride = size + 1.1
        cx = origin_x + col * stride + size / 2
        cy = origin_y + row * stride + size / 2
        r = size / 2 if radius is None else radius
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.2f}" fill="{fill}"/>')

    handle = _award(dot, x, y, scale, step, frame, count, letter, ink)
    return "".join(parts), handle * step + scale, 15 * step + scale


def _glyph(dot, x, y, col, row, size, grid, fill, radius=None):
    for grid_row, bits in enumerate(grid):
        for grid_col, bit in enumerate(bits):
            if bit == "1":
                dot(x, y, col + grid_col, row + grid_row, size, fill, radius)


def _award(dot, x, y, scale, step, frame, count, letter, fill):
    placed = _placement(scale, step, count)
    _disc(dot, x, y, scale, frame, placed["c0"], placed["c1"])
    _arms(dot, x, y, scale, frame, placed["c0"], placed["c1"])
    _base(dot, x, y, scale, frame, placed["c0"], placed["c1"])
    if letter:
        _rank_letters(dot, x, y, scale, step, placed, letter, fill)
    return placed["handle"]


def _metrics(scale):
    ink = scale * 0.7
    side = ink * 0.62
    big_w, big_h = _ink_size(ink)
    side_w, side_h = _ink_size(side)
    radius = side * 0.58
    spill = max(0, radius - side / 2)
    return {
        "ink": ink,
        "side": side,
        "big_w": big_w,
        "big_h": big_h,
        "side_w": side_w,
        "side_h": side_h,
        "radius": radius,
        "spill": spill,
        "side_box": side_w + spill * 2,
        "gap": max(1.5, (ink + 1.1) * 0.48),
    }


def _placement(scale, step, count):
    c0 = 1
    if count < 2:
        return {"c0": c0, "c1": 11, "handle": 12, "group": 0, "count": count}
    box = _metrics(scale)
    group = (
        box["side_box"] + box["gap"] + box["big_w"] + box["gap"] + box["side_box"]
        if count >= 3
        else box["big_w"] + box["gap"] + box["side_box"]
    )
    # The glass stays clear of the grade on both sides.
    margin = step * 2.35
    span = 10
    while span * step - scale < group + margin * 2:
        span += 2
    return {
        "c0": c0,
        "c1": c0 + span,
        "handle": c0 + span + 1,
        "group": group,
        "count": count,
    }


# Offsets from the disc's center. One center is a circle. Two centers stretch it
# into the wider plaque that holds the extra letters.
PROFILE = (
    (-2, -1, 0, 1, 2),
    (-3, -2, 2, 3),
    (-4, 4),
    (-5, -4, 4, 5),
    (-5, 5),
    (-5, 5),
    (-5, 5),
    (-5, 5),
    (-5, 5),
    (-5, -4, 4, 5),
    (-4, 4),
    (-3, -2, 2, 3),
    (-2, -1, 0, 1, 2),
)


def _disc(dot, x, y, scale, frame, c0, c1):
    left_center = c0 + 5
    right_center = c1 - 5
    for row, offsets in enumerate(PROFILE):
        cols = set()
        for offset in offsets:
            if offset <= 0:
                cols.add(left_center + offset)
            if offset >= 0:
                cols.add(right_center + offset)
        if right_center > left_center and row in (0, 12):
            inner_left = left_center + max(offset for offset in offsets if offset <= 0)
            inner_right = right_center + min(offset for offset in offsets if offset >= 0)
            cols.update(range(inner_left, inner_right + 1))
        for col in cols:
            dot(x, y, col, row, scale, frame)


def _arms(dot, x, y, scale, frame, c0, c1):
    left = c0 - 1
    right = c1 + 1
    center = int((c0 + c1) / 2)
    for row in range(6, 11):
        dot(x, y, left, row, scale, frame)
        dot(x, y, right, row, scale, frame)
    _hook(dot, x, y, scale, frame, left, center - 4, 1)
    _hook(dot, x, y, scale, frame, right, center + 4, -1)


def _hook(dot, x, y, scale, frame, outer, edge, inward):
    sign = 1 if inward > 0 else -1
    first = outer + sign
    dot(x, y, first, 10, scale, frame)
    dot(x, y, first, 11, scale, frame)
    span = abs(edge - first)
    if span > 1:
        mid = first + sign * int(span / 2 + 0.5)
        for col in range(min(first, mid), max(first, mid) + 1):
            dot(x, y, col, 11, scale, frame)
        for col in range(min(mid, edge), max(mid, edge) + 1):
            dot(x, y, col, 12, scale, frame)
    dot(x, y, edge, 12, scale, frame)
    dot(x, y, edge, 13, scale, frame)
    dot(x, y, edge + inward, 13, scale, frame)


def _base(dot, x, y, scale, frame, c0, c1):
    center = int((c0 + c1) / 2)
    for col in range(center - 4, center + 4 + 1):
        dot(x, y, col, 14, scale, frame)
        dot(x, y, col, 15, scale, frame)


def _ink_size(size):
    stride = size + 1.1
    return 4 * stride + size, 6 * stride + size


def _centered_glyph(dot, cx, cy, size, grid, fill, radius=None):
    width, height = _ink_size(size)
    _glyph(dot, cx - width / 2, cy - height / 2, 0, 0, size, grid, fill, radius)


def _rank_letters(dot, x, y, scale, step, placed, letter, fill):
    """The grade sits inside the glass, smaller than the disc, so the rim stays clear."""
    ink = scale * 0.7
    grid = GLYPHS[letter]
    cy = y + 6 * step + scale / 2
    if not placed["group"]:
        cx = x + ((placed["c0"] + placed["c1"]) / 2) * step + scale / 2
        _centered_glyph(dot, cx, cy, ink, grid, fill)
        return
    box = _metrics(scale)
    ink = box["ink"]
    side = box["side"]
    big_w, big_h = box["big_w"], box["big_h"]
    side_w, side_h = box["side_w"], box["side_h"]
    radius = box["radius"]
    spill = box["spill"]
    side_box = box["side_box"]
    gap = box["gap"]
    side_cy = cy + big_h / 2 - side_h / 2
    group = side_box + gap + big_w + gap + side_box if placed["count"] >= 3 else big_w + gap + side_box
    mid = x + ((placed["c0"] + placed["c1"]) / 2) * step + scale / 2
    cursor = mid - group / 2
    if placed["count"] >= 3:
        _centered_glyph(dot, cursor + spill + side_w / 2, side_cy, side, grid, fill, radius)
        cursor += side_box + gap
    _centered_glyph(dot, cursor + big_w / 2, cy, ink, grid, fill)
    cursor += big_w + gap
    _centered_glyph(dot, cursor + spill + side_w / 2, side_cy, side, grid, fill, radius)


def dots(text, x, y, fill, scale=2.4):
    step = scale + 1.1
    parts = []
    cursor = x
    for char in text:
        grid = GLYPHS[char]
        for row, bits in enumerate(grid):
            for col, bit in enumerate(bits):
                if bit == "1":
                    cx = cursor + col * step + scale / 2
                    cy = y + row * step + scale / 2
                    parts.append(
                        f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{scale / 2:.2f}" fill="{fill}"/>'
                    )
        cursor += 5 * step + scale
    return "".join(parts), cursor - x


def open_svg(mode, width, height, title, mark=8, margin=20, border=True):
    colors = theme(mode)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f"<title>{xml(title)}</title>"
        f"{card_rect(width, height, colors, border)}"
        f'<rect x="{margin}" y="{margin}" width="{mark}" height="{mark}" fill="{colors["mark"]}"/>'
    )


def card_rect(width, height, colors, border, fill=""):
    ink = fill or colors["bg"]
    if not border:
        return f'<rect width="{width}" height="{height}" rx="16" fill="{ink}"/>'
    return (
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" '
        f'rx="8" fill="{ink}" stroke="{colors["rule"]}"/>'
    )


def week_glyphs(days, weeks, x, y, cell, gap, on, off):
    by_day = {}
    for day, count in days:
        by_day[datetime_date(day)] = count
    today = datetime.now(timezone.utc).date()
    sunday = today - timedelta(days=(today.weekday() + 1) % 7)
    start = sunday - timedelta(weeks=weeks - 1)
    parts = []
    for week in range(weeks):
        for row in range(7):
            day = start + timedelta(days=week * 7 + row)
            if day > today:
                continue
            fill = on if by_day.get(day, 0) else off
            parts.append(
                f'<rect x="{x + week * (cell + gap):.1f}" y="{y + row * (cell + gap):.1f}" '
                f'width="{cell}" height="{cell}" fill="{fill}"/>'
            )
    return "".join(parts)


def datetime_date(day):
    return datetime.strptime(day, "%Y-%m-%d").date()


def xml(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def label(x, y, text, fill, size=13, tracking=0.4, anchor="start"):
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}" '
        f'font-family="ui-monospace, Geist Mono, monospace" '
        f'font-size="{size}" letter-spacing="{tracking}" dominant-baseline="auto">{xml(text)}</text>'
    )
