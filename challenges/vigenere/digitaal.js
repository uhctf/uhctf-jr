// Vigenère: een ontcijferaar. Typ een sleutel en zie meteen het resultaat. De pagina zoekt de sleutel niet en zegt niet of hij klopt.
const ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
$("bericht").textContent = DATA.bericht;
$("bekend").textContent = "Elk bericht begint met: " + DATA.bekend;
for (let i = 0; i < 26; i++) {
  const vak = document.createElement("div");
  vak.style.cssText = "border:2px solid var(--lijn);background:#fff;padding:2px 0";
  vak.innerHTML = "<strong></strong><br><span class='klein'></span>";
  vak.querySelector("strong").textContent = ABC[i];
  vak.querySelector("span").textContent = i;
  $("alfabet").appendChild(vak);
}
function ontcijfer(tekst, sleutel) {
  let i = 0;
  return [...tekst].map(ch => {
    const p = ABC.indexOf(ch);
    if (p < 0) return ch;
    const s = ABC.indexOf(sleutel[i++ % sleutel.length]);
    return ABC[(p - s + 26) % 26];
  }).join("");
}
$("sleutel").addEventListener("input", () => {
  const sleutel = $("sleutel").value.toUpperCase().replace(/[^A-Z]/g, "");
  $("klaar").textContent = sleutel ? ontcijfer(DATA.bericht, sleutel) : "-";
});
