# elfboi.io — site source

Static site. No framework, no build step at deploy time, no dependencies.
`python3 build.py` regenerates every `.html` file in this folder from
`build.py` plus `src/`. Hosting is Vercel, which serves `index.html` at the
root with no configuration.

To look at it: open `index.html` in a browser. Everything works from the
file system except the newsletter forms.

---

## READ THIS FIRST

**`tools-clipped-browser.html` is generated. Do not edit it.**

It is a verbatim copy of `src/clipped-web.html`, made every time
`build.py` runs. Edit `src/clipped-web.html` and run `python3 build.py`.
Anything typed into `tools-clipped-browser.html` is gone on the next build.

That one file is the whole Clipped Browser app — markup, styles, audio
engine and UI, about 110 KB, no imports. It is the file the backend work
happens in.

---

## Where the backend hooks are

Everything below is in `src/clipped-web.html` unless stated otherwise.

### 1. The daily limit is not enforced

```js
var DAILY = 20 * 60;    // ~line 863
var usedToday = 0;      // ~line 864
```

`usedToday` is an ordinary variable in memory. It is not persisted
anywhere — no `localStorage`, no cookie, no server call — so **refreshing
the page resets the quota to zero**. There is no fetch or XMLHttpRequest
anywhere in the app; nothing has ever talked to a server.

The UI around it is finished and correct: `paintQuota()` draws the meter,
`paintReset()` writes the "resets at midnight" line in the reader's own
time zone, and the over-limit refusal is at ~line 1284. It is only the
counting that needs somewhere real to live.

Worth knowing before choosing an approach: audio never leaves the browser.
Decoding and restoration both happen client-side via Web Audio, which is a
selling point on the page ("Your Audio — never uploaded"). Any quota scheme
should keep that true — send the server durations, not files.

### 2. Google AdSense — configured, dormant

```js
var ADSENSE = { pub: '', railLeft: '', railRight: '', banner: '' };   // ~line 495
```

`initAds()` does nothing while `pub` is empty. Fill in the publisher ID
(`ca-pub-…`) and the three ad unit slot IDs and it adds `ads` to `<body>`,
which is what gives the rails and the bottom banner their space, loads
Google's script, and reveals the note explaining the ads. Nothing else
needs changing.

Note the site is not AdSense-approved yet and will need an `ads.txt` at the
domain root before ads serve.

### 3. Newsletter

Kit (ConvertKit) form `9845746`, posted to directly from the markup. Only
the public form ID is in here — **no API key is in this repository, and
none should ever be added**, since every byte of a static site is readable
by any visitor. Anything needing the Kit API key belongs server-side.

### 4. Checkout

Lemon Squeezy links live in the `BUY` dict at the top of `build.py`. A
template or tool with no entry there renders as "coming soon" and is not a
link; add a URL and its tile becomes a link on the next build.

Currently only `film-surround` (the $39 5.1 template) has one.
**`clipped-pro` has no entry, so the Buy now button on `clipped.html`
still points at `#`.**

---

## Known placeholders

| What | Where |
|---|---|
| `VIDEO_ID` in YouTube embeds | `build.py` — tool pages, `learn.html`, template walkthroughs |
| `BUY["clipped-pro"]` | missing — Buy now on `clipped.html` goes to `#` |
| AdSense `pub` and the three slot ids | `src/clipped-web.html` ~line 495 |
| `SHOW_EMPTY_SLOTS = True` | `build.py` ~line 297 — flip to `False` at launch to hide the marked screenshot slots |
| `ads.txt` | not created yet; needs the publisher ID |

---

## Layout

```
build.py                  everything is generated from here
src/clipped-web.html      the Clipped Browser app (hand-maintained)
elfboi.css                all styles, numbered sections, tokens at the top
elfboi.js                 nav, filters, audio players, galleries
index.html                the home page
*.html                    28 generated pages
images/                   artwork, screenshots, video
audio/                    the six clipped/restored demo clips on clipped.html
audio/original/           Lien's untouched source files, not served — kept
                          for reference only, safe to delete from a deploy
```

`elfboi.css` is one file in numbered sections, newest last. A later section
can override an earlier one, and several deliberately do; the comments say
why where it matters.

---

## Deploying

Upload the folder. `index.html` is the entry point. Nothing needs to be
compiled, bundled or installed. `build.py` is for regenerating the HTML, not
for serving.

Excluded from this package, by `.gitignore`: `node_modules/`, `package*.json`,
`qa-fonts.css`, `fonts/` and `__pycache__/`. Those are QA scaffolding used
while checking rendering and are not part of the site.
