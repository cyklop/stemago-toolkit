---
name: storm-research
description: "Verwende wenn der User eine STORM-Recherche will, den storm-research-Skill nennt, 'storm this', 'STORM-Briefing zu X', 'mehrperspektivische Recherche' sagt, oder ein quellenverifiziertes HTML-Research-Briefing zu einem Thema braucht, bei dem mehrere Blickwinkel und faktengeprüfte Aussagen zählen. Produziert ein self-contained HTML-Briefing aus fünf Experten-Perspektiven mit Primärquellen-Verifikation. NICHT für schnelle Faktenabfragen (Overkill), Ideen-Validierung (dafür /roast), oder Feature-Planung mit Spec (dafür /interview)."
argument-hint: "[Thema der Recherche]"
---

# STORM Research

## Worum es geht

Macht aus einem Thema ein verifiziertes, mehrperspektivisches HTML-Briefing. Fünf Experten-Lenses recherchieren das Thema, eine Contradiction-Map legt offen wo sie sich widersprechen, alles wird zu einem self-contained HTML-Report synthetisiert — der sich dann selbst adversarial peer-reviewt und jede Zitation gegen ihre Primärquelle prüft, bevor er ausgeliefert wird. Ergebnis: eine HTML-Datei ohne blinde Flecken und ohne ungeprüfte Aussagen.

Fahre die Pipeline End-to-End. Kürze keine Phase ab. Das ist schwerer als eine schnelle Web-Abfrage — genau das ist der Punkt. **Report-Inhalt auf Deutsch**; die Lens- und Verifier-Prompts unten bleiben **englisch verbatim** (kalibriert — nicht übersetzen).

**Abgrenzung:** `/roast` validiert eine *Idee* (GO/KILL). `/interview` plant ein *Feature* (Spec/Tasks). STORM *recherchiert ein Thema* multi-perspektivisch und quellenverifiziert. Der externe `deep-research`-Skill macht generischen Such-Fan-out → Report; STORM unterscheidet sich durch feste Perspektiven-Lenses, Contradiction-Map, designtes HTML-Briefing und Claim-Safety-Guide.

## Portabilität

Self-contained. Hängt nur an built-in Tools (`Agent` mit `general-purpose`, `Write`, Websuche/-fetch in den Agents) plus `report-template.html` in diesem Ordner. Keine externen Skripte, APIs oder anderen Skills nötig.

## Phase 0: Thema scopen

1. Enthält `$ARGUMENTS` das Thema → nutzen. Sonst fragen, was recherchiert werden soll.
2. Deine Interpretation des Themas in einer Zeile festhalten und weitermachen. Nur nachfragen, wenn das Thema echt mehrdeutig ist auf eine Art die die Recherche verändert. Default: weitermachen.
3. Die **Rolle des Lesers** bestimmen, damit die Handlungsempfehlung sie treffen kann. Aus Thema/Kontext ableiten; wenn unklar, in einer Zeile fragen oder default „Praktiker oder Entscheider in diesem Feld".
4. Einen kebab-case `topic-slug` fürs Dateinamen-Schema ableiten.
5. Dem User in einer Zeile sagen, dass die Pipeline läuft (5 Lenses, dann Verifikation).

## Phase 1: Fünf Experten-Lenses (parallele Agents)

Starte **fünf `general-purpose`-Agents in EINEM Message-Block**, damit sie parallel laufen. Jeder bekommt dasselbe Themen-Framing plus seine Lens. Nutze **exakt** diese Prompts (englisch, verbatim), ersetze `{TOPIC}` und ein einzeiliges `{TOPIC_FRAME}` (deine Phase-0-Interpretation):

**1. THE PRACTITIONER** — `You are THE PRACTITIONER for: {TOPIC} ({TOPIC_FRAME}). You work with this daily. Do real web research (prioritize recent sources, case studies, practitioner threads, operator data). Surface the GAP between what hands-on operators know and what academics/pundits miss, and the practical realities (workflow friction, what actually works, where it breaks) that get ignored. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each with a concrete data point/case/named source + URL. 3) THE ONE THING only a practitioner would say. Cite real sources with URLs. Under 400 words.`

**2. THE ACADEMIC** — `You are THE ACADEMIC for: {TOPIC} ({TOPIC_FRAME}). You care about peer-reviewed evidence and effect sizes, not anecdotes. Do real web research (peer-reviewed studies, arXiv, university and research-institute reports, journals). Answer: what does the rigorous evidence ACTUALLY say vs popular belief, and where does it CONTRADICT the hype. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each tied to a named study/report + URL with the actual finding/effect size. 3) THE ONE THING only an academic would say. Flag where evidence is thin or contested, and note peer-review status (published vs preprint). Under 400 words.`

