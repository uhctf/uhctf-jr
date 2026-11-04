# Oplossing: Hack het portaal

Standaardantwoord: `vertrouw-nooit-de-browser` (testwoorden: `vertrouw`, `nooit` en `de browser`). Open de site vanuit de laptopmap of `site/index.html`.

1. **Klasgemiddelde.** Op `klas.html` ligt een wazige laag met een slotje. Rechtsklik, Inspecteren: onder `.laag` staat `.inhoud` met "Testwoord 1 van 3: vertrouw". Lees het in Elementen, of verwijder de laag (`div.laag`) en zet `filter: blur` van `.inhoud` uit.
2. **Mijn rapport.** De link naar je rapport is `rapport.html?leerling=24`. Verander `24` in `1`: het rapport van de directeur heeft de notitie "sleutelwoord 2 is nooit" en wijst naar `beheer.html` en de sessiesleutel. Leerlingen 2 en 3 zijn personeel, 22, 23, 25 en 26 zijn klasgenoten, de rest bestaat niet.
3. **Beheer.** `beheer.html` zegt "Geen toegang, rol leerling". Open de ontwikkelaarstools, tabblad Application (Opslag in Firefox), Local Storage, sleutel `opdracht-portaal-token`. De waarde is `eyJ...==.<handtekening>`. Zet het deel voor de punt in de Decoder om (stap Base64 naar tekst): `{"gebruiker":"sam.peeters","leerling":24,"rol":"leerling"}`. Verander `leerling` bij rol in `beheerder`, zet terug naar Base64 (stap Tekst naar Base64), vervang de waarde (met of zonder `.handtekening`) en herlaad `beheer.html`: "Testwoord 3 van 3: de browser".

Antwoord: **vertrouw nooit de browser**. De kluis negeert hoofdletters, spaties en koppeltekens.

## Veelvoorkomende problemen

- Na het aanpassen van de token blijft de pagina "Geen toegang" zeggen: de pagina is niet herladen, of de Base64 is niet geldig (let op de `=` aan het einde en dat de JSON nog klopt). "Sessie herstellen" onderaan zet alles terug.
- In Firefox zie je Local Storage bij het tabblad Opslag.
- De decoder verwacht letters voor de punt, dus laat de handtekening weg bij het omzetten.
