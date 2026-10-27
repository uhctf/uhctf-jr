// Schatkaart: kies een raadsel, los het op en klik op de stip die erbij hoort. De letter komt in het vakje van het raadsel.
const kolommen = DATA.kolommen, aantalRijen = DATA.rijen;
const gekozen = DATA.raadsels.map(() => null);  // per raadsel de gekozen plek [kolom, rij]
let actief = 0;
const kaart = $("kaart");
kaart.style.gridTemplateColumns = "1.6em repeat(" + kolommen.length + ", 1fr)";
function label(tekst) { const d = document.createElement("div"); d.className = "kop"; d.textContent = tekst; return d; }
kaart.appendChild(label(""));
for (const k of kolommen) kaart.appendChild(label(k));
const stippen = {};
for (let r = 0; r < aantalRijen; r++) {
  kaart.appendChild(label(String(r + 1)));
  for (let c = 0; c < kolommen.length; c++) {
    const letter = DATA.letters[c + "," + r];
    if (letter === undefined) { const leeg = document.createElement("div"); leeg.className = "leeg"; kaart.appendChild(leeg); continue; }
    const k = document.createElement("button");
    k.type = "button"; k.className = "stip"; k.innerHTML = "<span class='punt'></span><span class='let'></span>";
    k.querySelector(".let").textContent = letter;
    k.setAttribute("aria-label", "Stip " + kolommen[c] + (r + 1));
    k.addEventListener("click", () => kiesStip(c, r));
    kaart.appendChild(k); stippen[c + "," + r] = k;
  }
}
const lijst = $("raadsels");
DATA.raadsels.forEach((r, i) => {
  const li = document.createElement("li");
  li.innerHTML = "<button type='button' class='raadsel'><span class='tekst'></span><span class='vak'></span></button>";
  li.querySelector(".tekst").textContent = "Kolom: " + r.kolom + " Rij: " + r.rij;
  li.querySelector("button").addEventListener("click", () => { actief = i; toon(); });
  lijst.appendChild(li);
});
function kiesStip(c, r) {
  gekozen[actief] = [c, r];
  const volgende = gekozen.findIndex((g, i) => g === null && i !== actief);
  if (volgende >= 0) actief = volgende;
  toon();
}
function toon() {
  for (const k of Object.values(stippen)) { k.classList.remove("gekozen"); k.removeAttribute("data-nr"); }
  gekozen.forEach((g, i) => { if (g) { const k = stippen[g[0] + "," + g[1]]; k.classList.add("gekozen"); k.dataset.nr = (k.dataset.nr ? k.dataset.nr + "," : "") + (i + 1); } });
  [...lijst.children].forEach((li, i) => {
    li.querySelector("button").classList.toggle("actief", i === actief);
    const g = gekozen[i];
    li.querySelector(".vak").textContent = g ? DATA.letters[g[0] + "," + g[1]] + " (" + kolommen[g[0]] + (g[1] + 1) + ")" : "?";
  });
  const klaar = gekozen.every((g) => g !== null);
  $("antwoord-kaart").hidden = !klaar;
  if (klaar) $("antwoord").textContent = gekozen.map((g) => DATA.letters[g[0] + "," + g[1]]).join("");
}
toon();
