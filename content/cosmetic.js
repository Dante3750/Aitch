// DanteHelp: hides leftover ad slots after the network rules block the ad itself.
(() => {
  const api = globalThis.browser ?? globalThis.chrome;
  const SELECTORS = globalThis.DANTEHELP_SELECTORS ?? [];
  const STYLE_ID = "dantehelp-cosmetic";
  const CHUNK = 200; // one bad selector only disables its own chunk

  function css() {
    const parts = [];
    for (let i = 0; i < SELECTORS.length; i += CHUNK) {
      parts.push(SELECTORS.slice(i, i + CHUNK).join(",") + "{display:none!important}");
    }
    return parts.join("\n");
  }

  function apply() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement("style");
    style.id = STYLE_ID;
    style.textContent = css();
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
