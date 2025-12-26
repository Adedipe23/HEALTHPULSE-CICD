const form = document.getElementById("vitalsForm");
const resultEl = document.getElementById("result");
const errorEl = document.getElementById("error");
const historyEl = document.getElementById("history");
const refreshBtn = document.getElementById("refreshBtn");

function showError(msg) {
  errorEl.textContent = msg;
  errorEl.classList.remove("hidden");
}

function clearError() {
  errorEl.textContent = "";
  errorEl.classList.add("hidden");
}

function showResult(data) {
  const badge = `<span class="badge">${data.overallStatus}</span>`;
  const notes = data.notes.map(n => `<li>${n}</li>`).join("");
  resultEl.innerHTML = `
    <strong>Overall status:</strong> ${badge}
    <ul>${notes}</ul>
  `;
  resultEl.classList.remove("hidden");
}

function toNumber(id) {
  return Number(document.getElementById(id).value);
}

async function loadHistory() {
  try {
    const r = await fetch("/api/v1/history");
    if (!r.ok) throw new Error(`History request failed: ${r.status}`);
    const data = await r.json();

    historyEl.innerHTML = (data.items || []).map(item => {
      const i = item.input;
      return `
        <div class="item">
          <div>
            <strong>${item.overallStatus}</strong>
            <span class="badge">${new Date(item.timestamp).toLocaleString()}</span>
          </div>
          <div class="meta">
            HR: ${i.heartRate} bpm · BP: ${i.systolic}/${i.diastolic} · Temp: ${i.temperatureC}°C · SpO₂: ${i.spo2}%
          </div>
        </div>
      `;
    }).join("") || `<p class="meta">No checks yet.</p>`;
  } catch (e) {
    showError("Cannot reach backend. Is the stack running?");
    console.error(e);
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearError();

  const payload = {
    heartRate: toNumber("heartRate"),
    systolic: toNumber("systolic"),
    diastolic: toNumber("diastolic"),
    temperatureC: toNumber("temperatureC"),
    spo2: toNumber("spo2")
  };

  try {
    const r = await fetch("/api/v1/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });

    const data = await r.json();
    if (!r.ok) throw new Error(data.error || "Request failed");

    showResult(data);
    await loadHistory();
  } catch (e) {
    showError(e.message || "Request failed");
    console.error(e);
  }
});

refreshBtn.addEventListener("click", loadHistory);

// Auto-refresh dashboard every 15s (nice for “changes visible quickly” demos)
setInterval(loadHistory, 15000);
loadHistory();
