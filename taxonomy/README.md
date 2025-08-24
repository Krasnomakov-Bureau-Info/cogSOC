# Cognitive Civil Defense Taxonomy (CCDT)

_Requisite variety for individual & small‑group defense and counteraction._

## Table of Contents

- [Why this exists — a short scenario](#why-this-exists--a-short-scenario)
- [Legal & evidentiary rationale](#legal--evidentiary-rationale)
- [What this repository offers](#what-this-repository-offers)
- [CCDT Requisite Variety — Simple taxonomy for individuals](#CCDT-requisite-variety--simple-taxonomy-for-individuals)
- [Main goals](#main-goals)
- [What's included](#whats-included)
- [Core ideas](#core-ideas)
- [How to use](#how-to-use)
- [Simple handling steps (practical)](#simple-handling-steps-practical)
- [Streamlit viewers](#streamlit-viewers)
- [Quick run](#quick-run)
- [Notes](#notes)
- [Quick examples](#quick-examples)
- [Validation (node)](#validation-node)
- [Contributing](#contributing)
- [License & provenance](#license--provenance)
- [Psychological Resilience Module](#psychological-resilience-module)
- [Response Ladder (Tiered Response Catalog)](#response-ladder-tiered-response-catalog)

## Why this exists — a short scenario

Imagine you find yourself in a weird, unsettling situation: someone follows you, speaks as if they know more about you, tampers with your devices, or you notice repeated unexplained interactions. You report it to local authorities but they ask for evidence and can't help. You may be abroad, isolated, and unsure who is responsible. You have no clear status, no network of local contacts, and no organisations that can reliably help — especially with covert surveillance or psychological pressure.

This grey area is widely exploited by malicious actors and, in some cases, by intelligence services to influence or coerce individuals. The behaviours involved can look like psychological operations, espionage, targeted surveillance, or staged pressure campaigns. They are designed to gather information, shape behaviour, and create leverage over a person.

## Legal & evidentiary rationale

Legal, regulatory, and judicial systems (national and international) operate on explicit records: precedent, comparative case analysis, chains of custody, and reproducible evidence handling. Outcomes hinge less on isolated anecdotes and more on coherent, timestamped, consistently classified event history.

Why rigorous logging matters:
- Precedent alignment: Courts, regulators, and investigators map new fact patterns to prior cases. A structured log accelerates that linkage.
- Evidentiary weight: Numerous small, well‑described, time‑anchored events can collectively meet a threshold that single dramatic incidents cannot.
- Pattern articulation: Categorisation (code, category, vector, route) turns subjective impressions into analyzable series (frequency, escalation rate, novelty).
- Professional framing: A normalized taxonomy reduces emotional narration and increases signal density—mirroring how MITRE ATT&CK links TTPs to known threat groups with traceable references.
- Actionability: Investigators can pivot on codes (e.g., all physical proximity pressure events) or vectors (digital vs. narrative) to prioritize forensic tasks.
- Reproducibility: Clear definitions and evidence hints reduce ambiguity when multiple people contribute observations over weeks or months.

Analogy to ATT&CK: MITRE ATT&CK catalogs adversary TTPs and maps them to documented groups and campaigns; this taxonomy similarly catalogs harassment / coercion / disruption techniques so recurring behaviors become recognizable operational patterns rather than “random incidents.”

Practical result: A disciplined log evolves into a professional dossier—harder to ignore, easier to escalate deterministically, and better aligned with how law enforcement, regulators, or courts evaluate persistence, intent, harm, and proportional response.

Conclusion: Treat each observation as a potential evidentiary brick. Capture it once, in a standard form, with minimal interpretation. Over time the structured accumulation supplies the leverage (credibility, clarity, precedence mapping) that isolated complaints lack. This is how you convert lived experience into a defensible, referenceable case file.

## What this repository offers

This repository contains a small, practical framework that helps you:

- Categorise targeted attacks and disruptive techniques.
- Log observations in a consistent, machine-readable way.
- Track patterns over time so scattered incidents become evidence.

Why this matters: not every single event is a rules violation, but a well-kept record of many small incidents can reveal covert campaigns and strengthen any later complaint or report.

How it helps in practice:

- Open the app, find the event class that matches your observation, and log it.
- The system supports simple handling decisions (ignore, validate, escalate).
- Keep files of cases, events and observations. If the situation escalates, start collecting stronger evidence and present prepared files to authorities.

Persistence matters: a growing, dated record (10, 20, 100 entries) is harder to ignore and more useful when you need to escalate.

This is a simple, pragmatic approach to make covert operations and directed pressure visible and easier to challenge.

The repo and the framework are under active development and will gain more events and mitigation guidance over time.

# CCDT Requisite Variety — Simple taxonomy for individuals

This is a small, practical taxonomy for logging, tracking and analysing attacks and disruptive techniques aimed at individuals and small teams. It's inspired by structured frameworks such as MITRE ATT&CK and DISARM, but written for non-specialists: simple, compact and easy to extend.

Note: the project only has a light relation to the Universal Matrix appendix in this folder; the taxonomy stands on its own for everyday use.

### Main goals
- Keep entries small and human-readable.
- Cover common attack patterns against people (social, digital, physical, narrative).
- Enable simple queries and light automation.
- Provide a short, practical handling pattern you can follow during an incident.

### What's included
- `schema.json` — JSON Schema used to validate datasets.
- `requisite_variety_taxonomy.json` — seed dataset of objects.
- `event_classes.json` / `event_classes.csv` — intake categories used by viewers.
- Streamlit viewers: `streamlit_event_viewer.py` and `streamlit_navigator.py` (see below).
- `um_information_theory_appendix_v2.pdf` — appendix with background and suggested patterns.

### Core ideas
- Object types: disturbance, tactic, primitive, buffer, metric, tripwire, mitigation, event-class.
- IDs follow RV-<TYPE>-NNNN (for example `RV-DST-0001`).
- Each object is minimal: `id`, `type`, `name`, `description`, and optional links to related objects.

### How to use
- Log: record incidents as `event-class` entries or disturbances.
- Track: reference disturbance IDs in notes; attach metrics and tripwires for detection.
- Analyse: query relationships to reveal common tactics and effective mitigations.
 - Journal: open an event in the navigator, add / update a Note and Score, then press the Save button to append a timestamped snapshot to today's daily log (JSON). Each save creates (or updates) a file `taxonomy/journal/YYYY-MM-DD.json` holding a chronological list of entries for that date.
	 - Duplicate suppression: if you press Save again without changing the note or score for that event on the same day, it will not add a redundant entry.
	 - Daily grouping: use the Journal (Daily Log) section at the bottom of the navigator to pick a date, review all entries for that day, edit notes/scores inline, and re-save.
	 - Export: download the selected day’s log as JSON via the Download day JSON button (good for backup or external analysis).
	 - Structure of a journal entry: `timestamp`, `date`, `event_id`, `event_code`, `event_name`, `category`, `category_name`, `note`, `score`.
	 - Recommended practice: treat the note as an objective observation (what, where, when, actors, immediate evidence references), and defer interpretation / hypothesis to separate analytical summaries later. Keep one entry per discrete observation instance—even if the taxonomy event class is the same—to preserve frequency data.

### Simple handling steps (practical)
1. Detect — use metrics & tripwires to decide if an event needs action.
2. Contain — apply short-term buffers (isolate accounts, pause communications, limit exposure).
3. Select — pick a mitigation mapped to the identified tactic or primitive.
4. Learn — record outcomes and update tripwires/mitigations for the future.

For more theory and longer guidance see the appendix at `taxonomy/um_information_theory_appendix_v2.pdf`.

### Streamlit viewers
This folder includes two small Streamlit prototypes that help browse and annotate event classes:

- `streamlit_event_viewer.py` — filterable table view of `event_classes.csv` with download.
- `streamlit_navigator.py` — category tabs, quick enrichment, notes and scoring; can persist simple edits to the JSON files.

### Quick run

From the `taxonomy` directory:

```bash
# create a venv and install minimal deps (macOS / zsh)
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install streamlit pandas

# or run the navigator prototype
streamlit run streamlit_navigator.py

or

python3 -m streamlit run streamlit_navigator.py
```

### Notes
- The viewers are prototypes: they use local files (`event_classes.json`, `event_classes_enriched.json`) and will attempt to write small changes back to disk when you add entries or enrich records.
- Keep backups of your JSON/CSV files if you make edits via Streamlit.

### Quick examples
- List mitigation IDs for a disturbance with `jq`:

```bash
jq '.objects | map(select(.id=="RV-DST-0002").mitigations[])' requisite_variety_taxonomy.json
```

- Resolve mitigation objects:

```bash
jq '.objects | map(select(.id=="RV-MIT-0001" or .id=="RV-MIT-0002"))' requisite_variety_taxonomy.json
```

### Validation (node)

Install once (adds date-time format support via `ajv-formats`):

```bash
npm init -y # if you don't already have a package.json
npm install ajv ajv-formats --save-dev
```

Validate taxonomy dataset:

```bash
node taxonomy/validate.js
```

One‑liner alternative (inline, but harder to read):

```bash
node -e 'const fs=require("fs");const Ajv=require("ajv");const addFormats=require("ajv-formats");const ajv=new Ajv({allErrors:true,strict:false});addFormats(ajv);const s=JSON.parse(fs.readFileSync("taxonomy/schema.json"));const d=JSON.parse(fs.readFileSync("taxonomy/requisite_variety_taxonomy.json"));console.log(ajv.validate(s,d)?"VALID":"INVALID",ajv.errors||"")'
```

### Contributing
- Add new objects as `draft` and keep entries focused.
- Validate against `schema.json` before committing.
- Deprecate rather than delete to preserve references.
- clone, make new branch, make pull request 
- make issues 

### License & provenance
- Monada Dominion Non-Commercial No-Derivatives Source License (MD-NC-ND) v1.0

---

## Psychological Resilience Module

Resilience layer as a formal, lightweight module that runs alongside the protocol. The aim is to reduce cognitive load, prevent decision thrash, and keep physiology in a calm, steady state—so the system remains crisp, deterministic, and humane.

### Psychological resilience practices (attach to daily routine)

**Foundations (always-on)**

- One-inbox mind: Treat all stimuli as “events” to be processed later. No ad-hoc thinking or reacting outside the processing window. This preserves attention and reduces rumination.
- Minimal self-talk script: “Log it, label it, leave it.” Use this phrase whenever something spikes emotion. It anchors behavior to the protocol, not to feelings.
- Cadence-first outlook: The win condition is steady tempo (sleep, meals, work blocks, processing window). Consistency beats theatrics.

**Morning (pre-work, 10–15 minutes)**

- Orient-Set: 3 breaths in through nose (4 sec), out through mouth (6 sec), then note three things: today’s goal, today’s processing window, today’s non-negotiable (sleep time).
- Micro-commitment list: 3 smallest tasks that move life forward (not security tasks). Check one before opening the intake. This ensures life ≠ defense.
- Brief body activation: 3–5 minutes of light movement (walk, mobility flow). It downshifts baseline arousal and improves attentional stability.

**During processing (in-window)**

- Box breathing (4-4-4-4) before triage: 1 minute to lower sympathetic arousal.
- Label-first rule: Name the event (code), set the route (ignore/verify/harden/escalate), then (if needed) feel. Not the other way around.
- Time cap: 25–45 minutes per session. If not done, defer. Avoid “just one more” spirals.

**Midday (reset, 5–7 minutes)**

- State reset: 10 slow breaths + short walk or stretch + hydration. A predictable refocus breaks accumulation of tension.
- Media hygiene: No doom-scrolling. If compelling content appears, capture the link to the intake queue; don’t consume now.

**Evening (wind-down, 15–20 minutes)**

- Variance journal (2 minutes): Note anything surprising that changed your day. If none, write “none.” This normalizes stability and flags trend changes.
- Gratitude triad: 3 items (specific, small). Offsets threat-focused bias and reduces baseline anxiety.
- Sleep anchor ritual (10–15 minutes): Same sequence nightly (lights down, hygiene, breath or body scan). Keep devices out of the bedroom. Use constant, benign sound (fan/white noise).

**On-demand tools (use when triggered)**

- 3×3 grounding: Name 3 sights, 3 sounds, 3 bodily sensations. Repeat until arousal drops. Fast and portable.
- Cognitive defusion (index card): Write the thought “They are everywhere.” Add prefix: “I’m noticing the thought that…” Repeat. It loosens the thought’s grip without arguing with it.
- Postpone worry: Create a 10-minute “worry slot” after tomorrow’s processing window. If worry arises, jot a one-line cue and defer. This protects sleep and attention.
- Micro-relief stack: Sip water, wash face, step outside for 2 minutes. Change temperature and context to reset autonomic state quickly.

**Weekly maintenance**

- Social contact minimum: 1 meaningful conversation or activity unrelated to defense. Human connection is a resilience multiplier.
- Joy slot: 1–2 hours of intrinsically enjoyable activity (game, art, nature). Schedule it; protect it. This is fuel, not a luxury.
- Physical health checkpoint: Sleep average, movement minutes, protein/hydration basics. Physiology sets the ceiling for cognition under pressure.

**Boundaries and framing**

- “No live debates” rule: Never argue in DMs/comments. All disputes route to the trust anchor or formal channels. This prevents emotional capture.
- “Boring by design”: The more theatrical the environment, the more boring the response. Calm is a tactic, not a mood.
- Identity separation: You are not the protocol. It’s a tool you run. If you miss a window, you resume next window—no self-criticism loop.

**Team up with your future self**

- If-Then scripts: If sleep score worsens 3 days, then change sleep schema tonight. If decision latency >15 min, then tighten schema tomorrow. Remove choice in crises.
- Compassion clause: Treat errors as signals to improve buffers, not as personal failures. The system learns; that’s the point.

**Environment shaping**

- Attention guardrails: Home screen with only essential apps; grayscale mode in evenings; notifications off by default.
- Space cues: Dedicated corner or desk for processing; physically separate from leisure space to reduce spillover stress.
- Movement microdoses: 1–2 minutes each hour (stand, stretch, walk). Movement flushes stress chemistry and preserves focus.

**Emergency script (when overwhelmed)**

- Step 1: Stop. Sit. 10 slow breaths.
- Step 2: Write one line: “Current job: add this to queue.”
- Step 3: Add it to the intake queue. Close device. Take a 5-minute walk.
- Step 4: Resume scheduled activity. Process at next window. No exceptions.

**How this supports the system**

- Reduces H(A|D) in practice: scripted responses minimize action-selection uncertainty under stress.
- Preserves tempo: predictable rituals and bounded processing windows maintain cadence.
- Lowers variance: consistent sleep and on-demand resets keep physiology stable, reducing reactivity.
- Prevents over-escalation: “boring by design,” no debates, and formal channels avoid being dragged into adversary tempo.

**One-page checklist (printable)**

- Morning: 3 breaths, 3 aims, 1 micro-task, 3–5 min movement
- Processing: 1 min breathing, label→route→act, 25–45 min cap
- Midday: 10 breaths, stretch/walk, hydrate, no doom-scroll
- Evening: 2-min variance note, 3 gratitude, sleep anchor ritual
- On-demand: 3×3 grounding; “I’m noticing the thought that…”; postpone worry; micro-relief stack
- Weekly: joy slot, social contact, health checkpoint
- Rules: no live debates; trust anchor only; boring by design; if-then scripts; compassion clause

Add this module as a fixed part of the protocol. It keeps the human in the loop calm, precise, and steady—so the whole system remains reliable, scalable, and widely usable by anyone, even under pressure.

---

## Response Ladder (Tiered Response Catalog)

Tiered response catalog you can wire to your taxonomy and protocol. It’s ordered from highest escalation (systemic, formal, public) down to micro, reversible actions and finally “ignore.” Use deterministic routing: each event class maps to exactly one measure at the lowest tier that fully addresses it; escalate only on tripwires.

### Level 7 — Strategic, system-wide escalation (rare, high-impact)

- Multi-agency formal case bundle: compile signed dossier (timeline, evidence hashes, logs, affected accounts, witness statements), file with relevant regulators, ombuds, consumer protection, data protection authority, telecom regulator, and platform trust/safety in parallel.
- Coordinated legal action: engage counsel; send preservation letters; file civil claims (defamation, harassment, CFAA-like), injunction requests, and protective orders where applicable.
- Law enforcement referral: lodge a formal complaint with case numbers, attach evidence index; request incident numbers for chain-of-custody.
- Institutional escalation: notify employer/uni/association via compliance channels; request internal investigation with documented process.
- Media strategy: background brief to reputable journalists; provide verifiable artifacts, signed integrity proofs, and minimal narrative; consider NGO/advocacy partnerships.
- Third-party audits: independent forensic assessment (devices, network, accounts); publish signed executive summary.
- Contingency relocation/identity protections: temporary relocation; confidential address services; credit freeze and identity monitoring.

### Level 6 — Cross-jurisdiction and platform escalation

- Cross-platform takedown wave: synchronized submissions to all platforms implicated (impersonation, doxxing, coordinated harassment).
- Regulator notifications: privacy commissioner/DPA complaint (processing without basis), telecom complaints (SIM swap), consumer authority (unfair practices).
- Corporate trust & safety escalation: verified reporter channels, enterprise abuse desks (if you have business accounts).
- Data broker opt-out batch: purge/opt-out requests with signed identity attestations.

### Level 5 — Formalization and public anchoring

- Trust anchor publication: signed statement of verification policy, contact protocol, and official channels for claims; include public keys/fingerprints.
- Public integrity proofs: signed hashes of critical documents, timelines, and device state; reproducible build manifests where relevant.
- Case register page: minimal, regularly updated index of case IDs (police, regulator, platform) to centralize references without re-litigating in social feeds.
- Cease-and-desist notices: template letters to specific actors/entities when identified.

### Level 4 — Targeted containment and restoration

- Deep-clean escalation: fresh OS install with selective restore; rotate device fleet over maintenance window; migrate critical accounts to hardware keys; revoke all tokens/sessions.
- Credential and recovery hardening: regenerate passwords, rotate recovery emails/phones, regenerate recovery codes; remove legacy auth methods.
- Network rebaseline: new router firmware/config; split SSIDs/VLANs; DNS over HTTPS with known resolver; disable UPnP; audit port forwards.
- Account hygiene sweep: remove unused apps, disconnect third-party integrations, enable login alerts; tighten privacy settings.
- Identity integrity countermeasures: verified profile banners linking to trust anchor; verified handles where available; takedowns of clones/typosquats.
- Physical risk reduction: predictable-but-nondisclosive schedules; check-in protocol with trusted contact; documented route variations.

### Level 3 — Operational buffers and automation

- Canonical intake pipeline: one inbox, schema-based event capture, near-duplicate collapse, hashing, and auto-labeling.
- Deterministic triage automation: rules engine mapping event codes to actions (IGNORE, VERIFY, HARDEN, ESCALATE) with tie-breaking by risk → reversibility → info gain.
- Notification discipline: batch windows, no real-time engagement with theater; time-shifted processing to break coupling.
- Content signing automation: one-click signing/hashing and posting to trust anchor; template-driven statements.
- Monitoring dashboards: DNR (distinct novelty rate), decision latency, incident counts, sleep score; threshold alerts.
- Evidence vault: append-only, timestamped, hashed storage for artifacts; exportable case bundles.

### Level 2 — Minimal, reversible countermeasures

- Account-level: rotate single credential; enable/confirm 2FA; revoke active sessions; review recent security events.
- Device-level: remove high-risk apps; permission audit; disable developer options/sideloading; reset network settings; re-check profiles/configs.
- Network-level: forget untrusted SSIDs; rotate Wi-Fi passphrase; disable WPS; toggle MAC randomization.
- Communication hygiene: move sensitive conversations to a single, verified channel; turn off read receipts/active status globally.
- Narrative hygiene: post a short, signed clarification only when there’s an active impersonation—otherwise point to trust anchor.
- Physical micro-variations: adjust departure windows ±10 minutes; alternate pre-vetted routes; avoid ad-hoc confrontations.
- Sleep integrity: pre-sleep anchor, no devices in bedroom, constant white noise, fixed wake time.

### Level 1 — Documentation, deferral, and pruning

- Document: capture screenshots, headers, logs; note time/place/actors; hash artifacts; add to event record.
- Defer: batch for next processing window; avoid real-time reactions.
- Prune: close unused accounts; uninstall nonessential apps; disable inbox rules/filters; consolidate channels; disable notifications from untrusted sources.
- Mute/Block/Report: apply platform tools without engaging; submit minimal evidence via form.

### Level 0 — Ignore (default for non-actionable theater)

- Ignore unverifiable, non-intersecting theatrics by policy; log once, no engagement, no amplification.

### Tripwire examples (to jump tiers deterministically)

- ≥2 verified account intrusions in 7 days → escalate to Level 4 deep-clean.
- ≥3 impersonations across distinct platforms in 30 days → Level 5 trust anchor + coordinated takedown (Level 6 if platforms fail).
- Decision latency median >15 min for 3 days → tighten schemas, add pre-triage filters (Level 3).
- Sleep disruption score ≥3 for 3 consecutive nights → environmental changes and device exclusion (Level 2); if persists → professional consult (Level 4 targeted).
- Physical tailing confirmed ≥3 times in a week on fixed routes → check-in protocol + predictable windows (Level 4); file incident if escalation continues (Level 6/7).

### Routing guidance

- Map each taxonomy event code to a minimum effective level; do not skip levels.
- Only escalate when a defined tripwire is breached or a higher level is explicitly required (e.g., legal harm).
- All public communications should be templated, signed, and minimal; point back to the trust anchor.

### Artifacts and templates to prepare now

- Dossier template (index, timeline, evidence list with hashes, incident summaries, ask).
- Regulator/LE complaint templates per jurisdiction (fill-in fields, attachments list).
- Platform impersonation/takedown templates with evidence checklist.
- Trust anchor boilerplate (verification policy, keys, contact protocol).
- One-click signing/hashing scripts and export-to-bundle function.
- Intake schema (JSON) and a codebook mapping event classes → default level, evidence hints, and escalation tripwires.

This gives a full ladder from “file comprehensive cases and brief media” down to “ignore.” Hook it into your pipeline so a single labeled observation deterministically picks the least necessary action, and let metrics handle when to climb the ladder.