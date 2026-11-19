"""Trophy card. Compact is the best rank. Regular is three. Wide is the full row."""

import sys
from pathlib import Path

from frame import dots, label, open_svg
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


def _mini(mode, colors, data, best):
    name, _ = dots("TROPHIES", 28, 12, colors["fg"], scale=1.15)
    return "\n".join([
        open_svg(mode, 220, 148, f"{data['login']} trophies", mark=6, margin=14),
        name,
        label(16, 96, best["rank"], colors["figure"], 32, -0.8),
        label(16, 118, best["title"], colors["fg"], 13, 0.1),
        label(16, 136, f"{best['score']:,}", colors["muted"], 12, 0.2),
        "</svg>",
    ])


def _compact(mode, colors, data, best):
    name, _ = dots("TROPHIES", 40, 16, colors["fg"], scale=1.8)
    return "\n".join([
        open_svg(mode, 495, 132, f"{data['login']} trophies"),
        name,
        label(20, 108, best["rank"], colors["figure"], 42, -1),
        label(160, 90, best["title"], colors["fg"], 16, 0.2),
        label(160, 112, f"{best['score']:,}", colors["muted"], 13, 0.2),
        "</svg>",
    ])


def _regular(mode, colors, data, rows):
    name, _ = dots("TROPHIES", 40, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, 495, 195, f"{data['login']} trophies"), name]
    for index, row in enumerate(rows):
        x = 20 + index * 155
        parts.append(label(x, 112, row["rank"], colors["figure"], 32, -0.8))
        parts.append(label(x, 138, row["title"], colors["fg"], 13, 0.2))
        parts.append(label(x, 156, f"{row['score']:,}", colors["muted"], 12, 0.2))
    parts.append(f'<line x1="20" y1="168" x2="475" y2="168" stroke="{colors["rule"]}"/>')
    parts.append(label(20, 186, f"@{data['login']}", colors["fg"], 12, 0.2))
    parts.append("</svg>")
    return "\n".join(parts)


def _wide(mode, colors, data):
    name, _ = dots("TROPHIES", 40, 16, colors["fg"], scale=1.8)
    parts = [open_svg(mode, 896, 248, f"{data['login']} trophies"), name]
    for index, row in enumerate(data["rows"]):
        x = 20 + index * 146
        parts.append(
            f'<rect x="{x}" y="78" width="134" height="148" fill="none" stroke="{colors["rule"]}"/>'
        )
        parts.append(f'<rect x="{x + 12}" y="92" width="8" height="8" fill="{colors["mark"]}"/>')
        parts.append(label(x + 12, 150, row["rank"], colors["figure"], 28, -0.6))
        parts.append(label(x + 12, 176, row["title"], colors["fg"], 13, 0.2))
        parts.append(label(x + 12, 198, f"{row['score']:,}", colors["muted"], 12, 0.2))
    parts.append("</svg>")
    return "\n".join(parts)


def _variant(card, login, mode, size, filename):
    url = f"https://github.com/itsrealkaran/{card}?username={login}&theme={mode}&size={size}"
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
        "Compact is the best rank. Regular is the top three. Wide is the six-rank row.",
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
