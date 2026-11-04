// Verborgen bestanden: een bestandsinspecteur. Hex, tekst of afbeelding: jij kiest hoe je een bestand bekijkt. De pagina zegt niet wat verdacht is.
const bestanden = DATA.bestanden.map(b => ({ naam: b.naam, bytes: Uint8Array.from(atob(b.b64), c => c.charCodeAt(0)) }));
let gekozen = null, url = null;

for (const rij of [["Formaat", "Eerste bytes (hex)", "Als tekst"], ...DATA.magic]) {
  const tr = document.createElement("tr");
  for (const cel of rij) { const td = document.createElement(rij[0] === "Formaat" ? "th" : "td"); td.textContent = cel; tr.appendChild(td); }
  $("magic").appendChild(tr);
}
bestanden.forEach((b, i) => {
  const knop = document.createElement("button");
  knop.type = "button";
  knop.textContent = b.naam + " (" + b.bytes.length + " bytes)";
  knop.addEventListener("click", () => {
    gekozen = b;
    [...$("lijst").children].forEach((k, j) => k.classList.toggle("gekozen", j === i));
    $("kop").textContent = b.naam;
    toonHex();
  });
  $("lijst").appendChild(knop);
});

function leeg() {
  if (url) { URL.revokeObjectURL(url); url = null; }
  $("weergave").textContent = "";
  return gekozen;
}
function toonHex() {
  const b = leeg(); if (!b) return;
  const pre = document.createElement("pre"); pre.id = "hex";
  const delen = [];
  for (let i = 0; i < b.bytes.length; i += 16) {
    const rij = b.bytes.slice(i, i + 16);
    const hex = [...rij].map(x => x.toString(16).padStart(2, "0").toUpperCase()).join(" ").padEnd(47, " ");
    const asc = [...rij].map(x => x >= 32 && x < 127 ? String.fromCharCode(x) : ".").join("");
    delen.push("<span class='adres'>" + i.toString(16).padStart(6, "0") + "</span>  " + hex + "  <span class='asc'>" + asc.replace(/&/g, "&amp;").replace(/</g, "&lt;") + "</span>");
  }
  pre.innerHTML = delen.join("\n");
  $("weergave").appendChild(pre);
}
function toonTekst() {
  const b = leeg(); if (!b) return;
  const pre = document.createElement("pre");
  pre.textContent = new TextDecoder("utf-8").decode(b.bytes);
  $("weergave").appendChild(pre);
}
function toonBeeld() {
  const b = leeg(); if (!b) return;
  url = URL.createObjectURL(new Blob([b.bytes]));
  const img = document.createElement("img");
  img.alt = b.naam;
  img.onerror = () => { $("weergave").innerHTML = "<p class='melding fout'>Dit is geen afbeelding die de browser kan tonen.</p>"; };
  img.src = url;
  $("weergave").appendChild(img);
}
$("toon-hex").addEventListener("click", toonHex);
$("toon-tekst").addEventListener("click", toonTekst);
$("toon-beeld").addEventListener("click", toonBeeld);
