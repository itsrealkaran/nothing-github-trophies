"""SVG frame shared by one card. The dot grid never sets body copy."""

from datetime import datetime, timedelta, timezone

from nothing import GLYPHS, theme


# The center letter stays the single-letter size, with a blank cell between
# it and the cup. Extra letters are smaller, share its baseline, and sit in a
# lower shoulder. The rim rises over the tall letter and steps down over the
# short ones, like a crown.
RANKS = ("SSS", "SS", "S", "AAA", "AA", "A", "B", "C")
SHOULDER = 5


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

    if count < 2:
        _plain_cup(dot, x, y, scale, frame, bool(text))
        letter_col, handle = 4, 12
    else:
        letter_col, handle = _crown_cup(dot, x, y, scale, frame, bool(text), count)
    if letter:
        _glyph(dot, x, y, letter_col, 3, scale, GLYPHS[letter], ink)
        if count >= 2:
            _side_letters(dot, x, y, scale, step, count, letter, ink)
    return "".join(parts), handle * step + scale, 13 * step + scale


def _glyph(dot, x, y, col, row, size, grid, fill):
    for grid_row, bits in enumerate(grid):
        for grid_col, bit in enumerate(bits):
            if bit == "1":
                dot(x, y, col + grid_col, row + grid_row, size, fill)


def _plain_cup(dot, x, y, scale, frame, peaked):
    if peaked:
        dot(x, y, 6, 0, scale, frame)
    for col in range(2, 11):
        dot(x, y, col, 1, scale, frame)
    for row in range(2, 11):
        dot(x, y, 1, row, scale, frame)
        dot(x, y, 11, row, scale, frame)
    for row in (4, 5, 6):
        dot(x, y, 0, row, scale, frame)
        dot(x, y, 12, row, scale, frame)
    for col in range(1, 12):
        dot(x, y, col, 11, scale, frame)
    for col in range(4, 9):
        dot(x, y, col, 12, scale, frame)
    for col in range(3, 10):
        dot(x, y, col, 13, scale, frame)


def _crown_cup(dot, x, y, scale, frame, peaked, count):
    left = SHOULDER if count >= 3 else 0
    raised_left = 1 + left
    raised_right = raised_left + 10
    outer_right = raised_right + SHOULDER
    outer_left = 1
    stem = (raised_left + raised_right) // 2
    if peaked:
        dot(x, y, stem, 0, scale, frame)
    for col in range(raised_left + 1, raised_right):
        dot(x, y, col, 1, scale, frame)
    for row in range(2, 5):
        dot(x, y, raised_left, row, scale, frame)
        dot(x, y, raised_right, row, scale, frame)
    if left:
        for col in range(outer_left + 1, raised_left):
            dot(x, y, col, 4, scale, frame)
        dot(x, y, outer_left, 4, scale, frame)
    for col in range(raised_right + 1, outer_right):
        dot(x, y, col, 4, scale, frame)
    dot(x, y, outer_right, 4, scale, frame)
    for row in range(5, 11):
        dot(x, y, outer_left if left else raised_left, row, scale, frame)
        dot(x, y, outer_right, row, scale, frame)
    for row in ((6, 7, 8) if left else (4, 5, 6)):
        dot(x, y, 0, row, scale, frame)
    for row in (6, 7, 8):
        dot(x, y, outer_right + 1, row, scale, frame)
    wall = outer_left if left else raised_left
    for col in range(wall, outer_right + 1):
        dot(x, y, col, 11, scale, frame)
    for col in range(stem - 2, stem + 3):
        dot(x, y, col, 12, scale, frame)
    for col in range(stem - 3, stem + 4):
        dot(x, y, col, 13, scale, frame)
    return raised_left + 3, outer_right + 1


def _side_letters(dot, x, y, scale, step, count, letter, fill):
    left = SHOULDER if count >= 3 else 0
    raised_left = 1 + left
    raised_right = raised_left + 10
    outer_right = raised_right + SHOULDER
    bottom = 9 * step + scale
    max_h = bottom - (5 * step + 1.2)
    side = min(scale * 0.55, (max_h - 6.6) / 7)
    shoulders = []
    if left:
        shoulders.append((1 * step + scale, raised_left * step))
    shoulders.append((raised_right * step + scale, outer_right * step))
    gap = min(right - left_edge for left_edge, right in shoulders)
    side = min(side, ((gap - 3.2) - 4.4) / 5)
    if side < 0.7:
        return
    side_h = 6 * (side + 1.1) + side
    side_w = 4 * (side + 1.1) + side
    side_y = y + bottom - side_h
    for left_edge, right in shoulders:
        origin = x + left_edge + (right - left_edge - side_w) / 2
        _glyph(dot, origin, side_y, 0, 0, side, GLYPHS[letter], fill)


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
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" rx="6" '
        f'fill="{colors["bg"]}" stroke="{colors["rule"]}" stroke-width="1"/>'
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
