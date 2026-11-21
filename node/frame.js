"use strict";

const { GLYPHS, theme } = require("./nothing");
const { fixed, py, xml } = require("./format");

// A glass disc holds the rank. Two arms cradle its lower half and stand on a flat base.
// A double grade adds a smaller letter on the right. A triple grade adds one on each
// side. The rank is centered in the disc, and the shorter letters share its baseline.
const RANKS = new Set(["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"]);

function trophy(x, y, scale, rank, colors, ink = null) {
  const text = RANKS.has(rank) ? rank : "";
  const letter = text.slice(0, 1);
  const count = text.length;
  const step = scale + 1.1;
  const frame = text ? colors.fg : colors.muted;
  // A reversed theme passes the cup color so the letters stay unaccented.
  const fill = ink || colors.mark;
  const parts = [];
  const dot = (originX, originY, col, row, size, fill, radius = null) => {
    const stride = size + 1.1;
    const cx = originX + col * stride + size / 2;
    const cy = originY + row * stride + size / 2;
    const r = radius == null ? size / 2 : radius;
    parts.push(
      `<circle cx="${fixed(cx, 1)}" cy="${fixed(cy, 1)}" r="${fixed(r, 2)}" fill="${fill}"/>`
    );
  };
  const handle = award(dot, x, y, scale, step, frame, count, letter, fill);
  return [parts.join(""), handle * step + scale, 15 * step + scale];
}

function glyph(dot, x, y, col, row, size, grid, fill, radius = null) {
  grid.forEach((bits, gridRow) => {
    for (let gridCol = 0; gridCol < bits.length; gridCol += 1) {
      if (bits[gridCol] === "1") dot(x, y, col + gridCol, row + gridRow, size, fill, radius);
    }
  });
}

function award(dot, x, y, scale, step, frame, count, letter, fill) {
  const placed = placement(scale, step, count);
  disc(dot, x, y, scale, frame, placed.c0, placed.c1);
  arms(dot, x, y, scale, frame, placed.c0, placed.c1);
  base(dot, x, y, scale, frame, placed.c0, placed.c1);
  if (letter) rankLetters(dot, x, y, scale, step, placed, letter, fill);
  return placed.handle;
}

function metrics(scale) {
  const ink = scale * 0.7;
  const side = ink * 0.62;
  const [bigW, bigH] = inkSize(ink);
  const [sideW, sideH] = inkSize(side);
  const radius = side * 0.58;
  const spill = Math.max(0, radius - side / 2);
  return {
    ink,
    side,
    bigW,
    bigH,
    sideW,
    sideH,
    radius,
    spill,
    sideBox: sideW + spill * 2,
    gap: Math.max(1.5, (ink + 1.1) * 0.48),
  };
}

function placement(scale, step, count) {
  const c0 = 1;
  if (count < 2) return { c0, c1: 11, handle: 12, group: 0, count };
  const box = metrics(scale);
  const group = count >= 3
    ? box.sideBox + box.gap + box.bigW + box.gap + box.sideBox
    : box.bigW + box.gap + box.sideBox;
  // The glass stays clear of the grade on both sides.
  const margin = step * 2.35;
  let span = 10;
  while (span * step - scale < group + margin * 2) span += 2;
  return { c0, c1: c0 + span, handle: c0 + span + 1, group, count };
}

// Offsets from the disc's center. One center is a circle. Two centers stretch it
// into the wider plaque that holds the extra letters.
const PROFILE = [
  [-2, -1, 0, 1, 2],
  [-3, -2, 2, 3],
  [-4, 4],
  [-5, -4, 4, 5],
  [-5, 5],
  [-5, 5],
  [-5, 5],
  [-5, 5],
  [-5, 5],
  [-5, -4, 4, 5],
  [-4, 4],
  [-3, -2, 2, 3],
  [-2, -1, 0, 1, 2],
];

function disc(dot, x, y, scale, frame, c0, c1) {
  const leftCenter = c0 + 5;
  const rightCenter = c1 - 5;
  PROFILE.forEach((offsets, row) => {
    const cols = new Set();
    offsets.forEach((offset) => {
      if (offset <= 0) cols.add(leftCenter + offset);
      if (offset >= 0) cols.add(rightCenter + offset);
    });
    if (rightCenter > leftCenter && (row === 0 || row === 12)) {
      const innerLeft = leftCenter + Math.max(...offsets.filter((offset) => offset <= 0));
      const innerRight = rightCenter + Math.min(...offsets.filter((offset) => offset >= 0));
      for (let col = innerLeft; col <= innerRight; col += 1) cols.add(col);
    }
    cols.forEach((col) => dot(x, y, col, row, scale, frame));
  });
}

function arms(dot, x, y, scale, frame, c0, c1) {
  const left = c0 - 1;
  const right = c1 + 1;
  const center = (c0 + c1) / 2;
  for (let row = 6; row <= 10; row += 1) {
    dot(x, y, left, row, scale, frame);
    dot(x, y, right, row, scale, frame);
  }
  hook(dot, x, y, scale, frame, left, center - 4, 1);
  hook(dot, x, y, scale, frame, right, center + 4, -1);
}

