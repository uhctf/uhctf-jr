// Doolhof: beweeg met de pijltjestoetsen (of WASD, de knoppen of klik op een buurvak). De letters op je route staan onderaan; jij bepaalt wanneer je klaar bent.
const b = DATA.breedte, h = DATA.hoogte;
const cel = Math.min(Math.floor(640 / b), Math.floor(620 / h), 48);
const canvas = $("doolhof");
canvas.width = b * cel + 4; canvas.height = h * cel + 4;
const ctx = canvas.getContext("2d");
const open = (x, y) => DATA.open[y][x];  // string met de open richtingen: N, S, W, O
const pijl = { N: [0, -1], S: [0, 1], W: [-1, 0], O: [1, 0] };
let route = [DATA.start.slice()];  // cellen van Start tot nu; terug stappen haalt de laatste cel weg

function teken() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.save(); ctx.translate(2, 2);
  // gekleurd spoor van de route
  ctx.fillStyle = "rgba(0,239,225,.35)";
  for (const [x, y] of route) ctx.fillRect(x * cel, y * cel, cel, cel);
  ctx.strokeStyle = "#222"; ctx.lineWidth = 3; ctx.lineCap = "round";
  ctx.beginPath();
  for (let y = 0; y < h; y++) for (let x = 0; x < b; x++) {
    const o = open(x, y), px = x * cel, py = y * cel;
    if (!o.includes("N") && !(x === DATA.start[0] && y === DATA.start[1])) { ctx.moveTo(px, py); ctx.lineTo(px + cel, py); }
    if (!o.includes("S") && !(x === DATA.einde[0] && y === DATA.einde[1])) { ctx.moveTo(px, py + cel); ctx.lineTo(px + cel, py + cel); }
    if (!o.includes("W")) { ctx.moveTo(px, py); ctx.lineTo(px, py + cel); }
    if (!o.includes("O")) { ctx.moveTo(px + cel, py); ctx.lineTo(px + cel, py + cel); }
  }
  ctx.stroke();
  ctx.fillStyle = "#222"; ctx.font = "bold " + Math.round(cel * 0.5) + "px system-ui, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
  for (const [sleutel, letter] of Object.entries(DATA.letters)) {
    const [x, y] = sleutel.split(",").map(Number);
    ctx.fillText(letter, x * cel + cel / 2, y * cel + cel / 2 + 1);
  }
  // jij
  const [px, py] = route[route.length - 1];
  ctx.fillStyle = "#ff00cc"; ctx.strokeStyle = "#222"; ctx.lineWidth = 2;
  const m = cel * 0.22; ctx.fillRect(px * cel + m, py * cel + m, cel - 2 * m, cel - 2 * m); ctx.strokeRect(px * cel + m, py * cel + m, cel - 2 * m, cel - 2 * m);
  ctx.restore();
  const letters = route.map(([x, y]) => DATA.letters[x + "," + y] || "").join("");
  $("letters").textContent = letters || "–";
}

function stap(richting) {
  const [x, y] = route[route.length - 1];
  if (!open(x, y).includes(richting)) return;
  const nx = x + pijl[richting][0], ny = y + pijl[richting][1];
  if (nx < 0 || ny < 0 || nx >= b || ny >= h) return;
  const vorige = route[route.length - 2];
  if (vorige && vorige[0] === nx && vorige[1] === ny) route.pop();  // terug op je stappen: die stap wordt ongedaan gemaakt
  else route.push([nx, ny]);
  teken();
}
const toetsen = { ArrowUp: "N", ArrowDown: "S", ArrowLeft: "W", ArrowRight: "O", w: "N", s: "S", a: "W", d: "O", W: "N", S: "S", A: "W", D: "O" };
document.addEventListener("keydown", (e) => {
  if (toetsen[e.key] && !/input|textarea|select/i.test(e.target.tagName)) { e.preventDefault(); stap(toetsen[e.key]); }
});
for (const knop of document.querySelectorAll("[data-richting]")) knop.addEventListener("click", () => stap(knop.dataset.richting));
canvas.addEventListener("click", (e) => {
  const r = canvas.getBoundingClientRect(), schaal = canvas.width / r.width;
  const x = Math.floor(((e.clientX - r.left) * schaal - 2) / cel), y = Math.floor(((e.clientY - r.top) * schaal - 2) / cel);
  const [px, py] = route[route.length - 1];
  for (const [d, [dx, dy]] of Object.entries(pijl)) if (px + dx === x && py + dy === y) stap(d);
});
$("opnieuw").addEventListener("click", () => { route = [DATA.start.slice()]; teken(); });
teken();
