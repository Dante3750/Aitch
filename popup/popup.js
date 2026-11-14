const api = globalThis.browser ?? globalThis.chrome;
const toggle = document.getElementById("toggle");
const status = document.getElementById("status");

function render(enabled) {
  toggle.checked = enabled;
  status.textContent = enabled ? "Blocking ads" : "Paused";
}

api.storage.local.get({ enabled: true }).then(({ enabled }) => render(enabled));

toggle.addEventListener("change", async () => {
  const enabled = toggle.checked;
  await api.declarativeNetRequest.updateEnabledRulesets(
    enabled ? { enableRulesetIds: ["ads"] } : { disableRulesetIds: ["ads"] }
  );
  await api.storage.local.set({ enabled });
  render(enabled);
});