**3. THE SKEPTIC** — `You are THE SKEPTIC for: {TOPIC} ({TOPIC_FRAME}). You think the mainstream view is overstated or wrong. Build the STRONGEST steelman bear case. Do real web research for backlash, failures, contradicting data, policy/regulatory changes, debunkings. Answer: the strongest counterargument, and what proponents conveniently ignore. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each with a concrete source + URL. 3) THE ONE THING only a skeptic would say. Be rigorous, not contrarian for sport. Cite real sources with URLs. Under 400 words.`

**4. THE ECONOMIST** — `You are THE ECONOMIST for: {TOPIC} ({TOPIC_FRAME}). You follow the money. Do real web research for revenues, valuations, market size, funding flows, unit economics, incentives. Answer: who profits from the current narrative, and what financial incentives shape the research and hype. Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each with a real number (revenue/valuation/market size/funding) + named source + URL. 3) THE ONE THING only an economist would say (the follow-the-money insight). Cite real figures with URLs. Under 400 words.`

**5. THE HISTORIAN** — `You are THE HISTORIAN for: {TOPIC} ({TOPIC_FRAME}). You have seen disruption cycles before and look for patterns. Do real web research for genuine historical parallels (prior technologies, manias, market shifts). Answer: what parallels actually fit, and what we learn from how they played out (who won, who lost, what stabilized). Return EXACTLY: 1) CORE POSITION in 2 sentences. 2) STRONGEST EVIDENCE, 3-5 bullets each a specific historical case with dates/outcomes + a source URL. 3) THE ONE THING only a historian would say (the pattern no one else surfaces). Cite sources with URLs. Under 400 words.`

Wenn alle fünf zurück sind, poste eine 2-3-Zeilen-Notiz im Chat (auf Deutsch): wohin sie konvergieren, und der schärfste Dissens. Rohe Briefs NICHT in den Chat (die Agents haben sie schon zurückgegeben).

## Phase 2: Die Widersprüche mappen

Nur aus den fünf Briefs, inline (keine Agents):

1. **Direkte Konflikte** — wo zwei oder mehr Lenses das Gegenteil behaupten. Die konkret kollidierenden Aussagen benennen, nicht nur Themen.
2. **Stärkste vs. schwächste Evidenz** — welche Lens am besten gestützt ist (Rang: peer-reviewt kausal > offizielle Daten > Anekdote/Analogie) und welche am schwächsten, mit Begründung.
3. **Die auflösende Frage** — die eine empirische Frage, die den größten Widerspruch entscheiden würde.
4. **Universelle Übereinstimmung** — was jede Lens bestätigt, sogar Gegner. Der wahrscheinlich wahre, tragende Befund.
5. **Der blinde Fleck** — was KEINE Lens adressiert hat. Wird zur „fehlenden 6. Lens" und speist die Frontier-Frage.

Diese Map ist kein eigenes Deliverable. Sie ist das Rohmaterial für die Findings (supports/challenges), die verborgene Verbindung, die 6.-Lens-Box und die Frontier-Frage im Report.

## Phase 3: Den HTML-Report synthetisieren

1. Lies `report-template.html` in diesem Skill-Ordner. Klone es; baue das CSS **nicht** neu.
2. Fülle jede Sektion **auf Deutsch**. Mapping aus den Phasen:
   - **60-Sekunden-Zusammenfassung** — entscheider-tauglich, Nuance statt Schlagzeile. Erst der gesicherte Fakt, dann die umstrittene Interpretation.
   - **5 Kernbefunde, nach Verlässlichkeit sortiert** — die wichtigsten jetzt gesicherten Dinge, höchste Verlässlichkeit zuerst. Jeder trägt einen Confidence-Score 1-10 (in Phase 4 gesetzt) und Gestützt-von/Angezweifelt-von-Chips aus der Contradiction-Map.
   - **Verborgene Verbindung** — der nicht-offensichtliche Link aus Phase 2, der nur über alle fünf Lenses erscheint.
   - **Kernannahme / fehlende 6. Lens** — der blinde Fleck aus Phase 2, als Lens die die Schlüsse ändern könnte.
   - **Handlungsempfehlung** — 3-6 konkrete Züge für die in Phase 0 bestimmte Leser-Rolle. Konkret, nicht abstrakt.
   - **Claim-Safety-Guide** — behaupten / mit Vorbehalt / vermeiden, nach der Phase-4-Verifikation befüllt.
   - **Frontier-Frage** — die eine Frage, die alles ändern würde.
   - **Quellen** — jede Zitation mit Verifikations-Status-Tag (in Phase 4 gesetzt).
