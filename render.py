"""Trophy card. Compact is the best rank. Regular is three. Wide is the full row."""

import sys
from pathlib import Path

from frame import dots, label, open_svg, trophy
from github_user import LADDER, trophies
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data, border=True):
    colors = theme(mode)
    ranked = sorted(data["rows"], key=lambda row: (_strength(row["rank"]), -row["score"]))
    if size == "mini":
        return _mini(mode, colors, data, ranked[0], border)
    if size == "compact":
        return _compact(mode, colors, data, ranked[0], border)
    if size == "wide":
        return _wide(mode, colors, data, border)
    return _regular(mode, colors, data, ranked[:3], border)


def _strength(rank):
    try:
        return LADDER.index(rank)
    except ValueError:
        return len(LADDER)


def _ink(mode, colors):
    return colors["fg"] if mode.endswith("-r") else None


def _rule(x, y, width, height, color):
    return (
        f'<rect x="{x + 0.5:.1f}" y="{y + 0.5:.1f}" width="{width - 1:.1f}" '
        f'height="{height - 1:.1f}" fill="none" stroke="{color}"/>'
    )


def _square(x, y, size, color):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" fill="{color}"/>'


def _cup_scale(max_width, max_height, rank, colors, mode):
    ink = _ink(mode, colors)
    best = 1.5
    scale = 1.5
    while scale <= 4.8:
        _mark, cup_w, cup_h = trophy(0, 0, scale, rank, colors, ink)
        if cup_w > max_width or cup_h > max_height:
            break
        best = scale
        scale = round(scale + 0.05, 2)
    return round(best, 2)


def _plate(x, y, width, height, row, colors, scale, mode):
    ink = _ink(mode, colors)
    _mark, cup_w, cup_h = trophy(0, 0, scale, row["rank"], colors, ink)
    top, band = 16, 32
    cup_y = y + top + max(0, (height - top - band - cup_h) / 2)
    cup_x = x + (width - cup_w) / 2
    mid = x + width / 2
    return "".join([
        _rule(x, y, width, height, colors["rule"]),
        _square(x + 10, y + 10, 5, colors["mark"]),
        trophy(cup_x, cup_y, scale, row["rank"], colors, ink)[0],
        label(mid, y + height - 18, row["title"], colors["fg"], 12, 0.4, "middle"),
        label(mid, y + height - 5, f"{row['score']:,}", colors["muted"], 11, 0.1, "middle"),
    ])


def _plates(x, y, width, height, rows, colors, mode):
    span = width / len(rows)
    ink = _ink(mode, colors)
    widest = max(rows, key=lambda row: trophy(0, 0, 2, row["rank"], colors, ink)[1])
    scale = _cup_scale(span - 12, height - 48, widest["rank"], colors, mode)
    return "".join(
        _plate(x + index * span, y, span, height, row, colors, scale, mode)
        for index, row in enumerate(rows)
    )


def _mini(mode, colors, data, best, border):
    name, _ = dots("TROPHIES", 28, 12, colors["fg"], scale=1.15)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} trophies", mark=6, margin=14, border=border),
        name,
        _plate(12, 38, 196, 98, best, colors, _cup_scale(176, 50, best["rank"], colors, mode), mode),
        "</svg>",
    ])


def _compact(mode, colors, data, best, border):
    name, _ = dots("TROPHIES", 36, 16, colors["fg"], scale=1.8)
    x, y, width, height = 16, 46, 463, 70
    scale = _cup_scale(168, height - 10, best["rank"], colors, mode)
    ink = _ink(mode, colors)
    _mark, cup_w, cup_h = trophy(0, 0, scale, best["rank"], colors, ink)
    text_left = x + 28 + cup_w + 20
    text_mid = text_left + (x + width - 16 - text_left) / 2
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} trophies", border=border),
        name,
        _rule(x, y, width, height, colors["rule"]),
        _square(x + 10, y + 10, 5, colors["mark"]),
        trophy(x + 28, y + (height - cup_h) / 2, scale, best["rank"], colors, ink)[0],
        label(text_mid, y + height / 2 - 2, best["title"], colors["fg"], 16, 0.3, "middle"),
        label(text_mid, y + height / 2 + 18, f"{best['score']:,}", colors["muted"], 13, 0.2, "middle"),
        "</svg>",
    ])


def _regular(mode, colors, data, rows, border):
    name, _ = dots("TROPHIES", 36, 16, colors["fg"], scale=1.8)
    width = 440
    return "\n".join([
        open_svg(mode, width, 208, f"{data['login']} trophies", border=border),
        name,
        label(width - 20, 30, f"@{data['login']}", colors["muted"], 12, 0.2, "end"),
        _plates(16, 48, width - 32, 144, rows, colors, mode),
        "</svg>",
    ])


def _wide(mode, colors, data, border):
    name, _ = dots("TROPHIES", 36, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 896, 248, f"{data['login']} trophies", border=border),
        name,
        _plates(16, 48, 864, 184, data["rows"], colors, mode),
        "</svg>",
    ])


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/nothing-github-trophies?username={login}&theme={mode}&size={size}"
    return [
        f"**{card}** · {mode} · {size}",
        "",
        f"`{url}`",
        "",
        f"![{card} {mode} {size}](dist/{login}/{filename})",
        "",
    ]


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "itsrealkaran"
    data = trophies(login)
    out = ROOT / "dist" / data["login"]
    out.mkdir(parents=True, exist_ok=True)
    lines = [
        f"# {data['login']}",
        "",
        "Compact is the best rank. Regular is the top three. Wide is the six-rank row. The trophy is a glass disc held by two arms on a flat base. The category and the score are centered under it.",
        "",
    ]
    for mode in MODES:
        lines += [f"## {mode}", ""]
        for size in SIZES:
            filename = f"{mode}-{size}.svg"
            (out / filename).write_text(render(mode, size, data))
            lines += _variant("trophies", data["login"], mode, size, filename)
            print(data["login"], mode, size)
    (ROOT / "DUMMY.md").write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
