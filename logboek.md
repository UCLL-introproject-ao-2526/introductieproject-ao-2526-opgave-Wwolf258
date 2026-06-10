## 17 Maart 2026
Ik was van plan om te starten met de cursus. Alles mooi gelezen, alleen had ik issues met die github. Mail gestuurd naar de docent ter verduidelijking. 

## 23 Maart 2026
Feedback gekregen van de docent. Nog steeds niet duidelijk, de voorgestelde oplossing was niet van toepassing voor mijn gegeven. 

## 20 April 2026
Eindelijk tijd gevonden om dit vak terug te starten. Github oplossing gevonden via Reddit. 
Problemen gehad met pytest te gebruiken. Opgelost door research online. 

PNG opgelost Paint/Photoshop/MS Designer
SHA1 Encryptor/decryptor online te vinden
.class file --> gebruik Intellij

Foto's opzoeken -- > google images

## 20 April 2026
Tutorial (youtube video) doorgenomen van de blackjack oefening. 

## 22 April 2026
Gestart met het testen van de blackjack oefening. Pygame werkte niet op python 3.14, aanpassingen gezocht en gevonden om te starten met python 3.13.

## 23 April 2026
Blackjack maken zoals in een echt casino. Mogelijkheid tot het inzetten van 'echt' geld. Hoe moet ik het praktisch oplossen? Eerst nog eens uitgetest en momenteel werkt het spel goed. 
Variabelen achterliggend toegevoegd. Nog wel niet zichtbaar. 

## 24 April 2026
Saldo toekennen bij de start toegevoegd. Opgegeven met verder te werken aangezien het niet zichtbaar is. Er zitten nog fouten in die ik niet snap. 

## 25 April 2026
Een hele zaterdag hiervoor vrijgemaakt. Minder gedaan dan verwacht. Veel fouten gemaakt bij het opstellen van de def functie voor de betting. 
Vorige bug was verwerkt van het startsaldo. Maar ondertussen zijn er weer andere bugs ingekomen. 

Niet veel verder geraakt, gestopt om met een fris brein te starten morgen. 

## 26 April 2026
Bugs opgelost. Reddit en Stackoverflow to the rescue. 
Betprogramma werkt ondertussen. Ook gebruik gemaakt van een extensie om de code wat te ordenen visueel, maakt het werken sneller voor mezelf.

Volgende problemen wel ontdekt bij het afsluiten: Tekst komt over elkaar van 'Dealer wins' en 'Balance + Bets'. Spel gaat ook niet terug door zoals bij het vorige. Het blokkeert op het einde. 
Dit kon beter verwerkt worden, al ben ik blij dat het betting systeem lijkt te werken. 

## 29 April 2026
Spel gestart om zelf te spelen. Opgemerkt dat er nog meer bugs inzitten dan verwacht. Proberen toevoegen dat het saldo altijd wordt weergegeven. Weer extra bugs gemaakt. 
Uiteindelijk meer slecht gedaan dan goed vandaag qua aantal bugs. 

## 2 Mei 2026
Bugfixed, saldo wordt aangepast. Ik wou vandaag nog extra nieuwe items toevoegen maar hier niet toe geraakt. Tijdens het testen weer nieuwe bugs ontdekt. Proberen te gaan zoeken in de cursus programming 1&2, niet gevonden wat ik zocht. 


Bugfixes: Bij player busted, nadien niet meer mogelijk om terug te dealen. & Dealer wint altijd, wat niet de bedoeling is. 

## 3 Mei 2026
Persoonlijk zag ik het niet zitten om hier nog aan verder te werken. Meer video's gekeken over bugfixes op youtube dan echt nieuwe dingen toegevoegd. 
Alles werkt nu wel terug, dus meer gedaan dan initieel gedacht. 

## 6 Mei 2026 
Meer focus op layout mooier maken. Tekst die over elkaar staat etc aanpassen. 
Alle lijnen zijn onder elkaar nu bij het spelen. 


## 9 Mei 2026
We zitten bijna aan de 20 uur tijd dat we hebben voor dit project. Persoonlijk wou ik nog meer implementeren dit weekend om te zien hoe het gaat. 
Wat ik nog graag zou doen de komende 2 dagen: 
- Groene achtergrond
- Casino titel
- Blackjack bonus (direct 21 van de start)
- Game over (momenteel als balans 0 bereikt wordt, blokkeert het spel)
- Nog meer UI verbeteringen (zoals meer inzetknoppen dan alleen +10 en +50)

Uiteindelijk vandaag veel gesukkeld met de tekst (hoogtes/breedtes), zo gelaten aangezien het leesbaar is, nog niet ideaal. 
4 van de 5 punten verwerkt, meer dan initieel gehoopt. 

## 10 Mei 2026
UI verbeteren. Meer betknoppen maken. 
Wat kleine aanpassingen gedaan voor de leesbaarheid van de tekst weer. 
Nog wat kleine extra's toegevoegd tijdens het verbetern van de UI. Dealer/Player labels. 
Casino chips gemaakt met rondingen ipv rechthoeken. Ook vond ik het visueler om random de 4 soorten kaarten toe te voegen met hun respectievelijk teken. (--> Hier dacht ik gewoon de tekens toe te voegen, bleek wat moeilijker dan gedacht met de Unicodes, dit wist ik niet op voorhand anders had ik het niet gedaan.)
 
## 10/06/2026
Opmerking 1: Card [-1] en niet Card [0] of [1]
--> Niet akkoord. Volgens mij bij kaart met nummer 10, werkt alleen maar met -1 . Een card[0] bij een 10 geeft enkel 1 terug. 

Opmerking 2: Gebruik van symbolen. 
--> h, d, c, s zijn inderdaad eenvoudiger. Maar ik vond het gewoon visueel mooier voor een spel.

Opmerking 3: aces_count niet gebruikt?
--> Ik had dit gedaan voor de oneindige loop te vermijden waar ik inzat. Is nodig voor de aantal azen te tellen die omgezet worden van 11 naar 1?

Opmerking 4: Variablen gebruiken voor getallen
--> Terechte opmerking. 

Opmerking 5: Variabelen gebruiken voor kleuren
--> Terechte opmerking. (Uit het ook verloren door de vele aanpassingen dat dit vaak terugkomt.)

Opmerking 6: Plaats uitsparen, indentie. 
--> Terechte opmerking. Maar met mijn kennis destijds zag ik niet 100% hoe het anders kon. 

Opmerking 7: balance 1000 bovenaan
--> Terechte opmerking. Properder werken in de toekomst. 

Opmerking 8: Loopen over de buttons. 
--> Terechte opmerking. Voor mijn eigen gebruiksgemak gebruik ik liever if/else maar kan rommeliger zijn. 

--> Globaal gezien ben ik het eens met de opmerkingen. Deze zijn vaak terecht. Het belang voor mezelf is nu om na te kijken wanneer mijn code geschreven is. 
Te kijken of er nog vereenvoudigingen mogelijk zijn, 'basis'-waarden die telkens terugkomen steeds apart te definieren. 
