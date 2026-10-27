// Phishing of echt? Een digitaal potlood: zet bij elk bericht een kruisje bij "Nep" en vink de rode vlaggen aan die je ziet.
// De pagina controleert niets: onderaan staan gewoon de letters van de berichten die jij nep noemt, in volgorde.
const nep = DATA.kaarten.map(() => false);
const lijst = $("kaarten");
DATA.kaarten.forEach((k, i) => {
  const d = document.createElement("div");
  d.className = "bericht kanaal-" + k.kanaal.toLowerCase().replace(/[^a-z]/g, ""); d.id = "k-" + i;
  d.innerHTML = "<div class='kop'><span class='nr'></span><strong class='kanaal'></strong> <span class='van'></span></div>" +
    "<p class='tekst'></p><p class='link'></p>" +
    "<div class='vlaggen'></div>" +
    "<div class='rij'><button type='button' class='nepknop' aria-pressed='false'>Nep!</button><span class='letter' aria-label='Letter'></span></div>";
  d.querySelector(".nr").textContent = (i + 1) + ".";
  d.querySelector(".kanaal").textContent = k.kanaal + ":";
  d.querySelector(".van").textContent = k.van;
  d.querySelector(".tekst").textContent = k.tekst;
  d.querySelector(".link").textContent = k.link ? "Link: " + k.link : "";
  d.querySelector(".letter").textContent = k.letter;
  DATA.vlaggen.forEach((naam) => {
    const chip = document.createElement("button");
    chip.type = "button"; chip.className = "chip"; chip.textContent = naam; chip.setAttribute("aria-pressed", "false");
    chip.addEventListener("click", () => { const aan = chip.getAttribute("aria-pressed") !== "true"; chip.setAttribute("aria-pressed", String(aan)); chip.classList.toggle("aan", aan); });
    d.querySelector(".vlaggen").appendChild(chip);
  });
  d.querySelector(".nepknop").addEventListener("click", () => { nep[i] = !nep[i]; toon(); });
  lijst.appendChild(d);
});
function toon() {
  DATA.kaarten.forEach((k, i) => {
    const knop = $("k-" + i).querySelector(".nepknop");
    knop.classList.toggle("gekozen", nep[i]);
    knop.setAttribute("aria-pressed", String(nep[i]));
    $("k-" + i).classList.toggle("is-nep", nep[i]);
  });
  $("woord").textContent = DATA.kaarten.filter((k, i) => nep[i]).map((k) => k.letter).join("") || "–";
}
$("wis").addEventListener("click", () => {
  nep.fill(false);
  for (const chip of document.querySelectorAll(".chip")) { chip.classList.remove("aan"); chip.setAttribute("aria-pressed", "false"); }
  toon();
});
toon();
