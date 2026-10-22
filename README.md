# Our Mood

*Ein Moment für uns – ohne Druck, ohne Erwartungen.*

Ein privater Moodtracker für Paare, mit dem ihr an einem vereinbarten Tag Stimmung, Nähe und Intimität festhalten könnt. Die App läuft im Browser: ohne Konto, ohne Tracking. Optional könnt ihr eure Geräte **verschlüsselt über euren Raspberry Pi oder ein privates GitHub-Repository synchronisieren** und Lust-Signale als Push über euren eigenen ntfy-Server senden.

## Dateien

| Datei | Zweck |
|---|---|
| `index.html` | Die komplette App (HTML, CSS und JavaScript in einer Datei). Nur diese Datei wird für GitHub Pages gebraucht. |
| `README.md` | Diese Anleitung. |
| `CNAME` | Eigene Domain für GitHub Pages. |
| `sync-server/` | Optionaler Sync-Server für den Raspberry Pi (Docker), mit eigener Anleitung. |

Zum lokalen Ausprobieren öffnest du `index.html` einfach per Doppelklick im Browser.

## Funktionen

- Zwei getrennte Profile, deren Namen sich in den Einstellungen ändern lassen. Das Profil wird nach jedem Laden und nach „Fertig“ neu abgefragt.
- Ausführliches Formular mit den Abschnitten A–F (Stimmung, Einflüsse, **Lust & Wünsche**, Intimität, Reflexion, Speichern) und Fortschrittsanzeige. 
- **Lust & Wünsche:** Lust-Skala 1–5, gewünschte Häufigkeit, „Was würde meine Lust fördern?“, Wunsch nach mehr Initiative; bei Nähe oder Sex zusätzlich „Wer hat die Initiative ergriffen?“.
- **Mehrere Einträge pro Tag** mit Tageszeit (morgens, mittags, abends, nachts) – z. B. morgens „nicht so gut“, abends „sehr gut“. Rückfrage nur bei gleicher Tageszeit.
- **Kleiner Monatskalender** über der Eintragsliste: zeigt pro Tag die Stimmungs-Emojis; Antippen zeigt die Einträge dieses Tages.
- **Filter „Anzeigen“** in der Eintragsliste: alle Einträge, mit Sex, mit Kuscheln/Nähe, mit Selbstbefriedigung oder mit viel Lust (4–5). Der Kalender hebt die passenden Tage hervor.
- **Lust-Signal:** „Ich hätte heute Lust“ (optional mit kurzer Nachricht). Die andere Person sieht es beim Öffnen ihres Profils; um Mitternacht verschwindet es.
- **Wunschliste zu zweit:** Ideen für Dates, Neues und Orte – beide können ergänzen, abhaken und löschen.
- **Selbstbefriedigung (optional):** In den Einstellungen für beide gemeinsam einschaltbar (gleichberechtigt); Ja/Nein-Frage im Formular (auch Schnell-Eintrag) und Übersicht in der Auswertung.
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
   - Ohne eingerichteten Sync sind Einträge, Lust-Signal und Wunschliste nur auf **demselben Gerät und im selben Browser** sichtbar. Mit Sync (siehe unten) seht ihr alles auf beiden Handys.
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

## Sync über euren Raspberry Pi (empfohlen)

Mit dem kleinen Sync-Server im Ordner [`sync-server/`](sync-server/README.md) braucht ein neues Gerät nur noch **euer Paar-Passwort**: Seite öffnen, **„🔗 Mit Paar-Passwort verbinden“** tippen, fertig. Es gibt keinen Token und keinen Link.

- Der Server läuft als Docker-Container auf dem Pi und ist unter `https://sync.chaoten.online` erreichbar, genauso wie ntfy.
- Er speichert nur verschlüsselte Daten und kennt das Passwort nicht. Fehlversuche werden gebremst.
- **Einrichtung Schritt für Schritt:** siehe [`sync-server/README.md`](sync-server/README.md).
- **Passwort ändern:** ⚙️ → Sync → „Sync-Passwort ändern“. Danach auf den anderen Geräten das neue Passwort eintragen.

Die GitHub-Variante (nächster Abschnitt) bleibt als Alternative verfügbar.

## Sync über GitHub (Alternative)

