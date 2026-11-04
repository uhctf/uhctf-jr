// Hash-kraker: een lek met hashes, een hash-lab om zelf wachtwoorden te proberen en (onderaan) een kladblok.
// De wachtwoorden staan niet in deze pagina, enkel de hashes. De pagina onthoudt wat een team al gekraakt heeft.

// <hashes>  gewone JavaScript, zodat het ook vanaf schijf (file://) werkt, waar crypto.subtle niet altijd bestaat
const UTF8 = new TextEncoder();
const rotl = (x, n) => (x << n) | (x >>> (32 - n));
const hexBE = (w) => w.map((x) => (x >>> 0).toString(16).padStart(8, "0")).join("");
const hexLE = (w) => w.map((x) => [0, 8, 16, 24].map((s) => ((x >>> s) & 255).toString(16).padStart(2, "0")).join("")).join("");
// vul aan tot een veelvoud van 64 bytes, met de lengte in bits achteraan (groot of klein eindigend)
function vul(tekst, klein) {
  const b = UTF8.encode(tekst), n = b.length, totaal = (((n + 8) >> 6) + 1) << 6;
  const buf = new Uint8Array(totaal); buf.set(b); buf[n] = 0x80;
  const dv = new DataView(buf.buffer), bits = n * 8;
  if (klein) { dv.setUint32(totaal - 8, bits >>> 0, true); dv.setUint32(totaal - 4, Math.floor(bits / 4294967296), true); }
  else { dv.setUint32(totaal - 8, Math.floor(bits / 4294967296), false); dv.setUint32(totaal - 4, bits >>> 0, false); }
  return dv;
}
const MD5_S = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21];
const MD5_K = Array.from({ length: 64 }, (_, i) => Math.floor(Math.abs(Math.sin(i + 1)) * 4294967296) >>> 0);
function md5(tekst) {
  const dv = vul(tekst, true);
  let a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
  for (let o = 0; o < dv.byteLength; o += 64) {
    const M = Array.from({ length: 16 }, (_, i) => dv.getUint32(o + i * 4, true));
    let A = a0, B = b0, C = c0, D = d0;
    for (let i = 0; i < 64; i++) {
      let F, g;
      if (i < 16) { F = (B & C) | (~B & D); g = i; }
      else if (i < 32) { F = (D & B) | (~D & C); g = (5 * i + 1) % 16; }
      else if (i < 48) { F = B ^ C ^ D; g = (3 * i + 5) % 16; }
      else { F = C ^ (B | ~D); g = (7 * i) % 16; }
      F = (F + A + MD5_K[i] + M[g]) >>> 0;
      A = D; D = C; C = B; B = (B + rotl(F, MD5_S[i])) >>> 0;
    }
    a0 = (a0 + A) >>> 0; b0 = (b0 + B) >>> 0; c0 = (c0 + C) >>> 0; d0 = (d0 + D) >>> 0;
  }
  return hexLE([a0, b0, c0, d0]);
}
function sha1(tekst) {
  const dv = vul(tekst, false);
  let h0 = 0x67452301, h1 = 0xefcdab89, h2 = 0x98badcfe, h3 = 0x10325476, h4 = 0xc3d2e1f0;
  const w = new Array(80);
  for (let o = 0; o < dv.byteLength; o += 64) {
    for (let i = 0; i < 16; i++) w[i] = dv.getUint32(o + i * 4, false);
    for (let i = 16; i < 80; i++) w[i] = rotl(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1);
    let a = h0, b = h1, c = h2, d = h3, e = h4;
    for (let i = 0; i < 80; i++) {
      let f, k;
      if (i < 20) { f = (b & c) | (~b & d); k = 0x5a827999; }
      else if (i < 40) { f = b ^ c ^ d; k = 0x6ed9eba1; }
      else if (i < 60) { f = (b & c) | (b & d) | (c & d); k = 0x8f1bbcdc; }
      else { f = b ^ c ^ d; k = 0xca62c1d6; }
      const t = (rotl(a, 5) + f + e + k + w[i]) >>> 0;
      e = d; d = c; c = rotl(b, 30) >>> 0; b = a; a = t;
    }
    h0 = (h0 + a) >>> 0; h1 = (h1 + b) >>> 0; h2 = (h2 + c) >>> 0; h3 = (h3 + d) >>> 0; h4 = (h4 + e) >>> 0;
  }
  return hexBE([h0, h1, h2, h3, h4]);
}
const SHA256_K = [0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
  0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
  0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
  0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
  0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
  0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2];
