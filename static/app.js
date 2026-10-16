const portInput = document.getElementById("port");
const serviceSelect = document.getElementById("serviceSelect");
const hostInput = document.getElementById("host");
const form = document.getElementById("checkForm");
const submitButton = document.getElementById("submitButton");

serviceSelect?.addEventListener("change", () => {
  if (serviceSelect.value) portInput.value = serviceSelect.value;
});

document.querySelectorAll("[data-port]").forEach((button) => {
  button.addEventListener("click", () => {
    portInput.value = button.dataset.port;
    const matching = [...serviceSelect.options].find((o) => o.value === button.dataset.port);
    serviceSelect.value = matching ? matching.value : "";
    portInput.focus();
    document.querySelector(".checker-panel").scrollIntoView({ behavior: "smooth", block: "center" });
  });
});

form?.addEventListener("submit", () => {
  submitButton.disabled = true;
  submitButton.innerHTML = '<span class="loading-spinner"></span><span>Checking connection…</span>';
});
