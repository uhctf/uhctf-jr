// Wie is de hacker? Een digitaal potlood: klik op "Schrap" om een verdachte door te strepen en op een verklaring om die af te vinken.
// De pagina controleert niets en kent de hacker niet: jij bepaalt wie overblijft.
const schrap = new Set(), gebruikt = new Set();
const tabel = $("verdachten");
const kop = document.createElement("tr");
for (const k of DATA.kolommen) { const th = document.createElement("th"); th.textContent = k; kop.appendChild(th); }
kop.appendChild(document.createElement("th"));
tabel.appendChild(kop);
DATA.verdachten.forEach((v, i) => {
  const tr = document.createElement("tr"); tr.id = "v-" + i;
  for (const cel of v) { const td = document.createElement("td"); td.textContent = cel; tr.appendChild(td); }
  const td = document.createElement("td");
  td.innerHTML = "<button type='button' class='schrap'>Schrap</button>";
  td.querySelector(".schrap").addEventListener("click", () => { schrap.has(i) ? schrap.delete(i) : schrap.add(i); toon(); });
  tr.appendChild(td); tabel.appendChild(tr);
});
const lijst = $("verklaringen");
DATA.verklaringen.forEach((tekst, i) => {
  const li = document.createElement("li");
  li.innerHTML = "<button type='button' class='verklaring'></button>";
  li.querySelector("button").textContent = tekst;
  li.querySelector("button").addEventListener("click", () => { gebruikt.has(i) ? gebruikt.delete(i) : gebruikt.add(i); toon(); });
  lijst.appendChild(li);
});
function toon() {
  DATA.verdachten.forEach((v, i) => $("v-" + i).classList.toggle("geschrapt", schrap.has(i)));
  [...lijst.children].forEach((li, i) => li.querySelector("button").classList.toggle("gebruikt", gebruikt.has(i)));
  $("over").textContent = (DATA.verdachten.length - schrap.size) + " over";
}
$("wis").addEventListener("click", () => { schrap.clear(); gebruikt.clear(); toon(); });
toon();
