# elfboi.io — site source

Static site on Vercel. `python3 build.py` generates the root HTML pages from
`build.py` and `src/`; Vercel runs that command on deployment. No framework or
package installation is required.

**Edit `src/clipped-web.html`, not generated `tools-clipped-browser.html`.**
The page retains the existing design, static copy and controls. Its small
`src/clipped-api.mjs` module handles the Declip API and durable job lifecycle.
Static copy corrections are deferred to the designer.

## Clipped Browser integration

The browser uses same-origin `/api/declip/*` through the routes in `vercel.json`.
Audio uploads, playback and downloads go directly to private R2 using short-lived
signed URLs. The original file is uploaded without requiring a full browser
decode; metadata-only duration lookup has a short timeout and a null fallback.
The server verifies duration and enforces quotas. There is no local restoration
fallback and no comparison player.

One active job and up to ten bank references persist in this browser. Refresh or
a lost connection resumes the same remote job. Retry keeps the same create
request and uploaded file; queued/running work cannot be cancelled by removing
local state. Files expire 24 hours after job creation. Bank playback uses one
streaming media element rather than decoding long WAVs into memory. Removing a
bank row removes its local reference only. Cookie loss can prevent recovery.

The backend is https://github.com/a-n-t-h-o-n-y/declip-backend-2.
See its [integration and cutover guide](https://github.com/a-n-t-h-o-n-y/declip-backend-2/blob/elfboi-backend-integration/docs/elfboi-integration.md)
for the paired branch and production verification still required. The main
configuration steps are:

- Set the Vercel production environment variable `DECLIP_PROXY_SECRET` to the
  same private random value as the Worker's `VERCEL_PROXY_SECRET` (32+ characters).
  The route overwrites `X-Declip-Proxy-Secret` on the server; never put its value
  in browser code, Git or response headers.
- At cutover set Worker `PUBLIC_API_PROXY=vercel`, set `APP_ORIGIN` to the exact
  canonical website origin, and configure matching Turnstile hostname and R2
  CORS. Verify apex/www redirects first. Production API requests fail closed if
  the proxy secret or Vercel visitor address is missing/invalid.
- Keep signed Modal callbacks on the Worker origin. The site route excludes
  internal callbacks, local object endpoints and comparison endpoints. Ordinary
  site pages, newsletter forms and static build settings retain their behavior.
- Do not give ordinary Vercel previews production secret access or wildcard
  production origin permissions. Use mocked API responses for visual previews.

## Build and checks

```sh
python3 build.py
node --test tests/*.test.mjs
python3 -m http.server 8000
```

Open `http://localhost:8000/` for static previews. The Python preview server does
not implement `/api/declip`; live processing needs the configured Vercel route
and backend. The tests use in-memory API fixtures to cover upload, asynchronous
inspection, queues, refresh, uncertain responses, retries and expiring grants.

The canvas remains a decorative progress animation. Browser progress reflects
upload bytes or restoration chunks; waiting and saving are indeterminate.
Minimal recovery controls use the existing styling and appear only when needed.

## Other integrations

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

## Source layout

- `build.py`: page generation and tool/catalog content.
- `src/clipped-web.html`: Clipped Browser markup, styling and presentation.
- `src/clipped-api.mjs`: Declip session, uploads, saved jobs and recovery.
- `elfboi.css`, `elfboi.js`: shared site styling and interactions.
- `images/`, `audio/`: artwork and demo clips.
- `tests/clipped-api.test.mjs`: focused API client and route regression checks.

Generated root HTML, local dependencies and QA screenshots are ignored by Git.
Keep private configuration outside the public output directory.

## Known placeholders

`VIDEO_ID` embeds, most `BUY` entries including `clipped-pro`, AdSense publisher
and slot IDs, and `ads.txt` still need their launch values. `SHOW_EMPTY_SLOTS` in
`build.py` controls the marked screenshot placeholders. These are independent of
the backend integration.
