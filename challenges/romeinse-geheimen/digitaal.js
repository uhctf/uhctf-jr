// Romeinse geheimen: draai de binnenste ring tot de oefenwoorden gewone woorden worden. Lees dan het bericht.
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

function toon() {
  binnen.forEach((t, i) => { t.textContent = ABC[(i + verschuiving) % 26]; });
  $("schuif").value = verschuiving;
  $("getal").textContent = verschuiving;
  $("uitvoer").textContent = decodeer(DATA.bericht);
  const lijst = $("oefen");
  lijst.innerHTML = "";
  DATA.oefen.forEach((w) => {
    const li = document.createElement("li");
    li.innerHTML = "<span class='code'></span> → <strong></strong>";
    li.querySelector(".code").textContent = w; li.querySelector("strong").textContent = decodeer(w);
    lijst.appendChild(li);
  });
}
$("schuif").addEventListener("input", () => { verschuiving = Number($("schuif").value); toon(); });
$("links").addEventListener("click", () => { verschuiving = (verschuiving + 25) % 26; toon(); });
$("rechts").addEventListener("click", () => { verschuiving = (verschuiving + 1) % 26; toon(); });
$("oefen-kaart").hidden = DATA.oefen.length === 0;
$("oefenhint").textContent = DATA.hint ? "Hint: " + DATA.hint : "";
toon();
