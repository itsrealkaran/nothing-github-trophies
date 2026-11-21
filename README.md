# Trophies

Six ranks: stars, contributions, followers, issues, pull requests, and public repositories.

The grades are the GitHub Profile Trophy scale: C, B, A, AA, AAA, S, SS, SSS. A score below 1 leaves an empty frame. Contributions use that scale's commit cutoffs. The plates are flat squares.

| Rank | Stars | Contributions | Followers | Issues | Pulls | Repos |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| SSS | 2000 | 4000 | 1000 | 1000 | 1000 | 50 |
| SS | 700 | 2000 | 400 | 500 | 500 | 45 |
| S | 200 | 1000 | 200 | 200 | 200 | 40 |
| AAA | 100 | 500 | 100 | 100 | 100 | 35 |
| AA | 50 | 200 | 50 | 50 | 50 | 30 |
| A | 30 | 100 | 20 | 20 | 20 | 20 |
| B | 10 | 10 | 10 | 10 | 10 | 10 |
| C | 1 | 1 | 1 | 1 | 1 | 1 |

An SVG for a GitHub profile. Place the URL in a README, on a site, or anywhere an image is allowed.

## Contents

- [Usage](#usage)
- [Themes](#themes)
- [Sizes](#sizes)
- [Parameters](#parameters)
- [Examples](#examples)
- [Generate files](#generate-files)
- [Run locally](#run-locally)
- [Deploy](#deploy)
- [Configuration](#configuration)
- [Private data](#private-data)
- [Contributing](#contributing)

## Usage

```text
https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran
```

```md
![trophies](https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran)
```

Leave `theme` and `size` off for the classic regular card. An unknown username, theme, or size still returns an SVG, so the image slot in a README stays intact.

## Themes

| Theme | Background | Mark |
| --- | --- | --- |
| `classic` | Pure Black `#000000` | white |
| `classic-r` | Pure Black `#000000` | N-Red `#C8102E` |
| `white` | Pure White `#FFFFFF` | black |
| `white-r` | Pure White `#FFFFFF` | N-Red `#C8102E` |
| `light` | N-Grey `#DCD7D2` | N-Red `#C8102E` |
| `red` | Pure Black `#000000` | N-Red `#C8102E` |
| `blue` | Pure White `#FFFFFF` | N-Blue `#002F6C` |
| `yellow` | Pure Black `#000000` | N-Yellow `#FFC700` |

The title is a dot grid. Each category is a plate. A small square, the theme mark, sits in the corner of the plate. On `classic-r` and `white-r` that square is N-Red and the letter stays the cup color. On the other themes the letter is drawn in the accent. A double grade adds a smaller copy of that letter on the right. A triple grade adds one on each side. The shorter letters share the center letter's baseline, and the rank is centered in the disc. The trophy is a glass circle held by two arms, on a rectangular base the width of the single-letter award. The category and the score stay in monospace, centered at the bottom of the plate.

## Sizes

| Size | Dimensions | Contents |
| --- | --- | --- |
| `mini` | 220×148 | The strongest rank. |
| `compact` | 495px wide | That same rank. |
| `regular` | 495px wide | The top three. Default. |
| `wide` | 896px wide | All six, in category order. |

The files in `dist/` use the theme name, then the size: `classic-regular.svg`.

## Parameters

| Parameter | Required | Default | Purpose |
| --- | --- | --- | --- |
| `username` | yes |  | GitHub login. `user` is the same parameter. |
| `theme` | no | `classic` | One of the themes above. |
| `size` | no | `regular` | One of the sizes above. |

## Examples

Previews use `itsrealkaran`.

### classic

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic&size=mini`

![trophies classic mini](dist/itsrealkaran/classic-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic&size=compact`

![trophies classic compact](dist/itsrealkaran/classic-compact.svg)

#### regular

This is the default. You can leave `theme` and `size` off and get this card.

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic&size=regular`

![trophies classic regular](dist/itsrealkaran/classic-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic&size=wide`

![trophies classic wide](dist/itsrealkaran/classic-wide.svg)

### classic-r

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic-r&size=mini`

![trophies classic-r mini](dist/itsrealkaran/classic-r-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic-r&size=compact`

![trophies classic-r compact](dist/itsrealkaran/classic-r-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic-r&size=regular`

![trophies classic-r regular](dist/itsrealkaran/classic-r-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=classic-r&size=wide`

![trophies classic-r wide](dist/itsrealkaran/classic-r-wide.svg)

### white

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white&size=mini`

![trophies white mini](dist/itsrealkaran/white-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white&size=compact`

![trophies white compact](dist/itsrealkaran/white-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white&size=regular`

![trophies white regular](dist/itsrealkaran/white-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white&size=wide`

![trophies white wide](dist/itsrealkaran/white-wide.svg)

### white-r

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white-r&size=mini`

![trophies white-r mini](dist/itsrealkaran/white-r-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white-r&size=compact`

![trophies white-r compact](dist/itsrealkaran/white-r-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white-r&size=regular`

![trophies white-r regular](dist/itsrealkaran/white-r-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=white-r&size=wide`

![trophies white-r wide](dist/itsrealkaran/white-r-wide.svg)

### light

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=light&size=mini`

![trophies light mini](dist/itsrealkaran/light-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=light&size=compact`

![trophies light compact](dist/itsrealkaran/light-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=light&size=regular`

![trophies light regular](dist/itsrealkaran/light-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=light&size=wide`

![trophies light wide](dist/itsrealkaran/light-wide.svg)

### red

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=red&size=mini`

![trophies red mini](dist/itsrealkaran/red-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=red&size=compact`

![trophies red compact](dist/itsrealkaran/red-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=red&size=regular`

![trophies red regular](dist/itsrealkaran/red-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=red&size=wide`

![trophies red wide](dist/itsrealkaran/red-wide.svg)

### blue

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=blue&size=mini`

![trophies blue mini](dist/itsrealkaran/blue-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=blue&size=compact`

![trophies blue compact](dist/itsrealkaran/blue-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=blue&size=regular`

![trophies blue regular](dist/itsrealkaran/blue-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=blue&size=wide`

![trophies blue wide](dist/itsrealkaran/blue-wide.svg)

### yellow

#### mini

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=yellow&size=mini`

![trophies yellow mini](dist/itsrealkaran/yellow-mini.svg)

#### compact

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=yellow&size=compact`

![trophies yellow compact](dist/itsrealkaran/yellow-compact.svg)

#### regular

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=yellow&size=regular`

![trophies yellow regular](dist/itsrealkaran/yellow-regular.svg)

#### wide

`https://github.com/itsrealkaran/nothing-github-trophies?username=itsrealkaran&theme=yellow&size=wide`

![trophies yellow wide](dist/itsrealkaran/yellow-wide.svg)

## Generate files

Write the SVG files into the repo when you want a fixed picture instead of a live URL.

```bash
python3 render.py itsrealkaran
```

Python 3 is enough. There is no package to install. Files land in `dist/<login>/`. Public numbers use `gh` when it is signed in on that machine, or `GH_TOKEN` / `GITHUB_TOKEN`.

## Run locally

The Python container and the Node server use the same path and the same query.

### Python container

```bash
docker build -t trophies .
docker run --env GH_TOKEN --env PORT=8080 -p 8080:8080 trophies
```

If the token is in a local `.env` file, pass that file instead:

```bash
docker run --env-file .env --env PORT=8080 -p 8080:8080 trophies
```

The container runs `serve.py`. Open `http://127.0.0.1:8080/trophies?username=itsrealkaran`.

The image does not include the `gh` command. Set `GH_TOKEN` when you start it. Without a token, GitHub allows about 60 requests an hour.

### Node

```bash
node server.js
```

The server listens on port `8080`. It reads `GH_TOKEN` from the environment, or from a `.env` file in this folder. `python3 render.py` remains the command that writes `dist/`.

Vercel and Netlify can host `server.js`. Set `GH_TOKEN` on the project. `vercel.json` is included. A free function has a short time limit. Use the Python container when a request needs longer than that limit.

## Deploy

Fork this repo for your own host. Your copy stays awake if a shared deploy sleeps, your traffic stays off a shared GitHub limit, and you can add a token for your own counts.

1. Fork the repo.
2. Deploy the Dockerfile on Fly, Railway, Render, Cloud Run, or a virtual machine. Or deploy `server.js` on Vercel or Netlify.
3. Set the variables below as secrets. Do not commit them.
4. Open `https://github.com/itsrealkaran/nothing-github-trophies?username=yourname`.

Use that address in the image URL. The query stays the same.

## Configuration

| Variable | Required | Purpose |
| --- | --- | --- |
| `GH_TOKEN` | for a public server | GitHub token. `GITHUB_TOKEN` is the same variable. |
| `PORT` | no | Listen port. Default `8080`. |
| `CARD_CACHE_SECONDS` | no | How long a finished SVG is reused. Default `3600`. |

### Create a token

1. On GitHub, open Settings, then Developer settings, then Personal access tokens, then Tokens (classic).
2. Generate a new token.
3. Public cards need no extra scopes. The token raises the server limit from about 60 requests an hour to 5,000.
4. To include your own private counts, add the `repo` scope. The token account must match `username`.
5. Set the value as `GH_TOKEN` on the host. Do not put it in the image URL, this README, or git.

## Private data

Followers, issues, pull requests, and the repository rank use public data. The repository rank counts public repositories, so a private repository count is never shown.

Stars include private repositories only when `GH_TOKEN` belongs to that username. The contribution rank adds private contributions for that same token. Give the token the `repo` scope. Private repository names are never drawn.

## Contributing

This folder is the card: the drawing, the GitHub fetch, and both servers.

1. Fork the repo and edit `render.py`, or the files beside it when the change is the data or the colours.
2. Draw a sample with `python3 render.py yourname` and open `dist/yourname/`.
3. The live routes use that same drawing.
4. Do not commit a token, a `.env` file, or a private repository name.
5. Open a pull request and name the theme and size you checked.
