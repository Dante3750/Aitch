# DanteHelp

A small, readable ad blocker for Firefox and Chrome (Manifest V3).

**Status: v0.2.0, early.** It blocks about 43,000 known ad-server domains and hides
about 13,500 kinds of leftover ad slot, using the open EasyList data. It does not block
YouTube or Hotstar video ads.

## What it does

- **Network blocking** – blocks third-party requests to ad servers (`rules/ads.json`).
- **Slot hiding** – hides leftover ad containers (`content/selectors.js`, `content/cosmetic.js`).
- **On/off switch** – one toggle in the toolbar popup.

No tracking, no remote code, no account.

## Install (from source)

**Firefox:** open `about:debugging` → This Firefox → Load Temporary Add-on → pick `manifest.json`.

**Chrome:** open `chrome://extensions` → turn on Developer mode → Load unpacked → pick this folder.

## Layout

```
manifest.json          extension definition
rules/ads.json         network block rules (generated)
content/selectors.js   ad-slot selectors (generated)
content/cosmetic.js    applies the selectors
popup/                 toolbar popup with the on/off switch
tools/                 scripts that rebuild the generated files
```

## Updating the lists

Download `easylist_adservers.txt` and `easylist_general_hide.txt` from the
[EasyList repository](https://github.com/easylist/easylist/tree/master/easylist), then:

```
python3 tools/build_rules.py easylist_adservers.txt rules/ads.json
python3 tools/build_cosmetic.py easylist_general_hide.txt content/selectors.js
```

Add your own domains to `tools/extra_domains.txt` and selectors to
`tools/extra_selectors.txt`; the scripts merge them in.

## Licence

MIT for the code (see `LICENSE`). The generated rule files come from EasyList and keep its licence (see `NOTICE.md`).
