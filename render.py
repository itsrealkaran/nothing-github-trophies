"""Trophy card. Compact is the best rank. Regular is three. Wide is the full row."""

import sys
from pathlib import Path

from frame import dots, label, open_svg, trophy
from github_user import LADDER, trophies
from nothing import MODES, SIZES, theme

ROOT = Path(__file__).resolve().parent


def render(mode, size, data):
    colors = theme(mode)
    ranked = sorted(data["rows"], key=lambda row: (_strength(row["rank"]), -row["score"]))
    if size == "mini":
        return _mini(mode, colors, data, ranked[0])
    if size == "compact":
        return _compact(mode, colors, data, ranked[0])
    if size == "wide":
        return _wide(mode, colors, data)
    return _regular(mode, colors, data, ranked[:3])


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


def _plate(x, y, width, height, row, colors, scale, mode):
    ink = _ink(mode, colors)
    _mark, cup_w, cup_h = trophy(0, 0, scale, row["rank"], colors, ink)
    top, band = 18, 34
    cup_y = y + top + max(0, (height - top - band - cup_h) / 2)
    cup_x = x + (width - cup_w) / 2
    return "".join([
        _rule(x, y, width, height, colors["rule"]),
        _square(x + 10, y + 10, 5, colors["mark"]),
        trophy(cup_x, cup_y, scale, row["rank"], colors, ink)[0],
        label(x + 10, y + height - 20, row["title"], colors["fg"], 12, 0.5),
        label(x + 10, y + height - 6, f"{row['score']:,}", colors["muted"], 11, 0.15),
    ])


def _plates(x, y, width, height, rows, colors, scale, mode):
    span = width / len(rows)
    return "".join(
        _plate(x + index * span, y, span, height, row, colors, scale, mode)
        for index, row in enumerate(rows)
    )


def _mini(mode, colors, data, best):
    name, _ = dots("TROPHIES", 28, 12, colors["fg"], scale=1.15)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} trophies", mark=6, margin=14),
        name,
        _plate(12, 38, 196, 98, best, colors, 2.0, mode),
        "</svg>",
    ])


def _compact(mode, colors, data, best):
    name, _ = dots("TROPHIES", 36, 16, colors["fg"], scale=1.8)
    x, y, width, height = 16, 46, 463, 70
    scale = 2.05
    ink = _ink(mode, colors)
    _mark, cup_w, cup_h = trophy(0, 0, scale, best["rank"], colors, ink)
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} trophies"),
        name,
        _rule(x, y, width, height, colors["rule"]),
        _square(x + 10, y + 10, 5, colors["mark"]),
        trophy(x + 36, y + (height - cup_h) / 2, scale, best["rank"], colors, ink)[0],
        label(x + 36 + cup_w + 28, y + 32, best["title"], colors["fg"], 16, 0.3),
        label(x + 36 + cup_w + 28, y + 54, f"{best['score']:,}", colors["muted"], 13, 0.2),
        "</svg>",
    ])


def _regular(mode, colors, data, rows):
    name, _ = dots("TROPHIES", 36, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 192, f"{data['login']} trophies"),
        name,
        label(475, 30, f"@{data['login']}", colors["muted"], 12, 0.2, "end"),
        _plates(16, 48, 463, 128, rows, colors, 2.2, mode),
        "</svg>",
    ])


def _wide(mode, colors, data):
    name, _ = dots("TROPHIES", 36, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 896, 248, f"{data['login']} trophies"),
        name,
        _plates(16, 48, 864, 184, data["rows"], colors, 2.2, mode),
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
        "Compact is the best rank. Regular is the top three. Wide is the six-rank row. Extra letters share the center baseline, and the rim steps down over them.",
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
