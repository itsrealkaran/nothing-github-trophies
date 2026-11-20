"use strict";

const { dots, label, openSvg, trophy } = require("./frame");
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

function letters(rank) {
  return ["SSS", "SS", "S", "AAA", "AA", "A", "B", "C"].includes(rank) ? rank.length : 1;
}

function rankScale(size, rank) {
  const table = {
    mini: [2.8, 2.3, 1.9],
    compact: [3.2, 2.6, 2.2],
    regular: [2.6, 2.2, 1.8],
    wide: [2.7, 2.2, 1.8],
  };
  return table[size][letters(rank) - 1];
}

function cup(x, y, scale, row, colors) {
  return trophy(x, y, scale, row.rank, colors);
}

function mini(mode, colors, data, best) {
  const [name] = dots("TROPHIES", 28, 12, colors.fg, 1.15);
  return [
    openSvg(mode, 220, 148, data.login + " trophies", 6, 14),
    name,
    cup(16, 46, rankScale("mini", best.rank), best, colors)[0],
    label(100, 86, best.title, colors.fg, 14, 0.1),
    label(100, 108, commas(best.score), colors.muted, 12, 0.2),
    "</svg>",
  ].join("\n");
}

function compact(mode, colors, data, best) {
  const [name] = dots("TROPHIES", 40, 16, colors.fg, 1.8);
  return [
    openSvg(mode, 495, 132, data.login + " trophies"),
    name,
    cup(20, 44, rankScale("compact", best.rank), best, colors)[0],
    label(120, 86, best.title, colors.fg, 16, 0.2),
    label(120, 110, commas(best.score), colors.muted, 13, 0.2),
    "</svg>",
  ].join("\n");
}

function regular(mode, colors, data, rows) {
  const [name] = dots("TROPHIES", 40, 16, colors.fg, 1.8);
  const parts = [openSvg(mode, 495, 192, data.login + " trophies"), name];
  const tall = trophy(0, 0, rankScale("regular", "A"), "A", colors)[2];
  const bottom = 48 + tall;
  rows.forEach((row, index) => {
    const x = 20 + index * 155;
    const scale = rankScale("regular", row.rank);
    const measured = trophy(0, 0, scale, row.rank, colors);
    parts.push(cup(x + (130 - measured[1]) / 2, bottom - measured[2], scale, row, colors)[0]);
    parts.push(label(x, 122, row.title, colors.fg, 13, 0.2));
    parts.push(label(x, 142, commas(row.score), colors.muted, 12, 0.2));
  });
  parts.push(`<line x1="20" y1="160" x2="475" y2="160" stroke="${colors.rule}"/>`);
  parts.push(label(20, 178, "@" + data.login, colors.fg, 12, 0.2));
  parts.push("</svg>");
  return parts.join("\n");
}

function wide(mode, colors, data) {
  const [name] = dots("TROPHIES", 40, 16, colors.fg, 1.8);
  const parts = [openSvg(mode, 896, 248, data.login + " trophies"), name];
  const tall = trophy(0, 0, rankScale("wide", "A"), "A", colors)[2];
  const bottom = 84 + tall;
  data.rows.forEach((row, index) => {
    const x = 20 + index * 146;
    const scale = rankScale("wide", row.rank);
    const measured = trophy(0, 0, scale, row.rank, colors);
    parts.push(`<rect x="${x}" y="72" width="134" height="156" fill="none" stroke="${colors.rule}"/>`);
    parts.push(cup(x + (134 - measured[1]) / 2, bottom - measured[2], scale, row, colors)[0]);
    parts.push(label(x + 12, 168, row.title, colors.fg, 13, 0.2));
    parts.push(label(x + 12, 190, commas(row.score), colors.muted, 12, 0.2));
  });
  parts.push("</svg>");
  return parts.join("\n");
}

module.exports = { render };
