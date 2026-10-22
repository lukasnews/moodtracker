# Our Mood

*Ein Moment für uns – ohne Druck, ohne Erwartungen.*

Ein privater Moodtracker für Paare, mit dem ihr an einem vereinbarten Tag Stimmung, Nähe und Intimität festhalten könnt. Die App läuft komplett im Browser: ohne Konto, ohne Tracking. Einzige optionale Verbindung ist der Push für das Lust-Signal an euren eigenen ntfy-Server.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die komplette App (HTML, CSS und JavaScript in einer Datei). Nur diese Datei wird für GitHub Pages gebraucht. |
| `README.md` | Diese Anleitung. |

Zum lokalen Ausprobieren öffnest du `index.html` einfach per Doppelklick im Browser.

## Funktionen

- Zwei getrennte Profile, deren Namen sich in den Einstellungen ändern lassen. Das Profil wird nach jedem Laden und nach „Fertig“ neu abgefragt.
- Ausführliches Formular mit den Abschnitten A–F (Stimmung, Einflüsse, **Lust & Wünsche**, Intimität, Reflexion, Speichern) und Fortschrittsanzeige. 
- **Lust & Wünsche:** Lust-Skala 1–5, gewünschte Häufigkeit, „Was würde meine Lust fördern?“, Wunsch nach mehr Initiative; bei Nähe oder Sex zusätzlich „Wer hat die Initiative ergriffen?“.
- **Mehrere Einträge pro Tag** mit Tageszeit (morgens, mittags, abends, nachts) – z. B. morgens „nicht so gut“, abends „sehr gut“. Rückfrage nur bei gleicher Tageszeit.
- **Kleiner Monatskalender** über der Eintragsliste: zeigt pro Tag die Stimmungs-Emojis; Antippen zeigt die Einträge dieses Tages.
- **Lust-Signal:** „Ich hätte heute Lust“ (optional mit kurzer Nachricht). Die andere Person sieht es beim Öffnen ihres Profils; um Mitternacht verschwindet es.
- **Wunschliste zu zweit:** Ideen für Dates, Neues und Orte – beide können ergänzen, abhaken und löschen.
- **Zyklus (optional):** In den Einstellungen pro Person einschaltbar; Frage zur Zyklusphase im Formular und „Lust nach Zyklusphase“ in der Auswertung.
- Profilbild zeigt den Anfangsbuchstaben des Namens (bei gleichem Anfangsbuchstaben zwei Buchstaben).
- **Schnell-Eintrag „Lust heute?“** für beliebige Tage: Lust (Pflicht), Stimmung und Wunsch-Häufigkeit (optional).
- Zusatzfragen erscheinen nur, wenn sie passen (Sex → Erleben; Nähe/Sex → Gefühl danach).
- Schutz vor doppeltem Speichern, Hinweis bei ungespeicherten Eingaben, Rückfrage bei mehreren Einträgen am selben Tag.
- „Unsere bisherigen Einträge“ als einfache Liste: Details aufklappen, eigene Einträge bearbeiten oder löschen, nach Person und Zeitraum filtern.
- „Mein Bereich“ und eine gemeinsame Ansicht, die ausdrücklich geöffnet werden muss.
- Auswertung mit eigener **Sex & Lust**-Übersicht (Ø Lust, Anzahl Sex/Nähe, Lust-Verlauf je Person, Häufigkeitswunsch, Lustförderer, Initiative, Erleben) und unverbindlichen Beobachtungen – ohne Ziele und ohne Rangliste.
- Export als JSON, Import (zusammenführen oder ersetzen) mit Prüfung fehlerhafter Dateien, alles löschen nach Sicherheitsabfrage.

## Veröffentlichen mit GitHub Pages (ohne Programmierkenntnisse)

