# Oplossing

Het wachtwoord bestaat uit vier verschillende dingen uit het profiel, in een vaste volgorde. Dit is Mastermind met profielgegevens in plaats van kleuren: na elke gok hoor je per vak of het juist is, fout, of juist maar op de verkeerde plaats.

Een manier om te redeneren:

1. Gok een eerste rij, bv. A B C D. Zijn alle vier fout, dan weet je dat het wachtwoord uit E, F, G en H bestaat.
2. Wissel daarna twee letters of vervang er één en kijk wat de feedback verandert.
3. Als je weet welke dingen erin zitten, probeer dan de volgorde.

Het profiel is standaard willekeurig (`seed = 0`); bij elke bouw staat het juiste wachtwoord, met de letters en delen, in `begeleider.pdf`. Het antwoord is de vier delen aan elkaar geplakt, in kleine letters.