Damit ihr beide auf euren **eigenen Handys** dieselben Einträge, die Wunschliste und die Lust-Signale seht, gleicht die App ihre Daten über **ein privates GitHub-Repository** ab. Die Daten liegen dort als eine einzige Datei (`our-mood-data.enc.json`), die **auf dem Handy mit AES-256 verschlüsselt** wird. Der Schlüssel ist euer gemeinsames Sync-Passwort. GitHub und alle anderen sehen nur unlesbare Daten.

**Einrichtung (einmalig):**
1. **Privates Repository anlegen:** Auf GitHub **+ → New repository**, Name z. B. `moodtracker-data`, **Private** auswählen und **Create repository** klicken.
2. **Token erstellen:** GitHub → **Settings → Developer settings → Personal access tokens → Fine-grained tokens → Generate new token**.
   - *Repository access:* **Only select repositories** → `moodtracker-data`
   - *Permissions → Repository permissions → Contents:* **Read and write**
   - Ablaufdatum nach Wunsch. Danach muss das Token erneuert werden.
3. **In Our Mood auf dem ersten Handy:** ⚙️ Einstellungen → **Sync zwischen euren Handys** öffnen.
   - Repository `lukasnews/moodtracker-data` und das Token eintragen
   - Ein **gemeinsames Sync-Passwort** wählen (mind. 8 Zeichen)
   - **Speichern & synchronisieren** tippen
4. **Auf dem zweiten Handy** dasselbe mit **demselben Sync-Passwort**. Das Token darf dasselbe sein. Vorhandene Einträge beider Handys werden zusammengeführt.

**Weiteres Gerät verbinden (Laptop, Tablet, neues Handy):** Auf einem Gerät mit funktionierendem Sync unter ⚙️ → Sync → **„Einrichtungs-Link teilen“** tippen und den Link an dich selbst schicken (Messenger, Mail, AirDrop). Auf dem neuen Gerät den Link öffnen und **nur das Sync-Passwort** eingeben. Repository und Token stecken verschlüsselt im Link, ohne Passwort ist er wertlos. Der Link-Inhalt steht hinter `#`, wird also nicht an den Server gesendet und nach dem Öffnen sofort aus der Adresszeile entfernt.

**So funktioniert der Abgleich:**
- Die App gleicht beim Öffnen ab, kurz nach jedem Speichern, beim Zurückkehren in die App und jede Minute, solange sie offen ist.
- Bei gleichzeitigen Änderungen gewinnt pro Eintrag die neuere Änderung. Löschungen werden übertragen.
- Die Daten bleiben zusätzlich lokal auf jedem Handy. Ohne Internet funktioniert die App weiter und gleicht später ab.
- Token und Sync-Passwort werden nur im Browser des Geräts gespeichert, nie im Backup-Export und nie im öffentlichen App-Repository.
- **Sync-Passwort ändern:** ⚙️ → Sync → „Sync-Passwort ändern“. Die Datei im Repository wird mit dem neuen Passwort neu verschlüsselt. Auf dem anderen Handy erscheint dann ein Hinweis: Dort das neue Passwort eintragen und „Speichern & synchronisieren“ tippen.
- **Token und Sync-Passwort nie im Repository speichern** (auch nicht in einer `.env`). Das Passwort neben den verschlüsselten Daten hebt die Verschlüsselung auf. Besser ist ein Passwort-Manager.
- **Sync-Passwort vergessen = die Datei im Repository ist nicht mehr lesbar.** Die lokalen Daten auf den Handys bleiben erhalten.
- GitHub versioniert jede Änderung. Ältere Stände lassen sich so notfalls wiederherstellen.

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

- Keine externen Skripte, Schriften oder Dienste. Eine Content-Security-Policy erlaubt Netzwerkverbindungen nur zu euren eigenen Servern (ntfy-Push, Sync auf dem Pi) und zur GitHub-API (optionaler Sync): `connect-src https://ntfy.chaoten.online https://sync.chaoten.online https://api.github.com`.
- Nutzereingaben werden nur als Text (`textContent`) angezeigt, nie als HTML. `eval` wird nicht verwendet.
- Importierte Dateien werden nur mit `JSON.parse` gelesen und feldweise geprüft. Unbekannte Felder und ungültige Einträge werden verworfen.
