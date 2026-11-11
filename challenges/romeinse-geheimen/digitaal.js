// Romeinse geheimen: een hulpmiddel. Draai de binnenste ring, tik een woord in en het wiel vertaalt het met de gekozen verschuiving.
const ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let verschuiving = 0;
const svg = $("wiel");
const NS = "http://www.w3.org/2000/svg";
function tekst(x, y, inhoud, klasse) {
  const t = document.createElementNS(NS, "text");
  t.setAttribute("x", x); t.setAttribute("y", y); t.setAttribute("class", klasse);
  t.setAttribute("text-anchor", "middle"); t.setAttribute("dominant-baseline", "central");
  t.textContent = inhoud; svg.appendChild(t); return t;
}
const binnen = [];
for (let i = 0; i < 26; i++) {
  const hoek = (i / 26) * 2 * Math.PI - Math.PI / 2;
  tekst(160 + 138 * Math.cos(hoek), 160 + 138 * Math.sin(hoek), ABC[i], "buiten");
  binnen.push(tekst(160 + 100 * Math.cos(hoek), 160 + 100 * Math.sin(hoek), ABC[i], "binnen"));
}
for (const r of [80, 120, 152]) {  // klein naar groot, elk vooraan toegevoegd: de grootste ligt dus onderaan
  const c = document.createElementNS(NS, "circle");
  c.setAttribute("cx", 160); c.setAttribute("cy", 160); c.setAttribute("r", r);
  c.setAttribute("class", "ring r" + r);
  svg.insertBefore(c, svg.firstChild);
}
const decodeer = (s) => s.toUpperCase().replace(/[A-Z]/g, (ch) => ABC[(ABC.indexOf(ch) + verschuiving) % 26]);

// Het wiel vertaalt enkel wat je zelf intikt. Er staat geen bericht of oefenwoord in de pagina.
function toon() {
  binnen.forEach((t, i) => { t.textContent = ABC[(i + verschuiving) % 26]; });
  $("schuif").value = verschuiving;
  $("getal").textContent = verschuiving;
  $("uitvoer").textContent = decodeer($("invoer").value) || "…";
}
$("schuif").addEventListener("input", () => { verschuiving = Number($("schuif").value); toon(); });
$("links").addEventListener("click", () => { verschuiving = (verschuiving + 25) % 26; toon(); });
$("rechts").addEventListener("click", () => { verschuiving = (verschuiving + 1) % 26; toon(); });
$("invoer").addEventListener("input", toon);
toon();
