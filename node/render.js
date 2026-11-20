"use strict";

const { dots, label, openSvg, trophy } = require("./frame");
const { theme } = require("./nothing");
const { commas, fixed } = require("./format");

const LADDER = ["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"];

function render(mode, size, data) {
  const colors = theme(mode);
  const ranked = data.rows.slice().sort((a, b) => strength(a.rank) - strength(b.rank) || b.score - a.score);
  if (size === "mini") return mini(mode, colors, data, ranked[0]);
  if (size === "compact") return compact(mode, colors, data, ranked[0]);
  if (size === "wide") return wide(mode, colors, data);
  return regular(mode, colors, data, ranked.slice(0, 3));
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

function plate(x, y, width, height, row, colors, scale, mode) {
  const ink = letterInk(mode, colors);
  const measured = trophy(0, 0, scale, row.rank, colors, ink);
  const top = 18;
  const band = 34;
  const cupY = y + top + Math.max(0, (height - top - band - measured[2]) / 2);
  const cupX = x + (width - measured[1]) / 2;
  return [
    rule(x, y, width, height, colors.rule),
    square(x + 10, y + 10, 5, colors.mark),
    trophy(cupX, cupY, scale, row.rank, colors, ink)[0],
    label(x + 10, y + height - 20, row.title, colors.fg, 12, 0.5),
    label(x + 10, y + height - 6, commas(row.score), colors.muted, 11, 0.15),
  ].join("");
}

function plates(x, y, width, height, rows, colors, scale, mode) {
  const span = width / rows.length;
  return rows.map((row, index) => plate(x + index * span, y, span, height, row, colors, scale, mode)).join("");
}

function mini(mode, colors, data, best) {
  const [name] = dots("TROPHIES", 28, 12, colors.fg, 1.15);
  return [
    openSvg(mode, 220, 148, data.login + " trophies", 6, 14),
    name,
    plate(12, 38, 196, 98, best, colors, 2.0, mode),
    "</svg>",
  ].join("\n");
}

function compact(mode, colors, data, best) {
  const [name] = dots("TROPHIES", 36, 16, colors.fg, 1.8);
  const x = 16;
  const y = 46;
  const width = 463;
  const height = 70;
  const scale = 2.05;
  const ink = letterInk(mode, colors);
  const measured = trophy(0, 0, scale, best.rank, colors, ink);
  return [
    openSvg(mode, 495, 132, data.login + " trophies"),
    name,
    rule(x, y, width, height, colors.rule),
    square(x + 10, y + 10, 5, colors.mark),
    trophy(x + 36, y + (height - measured[2]) / 2, scale, best.rank, colors, ink)[0],
    label(x + 36 + measured[1] + 28, y + 32, best.title, colors.fg, 16, 0.3),
    label(x + 36 + measured[1] + 28, y + 54, commas(best.score), colors.muted, 13, 0.2),
    "</svg>",
  ].join("\n");
}

function regular(mode, colors, data, rows) {
  const [name] = dots("TROPHIES", 36, 16, colors.fg, 1.8);
  return [
    openSvg(mode, 495, 192, data.login + " trophies"),
    name,
    label(475, 30, "@" + data.login, colors.muted, 12, 0.2, "end"),
    plates(16, 48, 463, 128, rows, colors, 2.2, mode),
    "</svg>",
  ].join("\n");
}

function wide(mode, colors, data) {
  const [name] = dots("TROPHIES", 36, 16, colors.fg, 1.8);
  return [
    openSvg(mode, 896, 248, data.login + " trophies"),
    name,
    plates(16, 48, 864, 184, data.rows, colors, 2.2, mode),
    "</svg>",
  ].join("\n");
}

module.exports = { render };
