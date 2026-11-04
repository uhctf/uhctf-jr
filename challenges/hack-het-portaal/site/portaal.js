"use strict";
// Gedeeld door alle pagina's van het leerlingenportaal.
const SALT = "{{SALT}}";
const TOKEN_SLEUTEL = "opdracht-portaal-token";  // het voorvoegsel opdracht- wordt gewist door "Nieuw team" in de kluis
const HANDTEKENING = "{{HANDTEKENING}}";
const $ = (id) => document.getElementById(id);

function lees(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
function schrijf(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

function naarBase64(obj) {
  const bytes = new TextEncoder().encode(JSON.stringify(obj));
  let s = ""; bytes.forEach((b) => { s += String.fromCharCode(b); });
  return btoa(s);
}
function vanBase64(tekst) {
  tekst = tekst.trim().replace(/-/g, "+").replace(/_/g, "/");
  while (tekst.length % 4) tekst += "=";
  return new TextDecoder().decode(Uint8Array.from(atob(tekst), (c) => c.charCodeAt(0)));
}

// De sessiesleutel (token): twee delen met een punt ertussen. Het eerste deel is de inhoud in Base64, het tweede een handtekening.
// Bij het eerste bezoek krijgt elke leerling een token van een gewone leerling.
function sessie() {
  let t = lees(TOKEN_SLEUTEL);
  if (!t) { t = naarBase64({ gebruiker: "sam.peeters", leerling: 24, rol: "leerling" }) + "." + HANDTEKENING; schrijf(TOKEN_SLEUTEL, t); }
  return t;
}
function leesToken() {
  try { return JSON.parse(vanBase64(sessie().split(".")[0])); } catch (e) { return null; }
}
function herstelSessie() { try { localStorage.removeItem(TOKEN_SLEUTEL); } catch (e) {} location.reload(); }

// Gegevens die de "server" enkel geeft aan wie er recht op heeft, zijn hier versleuteld met een sleutel uit de aanvraag.
// (Een echt portaal controleert dat op een server; in deze oefening speelt de pagina zelf de server.)
function ontsleutel(hex, sleutel) {
  const bytes = Uint8Array.from(hex.match(/../g), (h) => parseInt(h, 16));
  const k = new TextEncoder().encode(SALT + ":" + sleutel);
  return new TextDecoder().decode(bytes.map((b, i) => b ^ k[i % k.length]));
}

function kop() {
  const t = leesToken();
  const naam = t ? t.gebruiker : "onbekend";
  const el = $("gebruiker");
  if (el) el.textContent = "Ingelogd als " + naam;
}
document.addEventListener("DOMContentLoaded", () => {
  sessie();
  kop();
  const knop = $("herstel");
  if (knop) knop.addEventListener("click", herstelSessie);
});