function sha256(tekst) {
  const dv = vul(tekst, false);
  const h = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19];
  const w = new Array(64);
  for (let o = 0; o < dv.byteLength; o += 64) {
    for (let i = 0; i < 16; i++) w[i] = dv.getUint32(o + i * 4, false);
    for (let i = 16; i < 64; i++) {
      const s0 = rotl(w[i - 15], 25) ^ rotl(w[i - 15], 14) ^ (w[i - 15] >>> 3), s1 = rotl(w[i - 2], 15) ^ rotl(w[i - 2], 13) ^ (w[i - 2] >>> 10);
      w[i] = (w[i - 16] + s0 + w[i - 7] + s1) >>> 0;
    }
    let [a, b, c, d, e, f, g, hh] = h;
    for (let i = 0; i < 64; i++) {
      const S1 = rotl(e, 26) ^ rotl(e, 21) ^ rotl(e, 7), ch = (e & f) ^ (~e & g), t1 = (hh + S1 + ch + SHA256_K[i] + w[i]) >>> 0;
      const S0 = rotl(a, 30) ^ rotl(a, 19) ^ rotl(a, 10), maj = (a & b) ^ (a & c) ^ (b & c), t2 = (S0 + maj) >>> 0;
      hh = g; g = f; f = e; e = (d + t1) >>> 0; d = c; c = b; b = a; a = (t1 + t2) >>> 0;
    }
    [a, b, c, d, e, f, g, hh].forEach((x, i) => { h[i] = (h[i] + x) >>> 0; });
  }
  return hexBE(h);
}
// </hashes>

const LEK = DATA.lek;          // de accounts uit het lek
const WOORDEN = DATA.woorden;  // een lijst woorden, handig in het kladblok
const OPSLAG = "opdracht-hash-gekraakt";  // het voorvoegsel opdracht- wordt gewist door "Nieuw team" in de kluis
const ALGOS = [["MD5", md5], ["SHA-1", sha1], ["SHA-256", sha256]];

let gekraakt = {};  // gebruiker -> wachtwoord
try { gekraakt = JSON.parse(localStorage.getItem(OPSLAG) || "{}") || {}; } catch (e) { gekraakt = {}; }
const bewaar = () => { try { localStorage.setItem(OPSLAG, JSON.stringify(gekraakt)); } catch (e) {} };

function tekenLek() {
  const lijf = $("lek-lijf");
  lijf.innerHTML = "";
  for (const r of LEK) {
    const tr = document.createElement("tr");
    if (gekraakt[r.gebruiker] != null) tr.className = "gekraakt";
    for (const [sleutel, klasse] of [["gebruiker", ""], ["email", ""], ["hash", "hash"], ["zout", "hash"], ["aangemaakt", ""], ["steun", ""]]) {
      const td = document.createElement("td"); td.textContent = r[sleutel] || "–"; if (klasse) td.className = klasse; tr.appendChild(td);
    }
    const td = document.createElement("td"); td.textContent = gekraakt[r.gebruiker] != null ? "✓ " + gekraakt[r.gebruiker] : ""; tr.appendChild(td);
    lijf.appendChild(tr);
  }
  const aantal = Object.keys(gekraakt).length;
  $("teller").textContent = aantal + " van " + LEK.length + " gekraakt";
  const beheer = LEK.find((r) => r.beheerder);
  const klaar = beheer && gekraakt[beheer.gebruiker] != null;
  $("beheerder-klaar").hidden = !klaar;
  if (klaar) $("beheerder-ww").textContent = gekraakt[beheer.gebruiker];
}

function probeer() {
  const invoer = $("poging").value;
  const uit = $("uitvoer");
  uit.innerHTML = "";
  if (invoer === "") { $("uitslag").textContent = ""; return; }
  const gevonden = [];
  for (const [naam, f] of ALGOS) {
    const h = f(invoer);
    const rij = document.createElement("div");
    rij.className = "hashrij";
    const k = document.createElement("span"); k.className = "algo"; k.textContent = naam + " (" + h.length + " tekens)";
    const v = document.createElement("code"); v.textContent = h;
    rij.append(k, v);
    const raak = LEK.filter((r) => r.hash === h);
    if (raak.length) rij.classList.add("raak");
    uit.appendChild(rij);
    for (const r of raak) gevonden.push([r, naam]);
  }
  if (!gevonden.length) { $("uitslag").textContent = "Geen enkel account in het lek heeft deze hash."; $("uitslag").className = "melding"; return; }
  for (const [r, naam] of gevonden) {
    // een wachtwoord met zout ervoor: toon enkel het wachtwoord zelf
    gekraakt[r.gebruiker] = r.zout && invoer.startsWith(r.zout) ? invoer.slice(r.zout.length) : invoer;
  }
  bewaar();
  $("uitslag").textContent = "Raak! Gekraakt: " + gevonden.map(([r, naam]) => r.gebruiker + " (" + naam + ")").join(", ") + ".";
  $("uitslag").className = "melding goed";
  tekenLek();
}

$("poging").addEventListener("input", probeer);
$("wis-lek").addEventListener("click", () => { if (confirm("Alles wat jullie gekraakt hebben uit deze lijst wissen?")) { gekraakt = {}; bewaar(); tekenLek(); } });
tekenLek();
