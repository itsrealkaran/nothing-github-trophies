"""SVG frame shared by one card. The dot grid never sets body copy."""

from datetime import datetime, timedelta, timezone

from nothing import GLYPHS, theme


# The rank is the bowl: one letter, or the whole token when the grade is longer.
RANKS = ("SSS", "SS", "S", "AAA", "AA", "A", "B", "C")


def trophy(x, y, scale, rank, colors):
    text = rank if rank in RANKS else ""
    count = len(text) or 1
    cols = 6 + count * 5 + (count - 1)
    center = (cols - 1) // 2
    right_wall = cols - 2
    right_handle = cols - 1
    step = scale + 1.1
    frame = colors["fg"] if text else colors["muted"]
    parts = []

    def dot(col, row, fill):
        cx = x + col * step + scale / 2
        cy = y + row * step + scale / 2
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{scale / 2:.2f}" fill="{fill}"/>')

    if text:
        dot(center, 0, frame)
    for col in range(2, right_wall):
        dot(col, 1, frame)
    for row in range(2, 10):
        dot(1, row, frame)
        dot(right_wall, row, frame)
    for row in (4, 5, 6):
        dot(0, row, frame)
        dot(right_handle, row, frame)
    dot(center, 10, frame)
    for col in range(center - 2, center + 3):
        dot(col, 11, frame)
    for col in range(center - 3, center + 4):
        dot(col, 12, frame)
    for index, char in enumerate(text):
        origin = 3 + index * 6
        for row, bits in enumerate(GLYPHS[char]):
            for col, bit in enumerate(bits):
                if bit == "1":
                    dot(origin + col, row + 3, colors["mark"])
    return "".join(parts), (cols - 1) * step + scale, 12 * step + scale


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
