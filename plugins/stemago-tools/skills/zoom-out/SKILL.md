---
name: zoom-out
description: "Eine Abstraktionsebene hochgehen und einen Überblick über den relevanten Code bekommen. Verwende wenn du einen unbekannten Codeabschnitt verstehen, Module und deren Verbindungen mappen, oder den größeren Kontext rund um eine Stelle sehen willst. Auch bei: 'was macht dieser Code eigentlich', 'zeig mir den größeren Zusammenhang', 'ich verstehe nicht wie das zusammenhängt', 'wo wird das aufgerufen'."
disable-model-invocation: true
---

Ich kenne diesen Codebereich noch nicht gut genug. Geh eine Abstraktionsebene höher.

Zeige mir eine Karte — keinen Code:

1. **Welche Module/Dateien** sind hier relevant?
2. **Wer ruft das auf** (Caller-Map — wer nutzt diese Komponente)?
3. **Was wird genutzt** (Dependencies — welche anderen Module stecken drin)?
4. **Wo ist die Grenze** dieses Subsystems — was gehört dazu, was nicht?

Verwende Domänen-Sprache aus `CONTEXT.md` (falls vorhanden).
Orientierung vor Implementierungsdetails.
