"use strict";

const { GLYPHS, theme } = require("./nothing");
const { fixed, py, xml } = require("./format");

// The rank is the bowl: one letter, or the whole token when the grade is longer.
const RANKS = new Set(["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"]);

function trophy(x, y, scale, rank, colors) {
  const text = RANKS.has(rank) ? rank : "";
  const count = text.length || 1;
  const cols = 6 + count * 5 + (count - 1);
  const center = (cols - 1) / 2;
  const rightWall = cols - 2;
  const rightHandle = cols - 1;
  const step = scale + 1.1;
  const frame = text ? colors.fg : colors.muted;
  const parts = [];
  const dot = (col, row, fill) => {
    const cx = x + col * step + scale / 2;
    const cy = y + row * step + scale / 2;
    parts.push(
      `<circle cx="${fixed(cx, 1)}" cy="${fixed(cy, 1)}" r="${fixed(scale / 2, 2)}" fill="${fill}"/>`
    );
  };
  if (text) dot(center, 0, frame);
  for (let col = 2; col < rightWall; col += 1) dot(col, 1, frame);
  for (let row = 2; row < 10; row += 1) {
    dot(1, row, frame);
    dot(rightWall, row, frame);
  }
  for (const row of [4, 5, 6]) {
    dot(0, row, frame);
    dot(rightHandle, row, frame);
  }
  dot(center, 10, frame);
  for (let col = center - 2; col < center + 3; col += 1) dot(col, 11, frame);
  for (let col = center - 3; col < center + 4; col += 1) dot(col, 12, frame);
  for (let index = 0; index < text.length; index += 1) {
    const origin = 3 + index * 6;
    GLYPHS[text[index]].forEach((bits, row) => {
      for (let col = 0; col < bits.length; col += 1) {
        if (bits[col] === "1") dot(origin + col, row + 3, colors.mark);
      }
    });
  }
  return [parts.join(""), (cols - 1) * step + scale, 12 * step + scale];
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