1. **Repository erstellen:** Melde dich bei [github.com](https://github.com) an, klicke oben rechts auf **+ → New repository**, gib einen Namen ein (z. B. `our-mood`) und klicke auf **Create repository**. Für GitHub Pages im kostenlosen Tarif muss das Repository *Public* sein. Das ist unbedenklich, denn dort liegt nur der App-Code, keine Einträge.
2. **`index.html` hochladen:** Klicke im neuen Repository auf **Add file → Upload files**, ziehe `index.html` in das Fenster und klicke auf **Commit changes**.
3. **GitHub Pages aktivieren:** Öffne **Settings → Pages**. Wähle unter *Build and deployment* bei *Source* den Eintrag **Deploy from a branch**, bei *Branch* den Branch **main** und den Ordner **/(root)**, und klicke auf **Save**.
4. **URL finden:** Nach 1–2 Minuten erscheint oben unter **Settings → Pages** „Your site is live at …“. Die Adresse lautet meist `https://DEIN-NAME.github.io/our-mood/`. Öffne sie auf dem Smartphone und lege sie bei Bedarf über „Zum Home-Bildschirm“ ab.
5. **Spätere Änderungen veröffentlichen:** Lade eine geänderte `index.html` wieder über **Add file → Upload files** hoch. Sie ersetzt die alte Datei. Alternativ öffnest du die Datei auf GitHub, klickst auf das Stift-Symbol und dann auf **Commit changes**. Nach ein bis zwei Minuten ist die neue Version online. Gespeicherte Einträge bleiben dabei erhalten, weil sie im Browser liegen und nicht auf GitHub.
6. **Grenzen der lokalen Speicherung:**
   - Die Einträge liegen **nur in dem Browser auf dem Gerät**, auf dem sie gespeichert wurden. Ein anderes Handy, ein anderer Browser (z. B. Safari statt Chrome) oder ein privates Fenster sieht sie nicht.
   - Wenn ihr zwei Geräte nutzt, hat jedes Gerät seine eigenen Daten. Zum Übertragen exportiert ihr auf dem einen Gerät und importiert auf dem anderen (*Zusammenführen*).
   - Werden Browserdaten bzw. Websitedaten gelöscht, sind die Einträge weg. Erstellt deshalb regelmäßig ein Backup.
   - Lust-Signal und Wunschliste sind nur für beide sichtbar, wenn ihr **dasselbe Gerät und denselben Browser** nutzt.
   - GitHub Pages schützt keine privaten Daten. Wer das entsperrte Gerät benutzen kann, kann die Einträge sehen. Die Backup-Datei ist unverschlüsselt.

## Eigene Domain: moods.chaoten.online

Die Datei `CNAME` im Repository enthält die Domain `moods.chaoten.online`. Damit sie funktioniert:

1. **DNS-Eintrag beim Domain-Anbieter** von `chaoten.online` anlegen:
   - Typ: `CNAME`
   - Name/Host: `moods`
   - Ziel/Wert: `lukasnews.github.io` (ohne Repository-Namen)
2. Auf GitHub unter **Settings → Pages → Custom domain** `moods.chaoten.online` eintragen (falls nicht schon automatisch gesetzt) und **Save** klicken.
3. Sobald der DNS-Check grün ist (das kann von wenigen Minuten bis zu 24 Stunden dauern), **Enforce HTTPS** aktivieren.

Hinweis: Gespeicherte Einträge gehören immer zu genau einer Adresse. Einträge, die unter `…github.io/…` gespeichert wurden, sind unter `moods.chaoten.online` nicht sichtbar. Übertragen lassen sie sich über Export und Import.

## Lust-Signal als Push aufs andere Handy (ntfy)

Die App kann das Lust-Signal über euren eigenen ntfy-Server **ntfy.chaoten.online** als Push-Benachrichtigung senden. Einträge, Antworten und die Wunschliste werden dabei nie übertragen, sondern nur Titel und die optionale Kurznachricht des Signals.

**Einrichtung (einmalig):**
1. **Auf dem Server:** Je Person ein Topic festlegen, z. B. `moods-lena` und `moods-tom`. Am besten schwer zu erratende Namen verwenden. Dann ein Zugangstoken erstellen, das in beide Topics **schreiben** darf, z. B. `ntfy token add <user>` und `ntfy access <user> moods-* write-only`.
2. **ntfy-App auf beiden Handys:** Server `https://ntfy.chaoten.online` hinzufügen, mit einem Benutzer anmelden, der **lesen** darf, und das **eigene** Topic abonnieren.
3. **In Our Mood auf jedem Handy:** ⚙️ Einstellungen → **Push (ntfy)** öffnen, Token und beide Topics eintragen und **Test senden** tippen.
4. Sendet jetzt jemand „✨ Ich hätte heute Lust“, bekommt die andere Person eine Benachrichtigung. Ein Tipp darauf öffnet die App.

**Sicherheit:** Das Token wird nur im Browser des jeweiligen Geräts gespeichert, nicht im Backup und nicht im GitHub-Code. Das Repository ist öffentlich, also das Token nie in `index.html` eintragen. Die Content-Security-Policy erlaubt Verbindungen ausschließlich zu `https://ntfy.chaoten.online`.

**Fehlermeldungen:** 401 = Token falsch, 403 = keine Schreibrechte fürs Topic, 400 = Nachrichtenformat abgelehnt.

## Datenschutz & Sicherheit

- Keine externen Skripte, Schriften oder Dienste. Eine Content-Security-Policy erlaubt Netzwerkverbindungen nur zum eigenen ntfy-Server (`connect-src https://ntfy.chaoten.online`), und das auch nur für das optionale Push-Signal.
- Nutzereingaben werden nur als Text (`textContent`) angezeigt, nie als HTML. `eval` wird nicht verwendet.
- Importierte Dateien werden nur mit `JSON.parse` gelesen und feldweise geprüft. Unbekannte Felder und ungültige Einträge werden verworfen.
