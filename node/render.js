"use strict";

const { dots, label, openSvg } = require("./frame");
const { theme } = require("./nothing");
const { commas } = require("./format");

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

function mini(mode, colors, data, best) {
  const [name] = dots("TROPHIES", 28, 12, colors.fg, 1.15);
  return [
    openSvg(mode, 220, 148, data.login + " trophies", 6, 14),
    name,
    label(16, 96, best.rank, colors.figure, 32, -0.8),
    label(16, 118, best.title, colors.fg, 13, 0.1),
    label(16, 136, commas(best.score), colors.muted, 12, 0.2),
    "</svg>",
  ].join("\n");
}

function compact(mode, colors, data, best) {
  const [name] = dots("TROPHIES", 40, 16, colors.fg, 1.8);
  return [
    openSvg(mode, 495, 132, data.login + " trophies"),
    name,
    label(20, 108, best.rank, colors.figure, 42, -1),
    label(160, 90, best.title, colors.fg, 16, 0.2),
    label(160, 112, commas(best.score), colors.muted, 13, 0.2),
    "</svg>",
  ].join("\n");
}

function regular(mode, colors, data, rows) {
  const [name] = dots("TROPHIES", 40, 16, colors.fg, 1.8);
  const parts = [openSvg(mode, 495, 195, data.login + " trophies"), name];
  rows.forEach((row, index) => {
    const x = 20 + index * 155;
    parts.push(label(x, 112, row.rank, colors.figure, 32, -0.8));
    parts.push(label(x, 138, row.title, colors.fg, 13, 0.2));
    parts.push(label(x, 156, commas(row.score), colors.muted, 12, 0.2));
  });
  parts.push(`<line x1="20" y1="168" x2="475" y2="168" stroke="${colors.rule}"/>`);
  parts.push(label(20, 186, "@" + data.login, colors.fg, 12, 0.2));
  parts.push("</svg>");
  return parts.join("\n");
}

function wide(mode, colors, data) {
  const [name] = dots("TROPHIES", 40, 16, colors.fg, 1.8);
  const parts = [openSvg(mode, 896, 248, data.login + " trophies"), name];
  data.rows.forEach((row, index) => {
    const x = 20 + index * 146;
    parts.push(`<rect x="${x}" y="78" width="134" height="148" fill="none" stroke="${colors.rule}"/>`);
    parts.push(`<rect x="${x + 12}" y="92" width="8" height="8" fill="${colors.mark}"/>`);
    parts.push(label(x + 12, 150, row.rank, colors.figure, 28, -0.6));
    parts.push(label(x + 12, 176, row.title, colors.fg, 13, 0.2));
    parts.push(label(x + 12, 198, commas(row.score), colors.muted, 12, 0.2));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

module.exports = { render };
