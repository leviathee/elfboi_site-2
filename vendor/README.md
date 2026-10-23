# Browser audio preview dependency

`mediabunny-preview.mjs` is a minified, input-only facade built from
[Mediabunny 1.62.1](https://github.com/Vanilagy/mediabunny/tree/v1.62.1) with
esbuild 0.28.2. It is about 272 KiB (73 KiB gzipped), self-hosted and loaded only
inside the optional preview worker. There is no CDN request or npm install in
the website's normal build/deploy flow.

Mediabunny is copyright Vanilagy, licensed under MPL-2.0; see
[the included license](mediabunny-LICENSE.txt). The complete corresponding
upstream source is available in the [published source package](https://registry.npmjs.org/mediabunny/-/mediabunny-1.62.1.tgz)
(`src/` and `dist/modules/`). No upstream source is modified. The small export
facade used to build this artifact is checked in beside it.

SHA-256 of `mediabunny-preview.mjs`:
`2637f6903a2b65598e9d215e3095b0d237838e3e686966f6ce9beb8b4bc14648`

To intentionally update/regenerate it, from the repository root (requires npm
only for this maintenance operation):

```sh
preview_repo="$PWD"
preview_build="$(mktemp -d)"
npm install --prefix "$preview_build" --ignore-scripts --no-audit --no-fund mediabunny@1.62.1 esbuild@0.28.2
cp vendor/mediabunny-preview-entry.mjs "$preview_build/entry.mjs"
(cd "$preview_build" && ./node_modules/.bin/esbuild entry.mjs --bundle --minify --format=esm --platform=browser --target=es2022 --legal-comments=eof --outfile="$preview_repo/vendor/mediabunny-preview.mjs")
cp "$preview_build/node_modules/mediabunny/LICENSE" vendor/mediabunny-LICENSE.txt
shasum -a 256 vendor/mediabunny-preview.mjs
node --test tests/*.test.mjs
```

Update the recorded version/hash when changing the dependency. Check actual
compressed files in a browser as well; Node tests exercise PCM parsing and the
application lifecycle, but do not supply browser WebCodecs decoders.
