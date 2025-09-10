# AI Company (HITL-first)

Dieses Repository enthält die Grundstruktur für ein agentisches Unternehmen mit Human‑in‑the‑Loop. Es ist darauf ausgelegt, innerhalb kürzester Zeit einsatzbereit zu sein und folgt dabei dem Prinzip **„Deterministic‑first, AI‑last“** (siehe unten).

## Features
- **Orchestrator-Agent** koordiniert mehrere Spezial-Agenten (Research, Engineer/Codex, Growth, Eval, Compliance).
- **GitHub-first Governance**: Jede Änderung geht über Issues, PRs und Environments mit manuellem Approval.
- **HITL**: Keine externe Aktion (E-Mail, Deploy, Budget) ohne menschliche Freigabe.
- **CI/CD**: Workflows für Smoke-Evals, Secret-Scanning, CodeQL-Security-Scans und Deployments.
- **Compliance**: Vorlagen für AI-Hinweis, Impressum, Datenschutz; EU AI Act und DSGVO-Art. 22 berücksichtigt.

## Quickstart
1. **Repo klonen** und in GitHub ein neues Repository erstellen.
2. **Secrets setzen**: `OPENAI_API_KEY` (weitere nach Bedarf).
3. **Branch-Protection & Environments** einrichten: `main` geschützt, `staging`/`production` mit Required Reviewers.
4. **Issue "Go-to-Market Sprint 1"** mit Label `task:agent` öffnen, um den Orchestrator zu starten (orchestrate Workflow).
5. **PRs reviewen**: Merges auf `main` nur nach bestandenem Eval und Approval.

## Betriebsprinzip
Dieses Projekt verfolgt einen **Deterministic‑first, AI‑last**‑Ansatz. Aufgaben werden, soweit möglich, zuerst mit deterministischen Funktionen, Regeln oder klassischen Algorithmen umgesetzt. Nur wenn diese Ansätze scheitern (z. B. weil die Spezifikation unvollständig ist, die Recall‑Rate unter 80 % liegt oder eine Generierung von Freitext erforderlich ist), eskaliert der Orchestrator zur Nutzung eines großen Sprachmodells (LLM). Selbst dann gilt: jede außenwirksame Aktion (E‑Mail, Deploy, Finanzausgabe) passiert ausschließlich nach deiner manuellen Freigabe via GitHub (Human‑in‑the‑Loop).

## Ordnerstruktur
Siehe die Unterordner (`.github`, `agents`, `scripts`, `docs`, `kb`, `sales`, `outreach`, `finance`, `reports`, `sops`, `config`).

### How it works (ai-company)
- Label `task:agent` auf ein Issue → Orchestrator erstellt Plan + kommentiert Link → triggert Engineer/Growth.
- **Engineer** ergänzt Tests/Policies/Ack und öffnet PR. **Growth** erstellt Drafts/Ack und öffnet PR.
- Du reviewst & mergest (HITL). Branches werden nach Merge gelöscht.
- Secret Scan (soft) + bestehende Eval laufen als Checks.

## How to trigger & merge (HITL)
1. Issue mit Label `task:agent` öffnen oder labeln – oder `workflow_dispatch` im Orchestrator nutzen.
2. Orchestrator kommentiert den Plan-Link und startet Agenten bzw. erstellt Fallback‑PRs.
3. PRs prüfen, `eval`‑Status abwarten und manuell mergen. Jeder PR enthält `Closes #<nr>`.

## Troubleshooting
- **Queued Runs:** Repo‑Minuten aufgebraucht oder Sichtbarkeit zu gering. Manuell via `workflow_dispatch` erneut starten.
- **Permissions:** Bei Forks `pull_request_target` nutzen. GITHUB_TOKEN muss `contents`/`pull-requests`/`issues` Rechte haben.
- **Labels fehlen:** Workflow `Sync labels` laufen lassen und sicherstellen, dass Issues das Label `task:agent` tragen.

## E2E-Testplan
1. Neues Issue mit Label `task:agent` öffnen (oder vorhandenes labeln).
2. Orchestrator kommentiert den Plan-Link und triggert Agenten.
3. Falls kein Agent-Run erkannt wird, erstellt der Orchestrator Fallback-PRs mit Ack-Dateien.
4. `eval`-Workflow läuft und setzt Commit-Status `eval`.
5. Nach grünem Status manuell mergen – der PR enthält `Closes #<nr>` und schließt das Issue.

