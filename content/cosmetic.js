// DanteHelp: hides leftover ad slots after the network rules block the ad itself.
(() => {
  const api = globalThis.browser ?? globalThis.chrome;

  // Kept deliberately narrow: broad selectors like [class*="ad"] break real sites.
  const SELECTORS = [
    "ins.adsbygoogle",
    "iframe[src*='doubleclick.net']",
    "iframe[src*='googlesyndication.com']",
    "iframe[id^='google_ads_iframe']",
    "div[id^='google_ads_iframe']",
    "div[id^='div-gpt-ad']",
    "div[data-google-query-id]",
    "div[id^='taboola-']",
    "div[class^='trc_rbox']",
    "div.OUTBRAIN",
    "div[data-ad-slot]",
    "div[data-ad-unit]",
    "amp-ad",
    "amp-embed[type='taboola']"
  ];

  const STYLE_ID = "dantehelp-cosmetic";

  function apply() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = SELECTORS.join(",\n") + " { display: none !important; }";
    (document.head || document.documentElement).appendChild(style);
  }

  function remove() {
    document.getElementById(STYLE_ID)?.remove();
  }

  api.storage.local.get({ enabled: true }).then(({ enabled }) => {
    if (enabled) apply();
  });

  api.storage.onChanged.addListener((changes, area) => {
    if (area !== "local" || !changes.enabled) return;
    changes.enabled.newValue ? apply() : remove();
  });
})();
