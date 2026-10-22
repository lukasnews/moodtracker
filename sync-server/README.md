# Our Mood – Sync-Server für den Raspberry Pi

Ein kleiner Dienst, damit ihr Our Mood auf **beliebig vielen Geräten** nutzen könnt. Auf einem neuen Gerät reicht dann: Seite öffnen, **„Mit Paar-Passwort verbinden“** tippen, Passwort eingeben.

- Er speichert **nur verschlüsselte Daten**. Die App verschlüsselt alles auf dem Gerät (AES-256).
- Er **kennt euer Passwort nicht**. Aus dem Passwort werden in der App zwei getrennte Werte abgeleitet: ein Anmelde-Token, von dem der Server nur einen Hash speichert, und der Verschlüsselungsschlüssel, der das Gerät nie verlässt.
- Fehlversuche werden gebremst (10 pro IP in 15 Minuten, 100 insgesamt pro Stunde).
- Er braucht nur Python und SQLite, ohne weitere Abhängigkeiten, und etwa 20–30 MB RAM.
- Er gehört **genau einem Paar**: Das erste Passwort, das sich verbindet, legt den Bereich an. Jedes andere Passwort wird abgelehnt.

---

## 1. Container auf dem Pi starten

Per SSH auf dem Pi:

```bash
git clone https://github.com/lukasnews/moodtracker.git
cd moodtracker/sync-server
docker compose up -d --build
```

Testen:

```bash
curl http://localhost:8087/v1/health
# → {"ok": true}
```

## 2. Unter https://sync.chaoten.online erreichbar machen

Das funktioniert **genauso wie bei eurem ntfy-Server**. Wie ntfy bei euch erreichbar ist, siehst du mit:

```bash
docker ps --format '{{.Names}}  {{.Image}}'
```

Je nachdem, was dort auftaucht:

**a) `nginx-proxy-manager` (Nginx Proxy Manager)**
1. Beim Domain-Anbieter einen DNS-Eintrag `sync` anlegen, genauso wie für `ntfy` (A-Record auf eure IP oder CNAME).
2. In der Proxy-Manager-Oberfläche **Add Proxy Host** wählen:
   - Domain: `sync.chaoten.online`
   - Forward: `http`, IP des Pi, Port `8087`
3. Im Tab **SSL** „Request a new SSL Certificate“ und „Force SSL“ aktivieren und speichern.

**b) `caddy`**
Im Caddyfile ergänzen und Caddy neu laden. Den DNS-Eintrag `sync` wie bei ntfy anlegen.
```
sync.chaoten.online {
    reverse_proxy localhost:8087
}
```

**c) `cloudflared` (Cloudflare Tunnel)**
Unter Cloudflare Zero Trust → **Networks → Tunnels** euren Tunnel öffnen und unter **Public Hostname → Add** eintragen:
- Subdomain `sync`, Domain `chaoten.online`
- Service: `http://localhost:8087`. Läuft cloudflared selbst im Docker, stattdessen die IP des Pi eintragen, z. B. `http://192.168.x.x:8087`.

**d) `traefik`**: Schreib mir, dann gibt es die passenden Labels.

Danach im Browser öffnen: **https://sync.chaoten.online/v1/health**. Dort sollte `{"ok": true}` erscheinen.

## 3. In der App einrichten

- **Erstes Gerät, am besten das mit den meisten Daten:** ⚙️ Einstellungen → **Sync zwischen euren Handys** → Die Adresse `https://sync.chaoten.online` ist schon eingetragen. Ein **Paar-Passwort** wählen und **Speichern & synchronisieren** tippen.
- **Jedes weitere Gerät:** Seite öffnen, auf der Startseite **„🔗 Mit Paar-Passwort verbinden“** tippen und das Passwort eingeben. Fertig.


## Pflege

**Geräte abmelden:** Das passiert in der App unter ⚙️ → Sync. Beim „Alle anderen Geräte abmelden“ merkt sich der Server das alte Passwort als gesperrt. Geräte mit dem alten Passwort bekommen die Antwort `410` und löschen ihre lokalen Daten. Ein gesperrtes Passwort kann nicht wieder verwendet werden.

**Updates:**
```bash
cd ~/moodtracker && git pull && cd sync-server && docker compose up -d --build
```

**Backup der Datenbank** (sie ist ohnehin verschlüsselt):
```bash
docker cp our-mood-sync:/data/our-mood-sync.db ./our-mood-sync-backup.db
```

**Zurücksetzen** (z. B. Passwort vergessen): Das löscht nur die Daten auf dem Server. Die Geräte behalten ihre Einträge und können danach mit einem neuen Passwort neu verbunden werden.
```bash
docker compose down -v && docker compose up -d
```

## Einstellungen (`docker-compose.yml`)

| Variable | Standard | Bedeutung |
|---|---|---|
| `ALLOWED_ORIGINS` | `https://moods.chaoten.online` | Nur diese Seite darf den Server nutzen (CORS) |
| `MAX_SPACES` | `1` | Anzahl Paare pro Server |
| `TRUST_PROXY` | `1` | Echte Client-IP hinter Proxy/Cloudflare für die Fehlversuch-Bremse |
| `FAILS_PER_IP` / `FAIL_WINDOW_SECONDS` | `10` / `900` | Bremse pro IP |
| `FAILS_GLOBAL` | `100` | Bremse insgesamt pro Stunde |

Wenn ihr eine andere Adresse als `sync.chaoten.online` nutzt, muss sie zusätzlich in der App (`index.html`, Zeile mit `connect-src`) eingetragen werden.
