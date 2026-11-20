"""SVG frame shared by one card. The dot grid never sets body copy."""

from datetime import datetime, timedelta, timezone

from nothing import GLYPHS, theme


# The center letter stays the single-letter size. Extra letters are smaller
# and sit inside the cup, on the right for a double grade and on both sides
# for a triple grade.
RANKS = ("SSS", "SS", "S", "AAA", "AA", "A", "B", "C")


def trophy(x, y, scale, rank, colors):
    text = rank if rank in RANKS else ""
    letter = text[:1]
    count = len(text)
    step = scale + 1.1
    frame = colors["fg"] if text else colors["muted"]
    parts = []

    def dot(origin_x, origin_y, col, row, size, fill):
        stride = size + 1.1
        cx = origin_x + col * stride + size / 2
        cy = origin_y + row * stride + size / 2
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{size / 2:.2f}" fill="{fill}"/>')

    extra_left = 4 if count >= 3 else 0
    extra_right = 4 if count >= 2 else 0
    left_wall = 1
    right_wall = 9 + extra_left + extra_right
    stem = (left_wall + right_wall) // 2
    letter_col = stem - 2
    handle = right_wall + 1

    if text:
        dot(x, y, stem, 0, scale, frame)
    for col in range(left_wall + 1, right_wall):
        dot(x, y, col, 1, scale, frame)
    for row in range(2, 10):
        dot(x, y, left_wall, row, scale, frame)
        dot(x, y, right_wall, row, scale, frame)
    for row in (4, 5, 6):
        dot(x, y, 0, row, scale, frame)
        dot(x, y, handle, row, scale, frame)
    dot(x, y, stem, 10, scale, frame)
    for col in range(left_wall + 2, right_wall - 1):
        dot(x, y, col, 11, scale, frame)
    for col in range(left_wall + 1, right_wall):
        dot(x, y, col, 12, scale, frame)
    if letter:
        for row, bits in enumerate(GLYPHS[letter]):
            for col, bit in enumerate(bits):
                if bit == "1":
                    dot(x, y, letter_col + col, row + 3, scale, colors["mark"])
        _side_letters(
            dot, x, y, scale, step, count, letter, colors["mark"],
            left_wall, right_wall, letter_col,
        )
    return "".join(parts), handle * step + scale, 12 * step + scale


def _side_letters(dot, x, y, scale, step, count, letter, fill, left_wall, right_wall, letter_col):
    if count < 2:
        return
    glyph_w = 4 * step + scale
    glyph_h = 6 * step + scale
    letter_left = letter_col * step
    letter_right = letter_left + glyph_w
    inner_left = left_wall * step + scale
    inner_right = right_wall * step
    pad = 1.5
    gaps = []
    if count >= 3:
        gaps.append(letter_left - inner_left)
    if count >= 2:
        gaps.append(inner_right - letter_right)
    room = min(gaps) - pad * 2
    side = min(scale * 0.32, (room - 4.4) / 5)
    if side < 0.75:
        return
    side_step = side + 1.1
    side_w = 4 * side_step + side
    side_h = 6 * side_step + side
    mid = 3 * step + glyph_h / 2
    side_y = y + mid - side_h / 2

    def paint(origin_x):
        for row, bits in enumerate(GLYPHS[letter]):
            for col, bit in enumerate(bits):
                if bit == "1":
                    dot(origin_x, side_y, col, row, side, fill)

    if count >= 3:
        paint(x + inner_left + pad + (letter_left - inner_left - pad * 2 - side_w) / 2)
    if count >= 2:
        paint(x + letter_right + pad + (inner_right - letter_right - pad * 2 - side_w) / 2)


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


def label(x, y, text, fill, size=13, tracking=0.4):
    return (
        f'<text x="{x}" y="{y}" fill="{fill}" '
        f'font-family="ui-monospace, Geist Mono, monospace" '
        f'font-size="{size}" letter-spacing="{tracking}" dominant-baseline="auto">{xml(text)}</text>'
    )
