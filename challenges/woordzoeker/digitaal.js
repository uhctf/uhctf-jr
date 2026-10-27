// Woordzoeker: een digitaal potlood. Klik op letters om ze te markeren (nog eens klikken haalt de markering weg) en klik op een woord in de lijst om het door te strepen.
// De pagina controleert niets: onderaan staan gewoon de letters die je niet gemarkeerd hebt.
const raster = DATA.raster, n = raster.length;
const gemarkeerd = new Set();
const grid = $("raster");
grid.style.gridTemplateColumns = "repeat(" + n + ", 1fr)";
const knoppen = [];
for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) {
  const k = document.createElement("button");
  k.type = "button"; k.className = "cel"; k.textContent = raster[r][c];
  k.addEventListener("click", () => {
    const sleutel = r + "," + c;
    gemarkeerd.has(sleutel) ? gemarkeerd.delete(sleutel) : gemarkeerd.add(sleutel);
    toon();
  });
  grid.appendChild(k); knoppen.push(k);
}
const lijst = $("woorden");
for (const w of DATA.woorden) {
  const li = document.createElement("li");
  li.innerHTML = "<button type='button' class='woord'></button>";
  li.querySelector("button").textContent = w;
  li.querySelector("button").addEventListener("click", (e) => e.currentTarget.classList.toggle("klaar"));
  lijst.appendChild(li);
}
function toon() {
  knoppen.forEach((k, i) => k.classList.toggle("gevonden", gemarkeerd.has(Math.floor(i / n) + "," + (i % n))));
  let rest = "";
  for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (!gemarkeerd.has(r + "," + c)) rest += raster[r][c];
  $("rest").textContent = rest;
}
$("wis").addEventListener("click", () => { gemarkeerd.clear(); toon(); });
toon();
