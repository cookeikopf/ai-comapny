# Security & Data Governance

Dieses Dokument beschreibt die Sicherheitsprinzipien und Prozesse für die
"AI Company". Die Einhaltung dieser Prinzipien ist Voraussetzung für den
Betrieb eines agentischen Unternehmens, das sensible Kundendaten nutzt und
automatisierte Entscheidungen trifft.

## Datenklassifizierung
Siehe `sops/security/SECURITY.md` für eine Übersicht der Datenklassen
(PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED) und entsprechende
Aufbewahrungsfristen. Keine personenbezogenen Daten (PII) dürfen in
Logs, Commits oder PRs erscheinen.

## Secrets & Schlüssel
- Speichere API‑Keys ausschließlich als **GitHub Actions Secrets** in den
  entsprechenden Environments (`staging`, `production`).
- Verwende **least privilege**: lege separate Keys für unterschiedliche
  Agenten und Tools an.
- **Rotation**: Alle Schlüssel sollten alle 90 Tage erneuert werden.
- Aktiviere GitHub Secret‑Scanning (siehe `secret-scan.yml` Workflow) und
  verwende Pre‑commit‑Hooks, um versehentliche Leaks zu verhindern.

## Kill‑Switch & Rate‑Limits
Konfiguriere `config/cost_limits.yaml` und `config/feature_flags.yaml`, um
Budgetgrenzen pro Lauf, Tag oder Woche zu setzen. Der `cost_guard.py`
Script bricht Ausführungen ab, wenn Kosten den definierten Schwellenwert
überschreiten. Zusätzlich können Feature-Flags (`allow_outbound_email`,
`allow_slack_post`) genutzt werden, um Außenwirkungen komplett zu
unterbinden.

## Audit‑Trail
Alle Aktionen des Systems (Agenten, Tools, LLMs) sind nachvollziehbar:
- GitHub PRs und Issues dienen als primäre Change‑Logs.
- Workflows (z. B. `orchestrate`, `release`, `send_messages`) laufen
  unter Angabe eines Trace‑IDs und schreiben den Status der Ausführung in
  die Job‑Logs.
- Durch die Integration von OpenTelemetry oder Langfuse (nicht in diesem
  MVP enthalten) lässt sich das Monitoring weiter ausbauen.

## Compliance
- AI Act (EU) und DSGVO Art. 22: Keine rein automatisierten Entscheidungen
  mit „rechtlichen oder ähnlich signifikanten Auswirkungen". Jede
  außenwirksame Aktion ist daher mit einem **Human‑in‑the‑Loop** versehen.
- Hinweise und Transparenztexte finden sich in `docs/ai_notice.md` und
  `docs/impressum.md`.