function hook(dot, x, y, scale, frame, outer, edge, inward) {
  const sign = inward > 0 ? 1 : -1;
  const first = outer + sign;
  dot(x, y, first, 10, scale, frame);
  dot(x, y, first, 11, scale, frame);
  const span = Math.abs(edge - first);
  if (span > 1) {
    const mid = first + sign * Math.floor(span / 2 + 0.5);
    for (let col = Math.min(first, mid); col <= Math.max(first, mid); col += 1) {
      dot(x, y, col, 11, scale, frame);
    }
    for (let col = Math.min(mid, edge); col <= Math.max(mid, edge); col += 1) {
      dot(x, y, col, 12, scale, frame);
    }
  }
  dot(x, y, edge, 12, scale, frame);
  dot(x, y, edge, 13, scale, frame);
  dot(x, y, edge + inward, 13, scale, frame);
}

function base(dot, x, y, scale, frame, c0, c1) {
  const center = (c0 + c1) / 2;
  for (let col = center - 4; col <= center + 4; col += 1) {
    dot(x, y, col, 14, scale, frame);
    dot(x, y, col, 15, scale, frame);
  }
}

function inkSize(size) {
  const stride = size + 1.1;
  return [4 * stride + size, 6 * stride + size];
}

function centeredGlyph(dot, cx, cy, size, grid, fill, radius = null) {
  const [width, height] = inkSize(size);
  glyph(dot, cx - width / 2, cy - height / 2, 0, 0, size, grid, fill, radius);
}

function rankLetters(dot, x, y, scale, step, placed, letter, fill) {
  // The grade sits inside the glass, smaller than the disc, so the rim stays clear.
  const ink = scale * 0.7;
  const grid = GLYPHS[letter];
  const cy = y + 6 * step + scale / 2;
  if (!placed.group) {
    const cx = x + ((placed.c0 + placed.c1) / 2) * step + scale / 2;
    centeredGlyph(dot, cx, cy, ink, grid, fill);
    return;
  }
  const box = metrics(scale);
  const side = box.side;
  const [bigW, bigH] = [box.bigW, box.bigH];
  const [sideW, sideH] = [box.sideW, box.sideH];
  const radius = box.radius;
  const spill = box.spill;
  const sideBox = box.sideBox;
  const gap = box.gap;
  const sideCy = cy + bigH / 2 - sideH / 2;
  const group = placed.count >= 3 ? sideBox + gap + bigW + gap + sideBox : bigW + gap + sideBox;
  const mid = x + ((placed.c0 + placed.c1) / 2) * step + scale / 2;
  let cursor = mid - group / 2;
  if (placed.count >= 3) {
    centeredGlyph(dot, cursor + spill + sideW / 2, sideCy, side, grid, fill, radius);
    cursor += sideBox + gap;
  }
  centeredGlyph(dot, cursor + bigW / 2, cy, ink, grid, fill);
  cursor += bigW + gap;
  centeredGlyph(dot, cursor + spill + sideW / 2, sideCy, side, grid, fill, radius);
}

function dots(text, x, y, fill, scale = 2.4) {
  const step = scale + 1.1;
  const parts = [];
  let cursor = x;
  for (const char of text) {
    const grid = GLYPHS[char];
    if (!grid) throw new Error("missing glyph " + char);
    grid.forEach((bits, row) => {
      for (let col = 0; col < bits.length; col += 1) {
        if (bits[col] !== "1") continue;
        const cx = cursor + col * step + scale / 2;
        const cy = y + row * step + scale / 2;
        parts.push(
          `<circle cx="${fixed(cx, 1)}" cy="${fixed(cy, 1)}" r="${fixed(scale / 2, 2)}" fill="${fill}"/>`
        );
      }
    });
    cursor += 5 * step + scale;
  }
  return [parts.join(""), cursor - x];
}

function openSvg(mode, width, height, title, mark = 8, margin = 20, border = true) {
  const colors = theme(mode);
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${py(width)}" height="${py(height)}" ` +
    `viewBox="0 0 ${py(width)} ${py(height)}" role="img">` +
    `<title>${xml(title)}</title>` +
    cardRect(width, height, colors, border) +
    `<rect x="${py(margin)}" y="${py(margin)}" width="${py(mark)}" height="${py(mark)}" fill="${colors.mark}"/>`
  );
}

function cardRect(width, height, colors, border, fill) {
  const ink = fill || colors.bg;
  if (!border) return `<rect width="${py(width)}" height="${py(height)}" rx="16" fill="${ink}"/>`;
  return (
    `<rect x="0.5" y="0.5" width="${py(width - 1)}" height="${py(height - 1)}" ` +
    `rx="8" fill="${ink}" stroke="${colors.rule}"/>`
  );
}

function label(x, y, text, fill, size = 13, tracking = 0.4, anchor = "start") {
  return (
    `<text x="${py(x)}" y="${py(y)}" fill="${fill}" text-anchor="${anchor}" ` +
    `font-family="ui-monospace, Geist Mono, monospace" ` +
    `font-size="${py(size)}" letter-spacing="${py(tracking)}" dominant-baseline="auto">${xml(text)}</text>`
  );
}

module.exports = { dots, openSvg, label, trophy };
