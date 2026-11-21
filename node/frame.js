"use strict";

const { GLYPHS, theme } = require("./nothing");
const { fixed, py, xml } = require("./format");

// The center letter stays the single-letter size, with a blank cell between
// it and the cup. Extra letters are smaller, share its baseline, and sit in a
// lower shoulder. The rim rises over the tall letter and steps down over the
// short ones, like a crown.
const RANKS = new Set(["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"]);
const SHOULDER = 5;

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
  let letterCol = 4;
  let handle = 12;
  if (count < 2) plainCup(dot, x, y, scale, frame, Boolean(text));
  else [letterCol, handle] = crownCup(dot, x, y, scale, frame, Boolean(text), count);
  if (letter) {
    glyph(dot, x, y, letterCol, 3, scale, GLYPHS[letter], fill);
    if (count >= 2) sideLetters(dot, x, y, scale, step, count, letter, fill);
  }
  return [parts.join(""), handle * step + scale, 13 * step + scale];
}

function glyph(dot, x, y, col, row, size, grid, fill) {
  grid.forEach((bits, gridRow) => {
    for (let gridCol = 0; gridCol < bits.length; gridCol += 1) {
      if (bits[gridCol] === "1") dot(x, y, col + gridCol, row + gridRow, size, fill);
    }
  });
}

function plainCup(dot, x, y, scale, frame, peaked) {
  if (peaked) dot(x, y, 6, 0, scale, frame);
  for (let col = 2; col < 11; col += 1) dot(x, y, col, 1, scale, frame);
  for (let row = 2; row < 11; row += 1) {
    dot(x, y, 1, row, scale, frame);
    dot(x, y, 11, row, scale, frame);
  }
  for (const row of [4, 5, 6]) {
    dot(x, y, 0, row, scale, frame);
    dot(x, y, 12, row, scale, frame);
  }
  for (let col = 1; col < 12; col += 1) dot(x, y, col, 11, scale, frame);
  for (let col = 4; col < 9; col += 1) dot(x, y, col, 12, scale, frame);
  for (let col = 3; col < 10; col += 1) dot(x, y, col, 13, scale, frame);
}

function crownCup(dot, x, y, scale, frame, peaked, count) {
  const left = count >= 3 ? SHOULDER : 0;
  const raisedLeft = 1 + left;
  const raisedRight = raisedLeft + 10;
  const outerRight = raisedRight + SHOULDER;
  const outerLeft = 1;
  const stem = Math.floor((raisedLeft + raisedRight) / 2);
  if (peaked) dot(x, y, stem, 0, scale, frame);
  for (let col = raisedLeft + 1; col < raisedRight; col += 1) dot(x, y, col, 1, scale, frame);
  for (let row = 2; row < 5; row += 1) {
    dot(x, y, raisedLeft, row, scale, frame);
    dot(x, y, raisedRight, row, scale, frame);
  }
  if (left) {
    for (let col = outerLeft + 1; col < raisedLeft; col += 1) dot(x, y, col, 4, scale, frame);
    dot(x, y, outerLeft, 4, scale, frame);
  }
  for (let col = raisedRight + 1; col < outerRight; col += 1) dot(x, y, col, 4, scale, frame);
  dot(x, y, outerRight, 4, scale, frame);
  for (let row = 5; row < 11; row += 1) {
    dot(x, y, left ? outerLeft : raisedLeft, row, scale, frame);
    dot(x, y, outerRight, row, scale, frame);
  }
  for (const row of left ? [6, 7, 8] : [4, 5, 6]) dot(x, y, 0, row, scale, frame);
  for (const row of [6, 7, 8]) dot(x, y, outerRight + 1, row, scale, frame);
  const wall = left ? outerLeft : raisedLeft;
  for (let col = wall; col <= outerRight; col += 1) dot(x, y, col, 11, scale, frame);
  for (let col = stem - 2; col < stem + 3; col += 1) dot(x, y, col, 12, scale, frame);
  for (let col = stem - 3; col < stem + 4; col += 1) dot(x, y, col, 13, scale, frame);
  return [raisedLeft + 3, outerRight + 1];
}

function sideLetters(dot, x, y, scale, step, count, letter, fill) {
  const left = count >= 3 ? SHOULDER : 0;
  const raisedLeft = 1 + left;
  const raisedRight = raisedLeft + 10;
  const outerRight = raisedRight + SHOULDER;
  const bottom = 9 * step + scale;
  const maxH = bottom - (5 * step + 1.2);
  let side = Math.min(scale * 0.55, (maxH - 6.6) / 7);
  const shoulders = [];
  if (left) shoulders.push([1 * step + scale, raisedLeft * step]);
  shoulders.push([raisedRight * step + scale, outerRight * step]);
  const gap = Math.min(...shoulders.map(([leftEdge, right]) => right - leftEdge));
  side = Math.min(side, (gap - 3.2 - 4.4) / 5);
  if (side < 0.7) return;
  const sideH = 6 * (side + 1.1) + side;
  const sideW = 4 * (side + 1.1) + side;
  const sideY = y + bottom - sideH;
  shoulders.forEach(([leftEdge, right]) => {
    glyph(dot, x + leftEdge + (right - leftEdge - sideW) / 2, sideY, 0, 0, side, GLYPHS[letter], fill);
  });
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
