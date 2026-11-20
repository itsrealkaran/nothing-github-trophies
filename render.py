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


def _scale(size):
    return {"mini": 2.8, "compact": 3.2, "regular": 2.6, "wide": 2.7}[size]


def _cup(x, y, scale, row, colors):
    mark, width, _height = trophy(x, y, scale, row["rank"], colors)
    return mark, width


def _mini(mode, colors, data, best):
    name, _ = dots("TROPHIES", 28, 12, colors["fg"], scale=1.15)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} trophies", mark=6, margin=14),
        name,
        _cup(16, 46, _scale("mini"), best, colors)[0],
        label(100, 86, best["title"], colors["fg"], 14, 0.1),
        label(100, 108, f"{best['score']:,}", colors["muted"], 12, 0.2),
        "</svg>",
    ])


def _compact(mode, colors, data, best):
    name, _ = dots("TROPHIES", 40, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} trophies"),
        name,
        _cup(20, 44, _scale("compact"), best, colors)[0],
        label(120, 86, best["title"], colors["fg"], 16, 0.2),
        label(120, 110, f"{best['score']:,}", colors["muted"], 13, 0.2),
        "</svg>",
    ])


def _regular(mode, colors, data, rows):
    name, _ = dots("TROPHIES", 40, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, 495, 192, f"{data['login']} trophies"), name]
    _mark, _width, tall = trophy(0, 0, _scale("regular"), "A", colors)
    bottom = 48 + tall
    for index, row in enumerate(rows):
        x = 20 + index * 155
        scale = _scale("regular")
        _mark, width, height = trophy(0, 0, scale, row["rank"], colors)
        parts.append(_cup(x + (130 - width) / 2, bottom - height, scale, row, colors)[0])
        parts.append(label(x, 122, row["title"], colors["fg"], 13, 0.2))
        parts.append(label(x, 142, f"{row['score']:,}", colors["muted"], 12, 0.2))
    parts.append(f'<line x1="20" y1="160" x2="475" y2="160" stroke="{colors["rule"]}"/>')
    parts.append(label(20, 178, f"@{data['login']}", colors["fg"], 12, 0.2))
    parts.append("</svg>")
    return "\n".join(parts)


def _wide(mode, colors, data):
    name, _ = dots("TROPHIES", 40, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, 896, 248, f"{data['login']} trophies"), name]
    _mark, _width, tall = trophy(0, 0, _scale("wide"), "A", colors)
    bottom = 84 + tall
    for index, row in enumerate(data["rows"]):
        x = 20 + index * 146
        scale = _scale("wide")
        _mark, width, height = trophy(0, 0, scale, row["rank"], colors)
        parts.append(
            f'<rect x="{x}" y="72" width="134" height="156" fill="none" stroke="{colors["rule"]}"/>'
        )
        parts.append(_cup(x + (134 - width) / 2, bottom - height, scale, row, colors)[0])
        parts.append(label(x + 12, 168, row["title"], colors["fg"], 13, 0.2))
        parts.append(label(x + 12, 190, f"{row['score']:,}", colors["muted"], 12, 0.2))
    parts.append("</svg>")
    return "\n".join(parts)


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
