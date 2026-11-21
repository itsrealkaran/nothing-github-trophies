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
  const dot = (originX, originY, col, row, size, fill) => {
    const stride = size + 1.1;
    const cx = originX + col * stride + size / 2;
    const cy = originY + row * stride + size / 2;
    parts.push(
      `<circle cx="${fixed(cx, 1)}" cy="${fixed(cy, 1)}" r="${fixed(size / 2, 2)}" fill="${fill}"/>`
    );
  };
  const handle = award(dot, x, y, scale, step, frame, count, letter, fill);
  return [parts.join(""), handle * step + scale, 13 * step + scale];
}

function glyph(dot, x, y, col, row, size, grid, fill) {
  grid.forEach((bits, gridRow) => {
    for (let gridCol = 0; gridCol < bits.length; gridCol += 1) {
      if (bits[gridCol] === "1") dot(x, y, col + gridCol, row + gridRow, size, fill);
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

function placement(scale, step, count) {
  const c0 = 1;
  if (count < 2) return { c0, c1: 11, handle: 12, group: 0, count };
  const side = scale * 0.52;
  const gap = Math.max(1.1, step * 0.22);
  const bigW = 4 * step + scale;
  const sideW = 4 * (side + 1.1) + side;
  const group = count >= 3 ? sideW + gap + bigW + gap + sideW : bigW + gap + sideW;
  const margin = step * 0.85;
  let span = 10;
  while (span * step - scale < group + margin * 2) span += 2;
  return { c0, c1: c0 + span, handle: c0 + span + 1, group, side, sideW, gap, bigW, count };
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
    if (rightCenter > leftCenter && (row === 0 || row === 10)) {
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
  for (let row = 4; row <= 8; row += 1) {
    dot(x, y, left, row, scale, frame);
    dot(x, y, right, row, scale, frame);
  }
  hook(dot, x, y, scale, frame, left, center - 4, 1);
  hook(dot, x, y, scale, frame, right, center + 4, -1);
}

function hook(dot, x, y, scale, frame, outer, edge, inward) {
  const sign = inward > 0 ? 1 : -1;
  const first = outer + sign;
  dot(x, y, first, 8, scale, frame);
  dot(x, y, first, 9, scale, frame);
  const span = Math.abs(edge - first);
  if (span > 1) {
    const mid = first + sign * Math.floor(span / 2 + 0.5);
    for (let col = Math.min(first, mid); col <= Math.max(first, mid); col += 1) {
      dot(x, y, col, 9, scale, frame);
    }
    for (let col = Math.min(mid, edge); col <= Math.max(mid, edge); col += 1) {
      dot(x, y, col, 10, scale, frame);
    }
  }
  dot(x, y, edge, 10, scale, frame);
  dot(x, y, edge, 11, scale, frame);
  dot(x, y, edge + inward, 11, scale, frame);
}

function base(dot, x, y, scale, frame, c0, c1) {
  const center = (c0 + c1) / 2;
  for (let col = center - 4; col <= center + 4; col += 1) {
    dot(x, y, col, 12, scale, frame);
    dot(x, y, col, 13, scale, frame);
  }
}

function rankLetters(dot, x, y, scale, step, placed, letter, fill) {
  if (!placed.group) {
    glyph(dot, x, y, 4, 2, scale, GLYPHS[letter], fill);
    return;
  }
  const mid = x + ((placed.c0 + placed.c1) / 2) * step + scale / 2;
  let cursor = mid - placed.group / 2;
  const sideH = 6 * (placed.side + 1.1) + placed.side;
  const sideY = y + 8 * step + scale - sideH;
  const grid = GLYPHS[letter];
  if (placed.count >= 3) {
    glyph(dot, cursor, sideY, 0, 0, placed.side, grid, fill);
    cursor += placed.sideW + placed.gap;
  }
  glyph(dot, cursor, y, 0, 2, scale, grid, fill);
  cursor += placed.bigW + placed.gap;
  glyph(dot, cursor, sideY, 0, 0, placed.side, grid, fill);
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

function openSvg(mode, width, height, title, mark = 8, margin = 20) {
  const colors = theme(mode);
  return (
    `<svg xmlns="http://www.w3.org/2000/svg" width="${py(width)}" height="${py(height)}" ` +
    `viewBox="0 0 ${py(width)} ${py(height)}" role="img">` +
    `<title>${xml(title)}</title>` +
    `<rect width="${py(width)}" height="${py(height)}" rx="16" fill="${colors.bg}"/>` +
    `<rect x="${py(margin)}" y="${py(margin)}" width="${py(mark)}" height="${py(mark)}" fill="${colors.mark}"/>`
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
