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

    def dot(origin_x, origin_y, col, row, size, fill):
        stride = size + 1.1
        cx = origin_x + col * stride + size / 2
        cy = origin_y + row * stride + size / 2
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size / 2:.2f}" fill="{fill}"/>')

    handle = _award(dot, x, y, scale, step, frame, count, letter, ink)
    return "".join(parts), handle * step + scale, 13 * step + scale


def _glyph(dot, x, y, col, row, size, grid, fill):
    for grid_row, bits in enumerate(grid):
        for grid_col, bit in enumerate(bits):
            if bit == "1":
                dot(x, y, col + grid_col, row + grid_row, size, fill)


def _award(dot, x, y, scale, step, frame, count, letter, fill):
    placed = _placement(scale, step, count)
    _disc(dot, x, y, scale, frame, placed["c0"], placed["c1"])
    _arms(dot, x, y, scale, frame, placed["c0"], placed["c1"])
    _base(dot, x, y, scale, frame, placed["c0"], placed["c1"])
    if letter:
        _rank_letters(dot, x, y, scale, step, placed, letter, fill)
    return placed["handle"]


def _placement(scale, step, count):
    c0 = 1
    if count < 2:
        return {"c0": c0, "c1": 11, "handle": 12, "group": 0, "count": count}
    side = scale * 0.52
    gap = max(1.1, step * 0.22)
    big_w = 4 * step + scale
    side_w = 4 * (side + 1.1) + side
    group = side_w + gap + big_w + gap + side_w if count >= 3 else big_w + gap + side_w
    margin = step * 0.85
    span = 10
    while span * step - scale < group + margin * 2:
        span += 2
    return {
        "c0": c0,
        "c1": c0 + span,
        "handle": c0 + span + 1,
        "group": group,
        "side": side,
        "side_w": side_w,
        "gap": gap,
        "big_w": big_w,
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
        if right_center > left_center and row in (0, 10):
            inner_left = left_center + max(offset for offset in offsets if offset <= 0)
            inner_right = right_center + min(offset for offset in offsets if offset >= 0)
            cols.update(range(inner_left, inner_right + 1))
        for col in cols:
            dot(x, y, col, row, scale, frame)


def _arms(dot, x, y, scale, frame, c0, c1):
    left = c0 - 1
    right = c1 + 1
    center = int((c0 + c1) / 2)
    for row in range(4, 9):
        dot(x, y, left, row, scale, frame)
        dot(x, y, right, row, scale, frame)
    _hook(dot, x, y, scale, frame, left, center - 4, 1)
    _hook(dot, x, y, scale, frame, right, center + 4, -1)


def _hook(dot, x, y, scale, frame, outer, edge, inward):
    sign = 1 if inward > 0 else -1
    first = outer + sign
    dot(x, y, first, 8, scale, frame)
    dot(x, y, first, 9, scale, frame)
    span = abs(edge - first)
    if span > 1:
        mid = first + sign * int(span / 2 + 0.5)
        for col in range(min(first, mid), max(first, mid) + 1):
            dot(x, y, col, 9, scale, frame)
        for col in range(min(mid, edge), max(mid, edge) + 1):
            dot(x, y, col, 10, scale, frame)
    dot(x, y, edge, 10, scale, frame)
    dot(x, y, edge, 11, scale, frame)
    dot(x, y, edge + inward, 11, scale, frame)


def _base(dot, x, y, scale, frame, c0, c1):
    center = int((c0 + c1) / 2)
    for col in range(center - 4, center + 4 + 1):
        dot(x, y, col, 12, scale, frame)
        dot(x, y, col, 13, scale, frame)


def _rank_letters(dot, x, y, scale, step, placed, letter, fill):
    if not placed["group"]:
        _glyph(dot, x, y, 4, 2, scale, GLYPHS[letter], fill)
        return
    mid = x + ((placed["c0"] + placed["c1"]) / 2) * step + scale / 2
    cursor = mid - placed["group"] / 2
    side_h = 6 * (placed["side"] + 1.1) + placed["side"]
    side_y = y + 8 * step + scale - side_h
    grid = GLYPHS[letter]
    if placed["count"] >= 3:
        _glyph(dot, cursor, side_y, 0, 0, placed["side"], grid, fill)
        cursor += placed["side_w"] + placed["gap"]
    _glyph(dot, cursor, y, 0, 2, scale, grid, fill)
    cursor += placed["big_w"] + placed["gap"]
    _glyph(dot, cursor, side_y, 0, 0, placed["side"], grid, fill)


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


def open_svg(mode, width, height, title, mark=8, margin=20):
    colors = theme(mode)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img">'
        f"<title>{xml(title)}</title>"
        f'<rect width="{width}" height="{height}" rx="16" fill="{colors["bg"]}"/>'
        f'<rect x="{margin}" y="{margin}" width="{mark}" height="{mark}" fill="{colors["mark"]}"/>'
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
