# DanteHelp

A small, readable ad blocker for Firefox and Chrome (Manifest V3).

**Status: v0.3.0, early.** Built on the open EasyList data: about 44,900 ad-server
domains, 2,300 path rules, 480 exceptions that keep sites working, and 13,500 kinds of
leftover ad slot. It does not block YouTube or Hotstar video ads.

## What it does

- **Network blocking** – blocks requests to ad servers and known ad paths (`rules/ads.json`).
- **Exceptions** – EasyList's allow rules are honoured, so fewer sites break.
- **Slot hiding** – hides leftover ad containers (`content/selectors.js`, `content/cosmetic.js`).
- **Pause on one site** – a per-site switch in the popup, next to the main on/off switch.

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

Download the list files from the
[EasyList repository](https://github.com/easylist/easylist/tree/master/easylist), then:

```
python3 tools/build_rules.py rules/ads.json easylist_adservers.txt easylist_thirdparty.txt \
    easylist_general_block.txt easylist_specific_block.txt easylist_allowlist.txt
python3 tools/build_cosmetic.py easylist_general_hide.txt content/selectors.js
```

Add your own domains to `tools/extra_domains.txt` and selectors to
`tools/extra_selectors.txt`; the scripts merge them in.

## Licence

MIT for the code (see `LICENSE`). The generated rule files come from EasyList and keep its licence (see `NOTICE.md`).
