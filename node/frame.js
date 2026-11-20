"use strict";

const { GLYPHS, theme } = require("./nothing");
const { fixed, py, xml } = require("./format");

// The center letter stays the single-letter size. Extra letters are smaller
// and sit inside the cup, on the right for a double grade and on both sides
// for a triple grade.
const RANKS = new Set(["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"]);

function trophy(x, y, scale, rank, colors) {
  const text = RANKS.has(rank) ? rank : "";
  const letter = text.slice(0, 1);
  const count = text.length;
  const step = scale + 1.1;
  const frame = text ? colors.fg : colors.muted;
  const parts = [];
  const dot = (originX, originY, col, row, size, fill) => {
    const stride = size + 1.1;
    const cx = originX + col * stride + size / 2;
    const cy = originY + row * stride + size / 2;
    parts.push(
      `<circle cx="${fixed(cx, 1)}" cy="${fixed(cy, 1)}" r="${fixed(size / 2, 2)}" fill="${fill}"/>`
    );
  };
  const extraLeft = count >= 3 ? 4 : 0;
  const extraRight = count >= 2 ? 4 : 0;
  const leftWall = 1;
  const rightWall = 9 + extraLeft + extraRight;
  const stem = Math.floor((leftWall + rightWall) / 2);
  const letterCol = stem - 2;
  const handle = rightWall + 1;
  if (text) dot(x, y, stem, 0, scale, frame);
  for (let col = leftWall + 1; col < rightWall; col += 1) dot(x, y, col, 1, scale, frame);
  for (let row = 2; row < 10; row += 1) {
    dot(x, y, leftWall, row, scale, frame);
    dot(x, y, rightWall, row, scale, frame);
  }
  for (const row of [4, 5, 6]) {
    dot(x, y, 0, row, scale, frame);
    dot(x, y, handle, row, scale, frame);
  }
  dot(x, y, stem, 10, scale, frame);
  for (let col = leftWall + 2; col < rightWall - 1; col += 1) dot(x, y, col, 11, scale, frame);
  for (let col = leftWall + 1; col < rightWall; col += 1) dot(x, y, col, 12, scale, frame);
  if (letter) {
    GLYPHS[letter].forEach((bits, row) => {
      for (let col = 0; col < bits.length; col += 1) {
        if (bits[col] === "1") dot(x, y, letterCol + col, row + 3, scale, colors.mark);
      }
    });
    sideLetters(dot, x, y, scale, step, count, letter, colors.mark, leftWall, rightWall, letterCol);
  }
  return [parts.join(""), handle * step + scale, 12 * step + scale];
}

function sideLetters(dot, x, y, scale, step, count, letter, fill, leftWall, rightWall, letterCol) {
  if (count < 2) return;
  const glyphW = 4 * step + scale;
  const glyphH = 6 * step + scale;
  const letterLeft = letterCol * step;
  const letterRight = letterLeft + glyphW;
  const innerLeft = leftWall * step + scale;
  const innerRight = rightWall * step;
  const pad = 1.5;
  const gaps = [];
  if (count >= 3) gaps.push(letterLeft - innerLeft);
  if (count >= 2) gaps.push(innerRight - letterRight);
  const room = Math.min(...gaps) - pad * 2;
  const side = Math.min(scale * 0.32, (room - 4.4) / 5);
  if (side < 0.75) return;
  const sideStep = side + 1.1;
  const sideW = 4 * sideStep + side;
  const sideH = 6 * sideStep + side;
  const mid = 3 * step + glyphH / 2;
  const sideY = y + mid - sideH / 2;
  const paint = (originX) => {
    GLYPHS[letter].forEach((bits, row) => {
      for (let col = 0; col < bits.length; col += 1) {
        if (bits[col] === "1") dot(originX, sideY, col, row, side, fill);
      }
    });
  };
  if (count >= 3) {
    paint(x + innerLeft + pad + (letterLeft - innerLeft - pad * 2 - sideW) / 2);
  }
  if (count >= 2) {
    paint(x + letterRight + pad + (innerRight - letterRight - pad * 2 - sideW) / 2);
  }
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
    `<rect x="0.5" y="0.5" width="${py(width - 1)}" height="${py(height - 1)}" rx="6" fill="${colors.bg}" stroke="${colors.rule}" stroke-width="1"/>` +
    `<rect x="${py(margin)}" y="${py(margin)}" width="${py(mark)}" height="${py(mark)}" fill="${colors.mark}"/>`
  );
}

function label(x, y, text, fill, size = 13, tracking = 0.4) {
  return (
    `<text x="${py(x)}" y="${py(y)}" fill="${fill}" ` +
    `font-family="ui-monospace, Geist Mono, monospace" ` +
    `font-size="${py(size)}" letter-spacing="${py(tracking)}" dominant-baseline="auto">${xml(text)}</text>`
  );
}

module.exports = { dots, openSvg, label, trophy };
