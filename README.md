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
test eval
