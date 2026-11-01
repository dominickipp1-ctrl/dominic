# Feierabend-Komplex – Klaviyo Flow Setup

Alle 15 Templates liegen in Klaviyo unter **Content → Templates** (Suche: `FK |`).
Bilder liegen in der Klaviyo-Bibliothek mit Prefix `FK_`. Quellcode: `build.py` → `templates/`.

## 0. Vorher erledigen (sonst laufen Kunden doppelt durch Flows)

1. **Rabattcode in Shopify anlegen:** `FEIERABEND10`, 10 %, nur Feierabend-Komplex, 1× pro Kunde.
   Empfehlung: Ablaufdatum bzw. in Klaviyo als *Unique Coupon* (7 Tage gültig), damit „läuft bald ab“ in Welcome 5 stimmt.
2. **Alte Shilajit-Flows absichern** (nicht löschen!) – Trigger-Filter ergänzen:
   - `Abandoned Cart Reminder (Email)` (XxHyMC, Checkout Started): *Item Names doesn't contain „FEIERABEND“*
   - `Browse Abandonment - Standard` (RpawXV, Viewed Product): *ProductName doesn't contain „FEIERABEND“*
   - `Welcome-Serie` (TDjbsn) hängt an Liste TykCWn → Feierabend bekommt eine **eigene Liste**.
3. **Klaviyo-Zeitzone** steht auf *US/Eastern* → auf *Europe/Berlin* umstellen (Settings → Account).
4. **Added to Cart** existiert im Account noch nicht → in Klaviyo unter Integrations → Shopify → Onsite-Tracking aktivieren (sonst Flow 3 weglassen).

## 1. Welcome – Liste „Feierabend Newsletter“ (neues Popup auf Feierabend-Seiten)

| # | Wartezeit | Template | Betreff | Vorschautext |
|---|---|---|---|---|
| 1 | sofort | SMsS39 | Dein Feierabend-Geschenk wartet 🌙 | 10 % auf deinen ersten Feierabend-Komplex – dein Code ist drin. |
| 2 | 1 Tag | X3VVRB | Dein Kopf hat noch nicht Feierabend? | Und plötzlich ist es elf. Warum dein Abend einen Schlusspunkt braucht. |
| 3 | 2 Tage | QQmHSe | 5 Zutaten. Keine Geheimnisse. | Was genau in deinen zwei Gummies steckt – mit exakter Menge. |
| 4 | 2 Tage | U6GtvC | „Ist es ein Wundermittel? Nein.“ | Warum wir diese ehrliche Bewertung besonders mögen. |
| 5 | 2 Tage | SNDn7R | Dein 10 % Code läuft bald ab ⏳ | Letzte Erinnerung: Sichere dir deinen Willkommensrabatt. |

Flow-Filter: *Placed Order zero times since starting this flow*.

## 2. Abandoned Checkout – Trigger *Checkout Started*

Trigger-Filter: *Item Names contains „FEIERABEND“*. Flow-Filter: *Placed Order zero times since starting this flow* + *not in flow in last 7 days*.

| # | Wartezeit | Template | Betreff | Vorschautext |
|---|---|---|---|---|
| 1 | 1 Std. | TwSV8e | Dein Feierabend wartet noch an der Kasse | Wir haben deinen Warenkorb für dich gespeichert. |
| 2 | 23 Std. | YqYhBF | Noch unsicher? Das fragen sich viele. | Melatonin, Abo, Garantie – die ehrlichen Antworten. |
| 3 | 24 Std. | VkviHr | 10 % für deinen ersten Feierabend – nur für dich | Dein Warenkorb ist noch da. Und jetzt gibt’s 10 % on top. |

## 3. Abandoned Cart – Trigger *Added to Cart* (erst nach Schritt 0.4)

Filter: *Started Checkout zero times* + *Placed Order zero times since starting this flow*.

| # | Wartezeit | Template | Betreff | Vorschautext |
|---|---|---|---|---|
| 1 | 2 Std. | VFBA9m | Hast du etwas vergessen? | Dein Feierabend-Komplex liegt noch im Warenkorb. |
| 2 | 1 Tag | XwDHQH | „…kaue einfach zwei leckere Gummis. Fertig.“ | Was andere über ihren neuen Feierabend sagen. |

## 4. Browse Abandonment – Trigger *Viewed Product*

Trigger-Filter: *ProductName contains „FEIERABEND“*. Flow-Filter: *Added to Cart / Checkout Started / Placed Order zero times since starting this flow* + *not in flow in last 14 days*.