3. Schreibe nach `docs/research/{topic-slug}-storm.html` (relativ zum Working Directory; Ordner anlegen falls nötig).

## Phase 4: Adversariales Peer-Review + Verifikation (nicht überspringen)

Das trennt STORM von einem normalen Report. Vor der Auslieferung ausführen.

**4a. Self-Review (inline).** Jeden der 5 Befunde 1-10 auf Verlässlichkeit scoren und begründen. Das schwächste Glied identifizieren und was es verifizieren würde. Bias-Check (welche Lens die Synthese dominiert hat, was untergewichtet wurde). Die fehlende 6. Perspektive benennen. Eine ehrliche Gesamtnote vergeben.

**4b. Jede Zitation verifizieren (parallele Agents).** Starte `general-purpose`-Agents in einem Message-Block, einen pro Zitations-Cluster (verwandte Claims gruppieren; ~4-6 Agents). Prompt je Agent (englisch, verbatim):

`Independently verify a citation against its PRIMARY source. Be skeptical; do not trust secondary blog summaries. CLAIM: {claim + cited figure + named source}. Find the actual primary source. Confirm or correct: exact title/authors/venue/year/URL, the real figure or effect size as published, sample/method and any author-stated limits, and peer-review status (published vs preprint). For any contested claim, find the strongest credible counter-source. Return: VERDICT = CONFIRMED / PARTIALLY CONFIRMED (list corrections) / UNVERIFIED / FALSE, then the corrected one-line citation, then 2-4 bullets of specifics with the primary URL. Under 280 words.`

**4c. Korrekturen anwenden.** Den Report editieren:
- Falsche Zahlen, Titel, Daten oder Mischcharakterisierungen fixen.
- Confidence-Scores runterstufen wo die Evidenz dünn war; Preprints und umstrittene Claims in die „Umstrittenes Signal"-Sidebar demoten.
- Einzel-Umfrage- oder beauftragte Statistiken ehrlich re-attribuieren.
- Das Verifikations-Banner füllen (`X erfunden, Y korrigiert, Z abgestuft`) und die Per-Zitation-Status-Tags.
- Den Claim-Safety-Guide aus den Verdikten befüllen.

## Output

1. Finales Deliverable: `docs/research/{topic-slug}-storm.html` (die v2, post-Verifikation).
2. Für den User öffnen: macOS `open <pfad>`. Wenn das OS unklar ist, einfach den Pfad geben.
3. Im Chat (deutsch, knapp): der Dateipfad, die Verifikations-Bilanz (`N/N geprüft, X erfunden, Y korrigiert, Z abgestuft`), der eine universelle Befund, die Frontier-Frage, und die Claim-Safety-Kurzfassung (was sicher behauptbar ist vs. vermeiden).

## Regeln & Guardrails

- **Nur echte Recherche.** Jede Lens und jede Zitation muss auf eine reale, gefetchte Quelle zurückgehen. Keine erfundenen Studien, Zahlen oder URLs. Nicht verifizierbare Zahl → demoten oder streichen, nie übertünchen.
- **Das Panel ist selbst gebaut.** Immer im Report offenlegen. Übereinstimmung über Lenses ist eine starke Hypothese, kein unabhängiger Beweis. Konvergenz nicht als Fachkonsens ausgeben.
- **Verifikation ist Pflicht.** Ein Report ohne Phase 4 ist kein STORM-Report. Das Verifikations-Banner muss wahrhaftig sein.
- **Verlässlichkeit = Evidenzqualität, nicht Confidence.** Nach der Quellen-Hierarchie scoren: peer-reviewt kausal > offizielle Politik-/Finanzdaten > einzelne beauftragte Umfrage > Analogie > Preprint.
- **Den Leser adressieren, keine Default-Person.** Handlungsempfehlung und Claim-Safety-Guide sprechen die in Phase 0 bestimmte Rolle an.
- **Kosten.** ~9-11 Agents pro Lauf. Das ist erwartet. Nicht breiter fächern als fünf Lenses bzw. ein Verifier pro Zitations-Cluster.
- **Design.** Sauberes Weiß, professionell (Montserrat / Roboto Mono, blauer Akzent). Template-CSS verbatim halten. Keinen anderen Visual-Style einsetzen.
