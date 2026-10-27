// Laag na laag: het bericht om te kopiëren en een link om het in de decoder te openen.
$("bericht").value = DATA.bericht;
$("decoder").href = "decoder/index.html#t=nl&i=" + encodeURIComponent(DATA.bericht);
$("kopieer").addEventListener("click", async () => {
  $("bericht").select();
  let ok = false;
  try { await navigator.clipboard.writeText(DATA.bericht); ok = true; } catch (e) {}
  if (!ok) { try { ok = document.execCommand("copy"); } catch (e) {} }
  $("gekopieerd").textContent = ok ? "Gekopieerd!" : "Selecteer de tekst en druk op Ctrl+C.";
});
