// Wachtwoord-mastermind: kies dingen uit het profiel en druk op Gok. De pagina neemt de rol van de begeleider over en zegt per vak: juist, fout of juist maar op de verkeerde plaats.
// Ze zegt nooit of je het wachtwoord gevonden hebt: dat zie je zelf aan de feedback. Onderaan staat de tekst van je gok, om in de kluis te typen.
const n = DATA.lengte;
let gok = [];        // gekozen items (indexen in het profiel)
let geschiedenis = [];  // { gok, feedback }
const geheim = DATA.geheim;

const profiel = $("profiel");
DATA.items.forEach((item, i) => {
  const k = document.createElement("button");
  k.type = "button"; k.className = "item"; k.dataset.i = i;
  k.innerHTML = "<span class='badge'></span><span class='label'></span><span class='waarde'></span>";
  k.querySelector(".badge").textContent = item.letter;
  k.querySelector(".label").textContent = item.label;
  k.querySelector(".waarde").textContent = item.waarde;
  k.addEventListener("click", () => { if (gok.length < n) { gok.push(i); toon(); } });
  profiel.appendChild(k);
});

function feedback(g) {
  return g.map((x, p) => (geheim[p] === x ? "juist" : geheim.includes(x) ? "plaats" : "fout"));
}
const SYMBOOL = { juist: "✓ juist", fout: "✗ fout", plaats: "⇄ verkeerde plaats" };
const tekstVan = (g) => g.map((i) => DATA.items[i].waarde).join("");

function rij(g, fb) {
  const d = document.createElement("div");
  d.className = "gokrij";
  g.forEach((x, p) => {
    const v = document.createElement("div");
    v.className = "vakje " + (fb ? fb[p] : "");
    v.innerHTML = "<strong></strong><span class='klein'></span>";
    v.querySelector("strong").textContent = DATA.items[x].letter;
    v.querySelector("span").textContent = fb ? SYMBOOL[fb[p]] : "";
    d.appendChild(v);
  });
  return d;
}
function toon() {
  const nu = $("nu"); nu.innerHTML = "";
  for (let p = 0; p < n; p++) {
    const v = document.createElement("button");
    v.type = "button"; v.className = "vakje leeg" + (p < gok.length ? " gevuld" : "");
    v.textContent = p < gok.length ? DATA.items[gok[p]].letter : "?";
    v.setAttribute("aria-label", p < gok.length ? "Verwijder " + DATA.items[gok[p]].letter : "Leeg vak");
    v.addEventListener("click", () => { if (p < gok.length) { gok.splice(p, 1); toon(); } });
    nu.appendChild(v);
  }
  $("gok").disabled = gok.length !== n;
  const hist = $("historiek"); hist.innerHTML = "";
  geschiedenis.forEach((h, i) => { const r = rij(h.gok, h.feedback); const nr = document.createElement("div"); nr.className = "nr"; nr.textContent = i + 1; r.prepend(nr); hist.appendChild(r); });
  const laatste = geschiedenis.length ? geschiedenis[geschiedenis.length - 1] : null;
  $("tekst-gok").textContent = tekstVan(gok.length === n ? gok : laatste ? laatste.gok : []) || "\u2013";
}
$("gok").addEventListener("click", () => {
  if (gok.length !== n) return;
  geschiedenis.push({ gok: gok.slice(), feedback: feedback(gok) });
  gok = []; toon();
});
$("wis").addEventListener("click", () => { gok = []; toon(); });
$("opnieuw").addEventListener("click", () => { gok = []; geschiedenis = []; toon(); });
toon();
