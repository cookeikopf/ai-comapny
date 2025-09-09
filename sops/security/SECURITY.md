## Sicherheitsrichtlinien

- **Least Privilege**: Zugriffsschlüssel (Secrets) werden ausschließlich als GitHub-Environment-Secrets gespeichert. Nur nötige Berechtigungen gewähren.
- **Rotation**: Alle Secrets werden mindestens alle 90 Tage rotiert.
- **Secret-Scanning**: Automatische Prüfung jeder Commit- und PR-Änderung auf versehentliche Schlüsseloffenlegung (siehe secret-scan Workflow).
- **Keine PII in Logs**: Persönlich identifizierbare Informationen (PII) dürfen weder in PR-Beschreibungen noch in Logs auftauchen. Daten müssen pseudonymisiert werden, bevor sie an Modelle übergeben werden.
- **Kill-Switch**: Pro Agent existieren Feature-Flags, um Funktionen im Notfall abzuschalten. Außerdem gelten Rate- und Budget-Limits, um exzessive Nutzung zu verhindern.