# Architekturübersicht

Diese Datei gibt einen Überblick über die technische und organisatorische
Architektur des Projekts "AI Company". Sie dient als Grundlage für
Entwickler, Operatoren und Compliance‑Verantwortliche.

## Hauptkomponenten

| Komponente       | Beschreibung |
|------------------|-------------|
| **Orchestrator** | Der Founder‑Agent koordiniert alle Spezial‑Agenten und entscheidet, welche Aufgaben erstellt und wie Ressourcen zugewiesen werden. Er arbeitet nach dem **Deterministic‑first**‑Prinzip und eskaliert zu LLMs nur bei Bedarf. |
| **Spezial‑Agenten** | Agents für Research, Engineering (Codex), Growth, Kommunikation, Eval und Compliance. Jeder Agent hat einen eigenen System‑Prompt (`agents/<name>/system.md`). |
| **MCP‑Stubs**    | Unter `tools/` befinden sich Stub‑Implementierungen für GitHub, Gmail und Slack. Sie kapseln die Authentifizierung, Logging und API‑Aufrufe. |
| **Scripts**       | In `scripts/` befinden sich deterministische Utilities (z. B. `normalize_leads.py`, `generate_outreach.py`) sowie Gatekeeper‑Skripte (`cost_guard.py`, `send_messages.py`). |
| **Config**        | Dateien in `config/` enthalten Kosten‑Limits, Feature‑Flags und Policies (z. B. `policies.yaml` für das deterministische Prinzip). |
| **CI/CD**         | Unter `.github/workflows/` definierte Workflows für Smoke‑Evals, Deployments, Secret‑Scanning, CodeQL, Orchestrierung und Nachrichtenversand. |

## Datenfluss (Simplifiziert)

1. **Issue**: Ein neuer Task mit Label `task:agent` wird in GitHub erstellt.
2. **Orchestrator Workflow** (`orchestrate.yml`) liest den Issue und ruft
   `scripts/orchestrate.py` auf, der auf Basis der Task‑Beschreibung einen
   Plan erstellt und passende Spezial‑Agenten aktiviert.
3. **Engineering Tasks** werden deterministisch ausgeführt (z. B. `normalize_leads.py`).
   Änderungen werden automatisch als PR erstellt; das **Merge** erfordert dein
   Review (Branch‑Protection).
4. **Growth/Communication** generiert Entwürfe (`generate_outreach.py`) und
   schreibt Drafts ins Repo bzw. intern in Slack. Das Senden von E‑Mails
   erfolgt nur über `send_messages.yml` nach Freigabe.
5. **Eval**/QA: Der `eval` Workflow führt Unit‑Tests und Smoke‑Evals aus.
6. **Deployment**: Der `release` Workflow deployt nach bestandenem Eval in
   `staging` und wartet in `production` auf Approval.

## Deterministic‑first

Der zentrale Grundsatz dieses Projekts lautet: **Deterministic‑first, AI‑last**.
Regeln und klassische Funktionen haben Vorrang – nur wenn sie scheitern oder
nicht ausreichen, eskalieren wir zur Nutzung eines Sprachmodells. Diese
Entscheidungslogik ist in `config/policies.yaml` definiert.

## Erweiterung

Dieses MVP lässt sich unkompliziert erweitern:
- **Live MCP‑Integrationen**: Ersetze die Stub‑Dateien in `tools/` durch echte
  Implementierungen. Hinterlege OAuth‑Tokens/Secrets via GitHub Secrets und
  setze `allow_outbound_email` bzw. `allow_slack_post` in
  `config/feature_flags.yaml` auf `true`.
- **Weitere Agenten**: Lege zusätzliche Ordner unter `agents/` an und
  erstelle passende Scripts.
- **Telemetry**: Integriere OpenTelemetry, Langfuse oder LangSmith, um
  Laufzeitmetriken zu erfassen und Evals zu automatisieren.