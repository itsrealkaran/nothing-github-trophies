"use strict";

const { dots, label, openSvg, trophy } = require("./frame");
const { theme } = require("./nothing");
const { commas, fixed } = require("./format");

const LADDER = ["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"];

function render(mode, size, data, border = true) {
  const colors = theme(mode);
  const ranked = data.rows.slice().sort((a, b) => strength(a.rank) - strength(b.rank) || b.score - a.score);
  if (size === "mini") return mini(mode, colors, data, ranked[0], border);
  if (size === "compact") return compact(mode, colors, data, ranked[0], border);
  if (size === "wide") return wide(mode, colors, data, border);
  return regular(mode, colors, data, ranked.slice(0, 3), border);
}

function strength(rank) {
  const index = LADDER.indexOf(rank);
  return index === -1 ? LADDER.length : index;
}

function letterInk(mode, colors) {
  return mode.endsWith("-r") ? colors.fg : null;
}

function rule(x, y, width, height, color) {
  return (
    `<rect x="${fixed(x + 0.5, 1)}" y="${fixed(y + 0.5, 1)}" width="${fixed(width - 1, 1)}" ` +
    `height="${fixed(height - 1, 1)}" fill="none" stroke="${color}"/>`
  );
}

function square(x, y, size, color) {
  return `<rect x="${fixed(x, 1)}" y="${fixed(y, 1)}" width="${size}" height="${size}" fill="${color}"/>`;
}

function cupScale(maxWidth, maxHeight, rank, colors, mode) {
  const ink = letterInk(mode, colors);
  let best = 1.5;
  for (let scale = 1.5; scale <= 4.8; scale += 0.05) {
    const measured = trophy(0, 0, scale, rank, colors, ink);
    if (measured[1] > maxWidth || measured[2] > maxHeight) break;
    best = scale;
  }
  return Math.round(best * 20) / 20;
}

function plate(x, y, width, height, row, colors, scale, mode) {
  const ink = letterInk(mode, colors);
  const measured = trophy(0, 0, scale, row.rank, colors, ink);
  const top = 16;
  const band = 32;
  const cupY = y + top + Math.max(0, (height - top - band - measured[2]) / 2);
  const cupX = x + (width - measured[1]) / 2;
  const mid = x + width / 2;
  return [
    rule(x, y, width, height, colors.rule),
    square(x + 10, y + 10, 5, colors.mark),
    trophy(cupX, cupY, scale, row.rank, colors, ink)[0],
    label(mid, y + height - 18, row.title, colors.fg, 12, 0.4, "middle"),
    label(mid, y + height - 5, commas(row.score), colors.muted, 11, 0.1, "middle"),
  ].join("");
}

function plates(x, y, width, height, rows, colors, mode) {
  const span = width / rows.length;
  const ink = letterInk(mode, colors);
  const widest = rows.reduce((best, row) => {
    const size = trophy(0, 0, 2, row.rank, colors, ink)[1];
    return size > best.size ? { rank: row.rank, size } : best;
  }, { rank: rows[0].rank, size: 0 });
  const scale = cupScale(span - 12, height - 48, widest.rank, colors, mode);
  return rows.map((row, index) => plate(x + index * span, y, span, height, row, colors, scale, mode)).join("");
}

function mini(mode, colors, data, best, border) {
  const [name] = dots("TROPHIES", 28, 12, colors.fg, 1.15);
  return [
    openSvg(mode, 220, 148, data.login + " trophies", 6, 14, border),
    name,
    plate(12, 38, 196, 98, best, colors, cupScale(176, 50, best.rank, colors, mode), mode),
    "</svg>",
  ].join("\n");
}

function compact(mode, colors, data, best, border) {
  const [name] = dots("TROPHIES", 36, 16, colors.fg, 1.8);
  const x = 16;
  const y = 46;
  const width = 463;
  const height = 70;
  const scale = cupScale(168, height - 10, best.rank, colors, mode);
  const ink = letterInk(mode, colors);
  const measured = trophy(0, 0, scale, best.rank, colors, ink);
  const textLeft = x + 28 + measured[1] + 20;
  const textMid = textLeft + (x + width - 16 - textLeft) / 2;
  return [
    openSvg(mode, 495, 132, data.login + " trophies", 8, 20, border),
    name,
    rule(x, y, width, height, colors.rule),
    square(x + 10, y + 10, 5, colors.mark),
    trophy(x + 28, y + (height - measured[2]) / 2, scale, best.rank, colors, ink)[0],
    label(textMid, y + height / 2 - 2, best.title, colors.fg, 16, 0.3, "middle"),
    label(textMid, y + height / 2 + 18, commas(best.score), colors.muted, 13, 0.2, "middle"),
    "</svg>",
  ].join("\n");
}

function regular(mode, colors, data, rows, border) {
  const [name] = dots("TROPHIES", 36, 16, colors.fg, 1.8);
  const width = 408;
  return [
    openSvg(mode, width, 208, data.login + " trophies", 8, 20, border),
    name,
    label(width - 20, 30, "@" + data.login, colors.muted, 12, 0.2, "end"),
    plates(16, 48, width - 32, 144, rows, colors, mode),
    "</svg>",
  ].join("\n");
}

function wide(mode, colors, data, border) {
  const [name] = dots("TROPHIES", 36, 16, colors.fg, 1.8);
  return [
    openSvg(mode, 896, 248, data.login + " trophies", 8, 20, border),
    name,
    plates(16, 48, 864, 184, data.rows, colors, mode),
    "</svg>",
  ].join("\n");
}

module.exports = { render };
