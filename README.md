# DanteHelp

A small, readable ad blocker for Firefox and Chrome (Manifest V3).

**Status: v0.1.0, early.** It blocks common third-party ad servers and hides the
empty slots they leave behind. It does not block YouTube or Hotstar video ads.

## What it does

- **Network blocking** – blocks requests to 23 common ad servers (`rules/ads.json`).
- **Slot hiding** – hides leftover ad containers (`content/cosmetic.js`).
- **On/off switch** – one toggle in the toolbar popup.

No tracking, no remote code, no account. The whole extension is about 150 lines.

## Install (from source)

**Firefox:** open `about:debugging` → This Firefox → Load Temporary Add-on → pick `manifest.json`.

**Chrome:** open `chrome://extensions` → turn on Developer mode → Load unpacked → pick this folder.

## Layout

```
manifest.json        extension definition
rules/ads.json       network block rules
content/cosmetic.js  hides leftover ad slots
popup/               toolbar popup with the on/off switch
```

## Contributing

Add ad domains to `rules/ads.json` or selectors to `content/cosmetic.js`.
Keep selectors narrow; broad ones break real sites.

## Licence

MIT. See `LICENSE`.
