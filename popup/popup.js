const api = globalThis.browser ?? globalThis.chrome;
const toggle = document.getElementById("toggle");
const siteToggle = document.getElementById("site-toggle");
const siteRow = document.getElementById("site-row");
const status = document.getElementById("status");
const PAUSE_RULE_BASE = 1000000; // dynamic rule ids, kept clear of the static ones

let host = null;

function render(enabled, pausedSites) {
  toggle.checked = enabled;
  siteToggle.checked = !pausedSites.includes(host);
  siteToggle.disabled = !enabled;
  status.textContent = !enabled ? "Paused everywhere"
    : host && pausedSites.includes(host) ? "Paused on this site" : "Blocking ads";
}

async function load() {
  return api.storage.local.get({ enabled: true, pausedSites: [] });
}

// Rewrites the "paused sites" allow rules so they match the stored list.
async function setPaused(site, paused) {
  const { pausedSites } = await load();
  const next = pausedSites.filter((s) => s !== site);
  if (paused) next.push(site);
  const old = await api.declarativeNetRequest.getDynamicRules();
  await api.declarativeNetRequest.updateDynamicRules({
    removeRuleIds: old.map((r) => r.id),
    addRules: next.map((s, i) => ({
      id: PAUSE_RULE_BASE + i,
      priority: 100,
      action: { type: "allowAllRequests" },
      condition: { requestDomains: [s], resourceTypes: ["main_frame"] }
    }))
  });
  await api.storage.local.set({ pausedSites: next });
  return next;
}

async function init() {
  try {
    const [tab] = await api.tabs.query({ active: true, currentWindow: true });
    const url = new URL(tab.url);
    if (url.protocol === "http:" || url.protocol === "https:") {
      host = url.hostname;
      document.getElementById("site").textContent = host;
      siteRow.hidden = false;
    }
  } catch {}
  const { enabled, pausedSites } = await load();
  render(enabled, pausedSites);
}

toggle.addEventListener("change", async () => {
  const enabled = toggle.checked;
  await api.declarativeNetRequest.updateEnabledRulesets(
    enabled ? { enableRulesetIds: ["ads"] } : { disableRulesetIds: ["ads"] }
  );
  await api.storage.local.set({ enabled });
  render(enabled, (await load()).pausedSites);
});

siteToggle.addEventListener("change", async () => {
  const pausedSites = await setPaused(host, !siteToggle.checked);
  render(toggle.checked, pausedSites);
});

init();
