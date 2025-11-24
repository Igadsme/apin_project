const API_BASE = "http://127.0.0.1:8000";

async function fetchAvailability() {
  const statusEl = document.getElementById("status");
  const tableEl = document.getElementById("availability-table");
  const bodyEl = document.getElementById("availability-body");

  try {
    statusEl.textContent = "Loading live data from backend...";
    const res = await fetch(`${API_BASE}/availability`);
    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }
    const data = await res.json();

    bodyEl.innerHTML = "";
    if (!Array.isArray(data) || data.length === 0) {
      statusEl.textContent = "No lots found yet. Seed the database and refresh.";
      tableEl.classList.add("hidden");
      return;
    }

    data.forEach((lot) => {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${lot.lot_name}</td>
        <td>${lot.total_spots}</td>
        <td><span class="badge badge-free">${lot.free_spots}</span></td>
        <td><span class="badge badge-occupied">${lot.occupied_spots}</span></td>
        <td><span class="badge badge-unknown">${lot.unknown_spots}</span></td>
      `;

      bodyEl.appendChild(tr);
    });

    statusEl.textContent = "Connected to backend. Data refreshes every 5 seconds.";
    tableEl.classList.remove("hidden");
  } catch (err) {
    console.error(err);
    statusEl.textContent = "Error: unable to reach backend. Is FastAPI running on port 8000?";
    tableEl.classList.add("hidden");
  }
}

fetchAvailability();
setInterval(fetchAvailability, 5000);
