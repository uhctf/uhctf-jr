# Oplossing: Hash-kraker

Standaardantwoord: `voetbal2017` (het wachtwoord van de beheerder). De zouten en datums hangen van de seed af; zie `begeleider.pdf` van de bouw.

1. Open de digitale pagina. In het lek staan vijf accounts. De lengte van de hash verraadt het type: 32 tekens is MD5, 40 is SHA-1, 64 is SHA-256.
2. In de hash-lab typ je wachtwoorden: de pagina toont MD5, SHA-1 en SHA-256 en markeert elke hash die in het lek staat.
   - `sofie` (MD5): `123456`, een van de meest gebruikte wachtwoorden.
   - `tom` (MD5): `voetbal`. Het steuntje zegt: mijn favoriete sport.
   - `lotte` (MD5): seizoen plus jaar van de kolom aangemaakt, bv. `zomer2019` (de seed bepaalt het seizoen en het jaar).
   - `jan` (SHA-1): `Welkom01`. Hoofdletters tellen mee in de hash: `welkom01` geeft een heel andere hash.
3. `beheerder` (SHA-256) heeft een zout, bv. `x7kq`. Het steuntje zegt: zoals Tom, maar met het jaar waarin de winkel begon. Het jaar staat in de kolom aangemaakt: `2017`. Probeer je `voetbal2017`, dan is de hash niet gelijk aan die van de beheerder: het zout is voor het wachtwoord gezet voordat er gehasht werd. Probeer `<zout>voetbal2017` en de hash klopt. Antwoord: `voetbal2017`.
4. Met code kan het ook: in het kladblok loop je over `WOORDEN`, plak je er jaartallen en een hoofdletter bij en vergelijk je `md5(poging)` met de hash. De zelftest (`./jr check hash-kraker`) doet precies dat.

De pagina onthoudt wat gekraakt is, ook als het team naar een andere opdracht gaat. "Nieuw team" in de kluis wist dat.
