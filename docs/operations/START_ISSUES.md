# Start‑Issues

Dieses Dokument beschreibt die ersten drei Issues, die du nach dem Aufsetzen
des Repositories erstellen solltest. Sie initialisieren das deterministische
Framework und demonstrieren, wie der Orchestrator Agenten aktiviert.

## 1. [TASK] Deterministic-first Gate aktivieren

**Ziel:** Policies und README ergänzen, damit der deterministische Ansatz
verbindlich ist. Der Orchestrator soll bei Einsatz eines LLMs begründen,
warum dies nötig ist.

**Akzeptanzkriterien:**
* `config/policies.yaml` enthält `strategy.mode = deterministic_first`.
* `README.md` beschreibt das Betriebsprinzip.
* Das Issue erhält einen Kommentar vom Orchestrator mit der Begründung für
  (oder gegen) eine Eskalation zum LLM.

## 2. [TASK] Lead-Parsing v1 (deterministisch)

**Ziel:** CSV‑Validierung und Normalisierung von Leads als reines Python‑Skript
(`scripts/normalize_leads.py`) implementieren. Keine LLMs einsetzen.

**Akzeptanzkriterien:**
* Pflichtfelder (Company, Name oder Role, EmailOrURL) werden geprüft.
* Zwei Ausgabedateien: `sales/leads.normalized.csv` und
  `sales/leads.rejected.csv`.
* Unit‑Tests (`pytest`) decken die wichtigsten Fälle ab.

## 3. [TASK] Outreach-Entwürfe nur bei Eskalation

**Ziel:** Outreach‑Generator so implementieren, dass er standardmäßig ein
Template aus `kb/playbooks/outreach_style.md` verwendet. Nur wenn das
Template nicht ausreicht, soll ein LLM (optional) eingesetzt werden.

**Akzeptanzkriterien:**
* Drafts werden in `outreach/drafts/` erstellt.
* Keine E‑Mails werden ohne weiteres versendet; die Empfänger müssen über
  das `send_messages` Workflow explizit freigegeben werden.