| # | Wartezeit | Template | Betreff | Vorschautext |
|---|---|---|---|---|
| 1 | 2 Std. | SbYjw9 | Noch am Überlegen? | Der Feierabend-Komplex – alles auf einen Blick. |
| 2 | 1 Tag | XPJZ88 | Mehr als ein Tee. Ohne Melatonin. | Warum der Feierabend-Komplex anders ist als Tee oder Melatonin. |
| 3 | 2 Tage | XQkfau | Teste ihn 60 Tage – ohne Risiko | Passt er nicht zu dir, bekommst du dein Geld zurück. |

## 5. Site Abandonment – Trigger *Active on Site*

Flow-Filter: *Viewed Product zero times since starting this flow* + *Placed Order zero times* + *not in flow in last 30 days* + *not in Browse-/Checkout-Flow*.

| # | Wartezeit | Template | Betreff | Vorschautext |
|---|---|---|---|---|
| 1 | 1 Std. | Wyh9LH | Schön, dass du vorbeigeschaut hast | Gib deinem Tag einen Schlusspunkt – so funktioniert’s. |
| 2 | 1 Tag | RNBMUf | Heute Abend schon Feierabend im Kopf? | Zwei Gummies. Jeden Abend. Und der Feierabend gehört wieder dir. |

## Rechtliches (vor Livegang prüfen)

- Health Claims: Im Text steht als Wirkaussage nur der zugelassene B6-Claim. Bitte keine Schlaf- oder Stress-Versprechen ergänzen.
- Kundenstimmen sind wörtliche Auszüge aus den Judge.me-Bewertungen. Nutze sie nur, wenn es echte Käufer sind.
- Preise und Pakete (29,99 € / 2+1 / 3+2) sind fest im Template. Bei Änderungen im Shop: `build.py` anpassen oder in Klaviyo ändern.

## Stand 01.11.2026 – von Claude über Windsor angelegt (alle als Entwurf)

| Flow | Klaviyo-ID | Trigger |
|---|---|---|
| FK \| Welcome – Feierabend-Komplex | UGbX4Z | Liste „Feierabend Newsletter“ (XpSqCi) |
| FK \| Abandoned Checkout – Feierabend-Komplex | XdsDCd | Checkout Started, Item Names enthält den exakten Produkttitel |
| FK \| Browse Abandonment – Feierabend-Komplex | XtkqEp | Viewed Product, ProductName enthält „FEIERABEND“ |
| FK \| Site Abandonment – Feierabend-Komplex | T4c6bv | Active on Site (TpctBE) |

Auf Entwurf gestellt (Duplikate): TDjbsn, VKGRLF, YmqiJh, XBFZzP, XJVgaB.
Warenkorb-Flow fehlt noch, bis „Added to Cart“ in Klaviyo erfasst wird.
Achtung: Wird der Produkttitel in Shopify geändert, muss der Checkout-Filter angepasst werden.

## Nach dem Kauf, Nachkauf & Winback (01.11.2026, alle Entwurf)

Alle hängen an „Placed Order“ mit Filter auf den Feierabend-Produkttitel. Die Paketgröße wird über den Bestellwert erkannt.

| Flow | Klaviyo-ID | Filter | Mails |
|---|---|---|---|
| FK \| Nach dem Kauf | VKnLH4 | jede Feierabend-Bestellung | sofort Danke + Einnahme (TbJQ2V) · Tag 6 Ritual-Tipps (RTsuBH) · Tag 14 Bewertung (Rw5WZP) |
| FK \| Nachkauf – 1 Dose | WSLBsp | Bestellwert < 40 € | Tag 22 „noch 8 Abende“ (XwJEaN) · Tag 27 „letzte Abende“ (YjXtxu) |
| FK \| Nachkauf – Paket 2+1 | UE8G7G | 40–70 € | Tag 80 „Vorrat geht zur Neige“ (XAEarR) |
| FK \| Nachkauf – Paket 3+2 | VMwwR3 | ≥ 70 € | Tag 140 „Vorrat geht zur Neige“ (XAEarR) |
| FK \| Winback – 1 Dose | UxmVzN | < 40 € | Tag 60 „Dein Feierabend vermisst dich“ (SAw3sk) |

Alle Nachkauf- und Winback-Flows stoppen automatisch, sobald der Kunde erneut bestellt.
Wenn sich Preise oder Pakete ändern, müssen die 40/70-€-Grenzen angepasst werden.
