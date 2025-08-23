## Why this exists — a short scenario

Imagine you find yourself in a weird, unsettling situation: someone follows you, speaks as if they know more about you, tampers with your devices, or you notice repeated unexplained interactions. You report it to local authorities but they ask for evidence and can't help. You may be abroad, isolated, and unsure who is responsible. You have no clear status, no network of local contacts, and no organisations that can reliably help — especially with covert surveillance or psychological pressure.

This grey area is widely exploited by malicious actors and, in some cases, by intelligence services to influence or coerce individuals. The behaviours involved can look like psychological operations, espionage, targeted surveillance, or staged pressure campaigns. They are designed to gather information, shape behaviour, and create leverage over a person.

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

# Requisite Variety — Simple taxonomy for individuals

This is a small, practical taxonomy for logging, tracking and analysing attacks and disruptive techniques aimed at individuals and small teams. It's inspired by structured frameworks such as MITRE ATT&CK and DISARM, but written for non-specialists: simple, compact and easy to extend.

Note: the project only has a light relation to the Universal Matrix appendix in this folder; the taxonomy stands on its own for everyday use.

Main goals
- Keep entries small and human-readable.
- Cover common attack patterns against people (social, digital, physical, narrative).
- Enable simple queries and light automation.
- Provide a short, practical handling pattern you can follow during an incident.

What's included
- `schema.json` — JSON Schema used to validate datasets.
- `requisite_variety_taxonomy.json` — seed dataset of objects.
- `event_classes.json` / `event_classes.csv` — intake categories used by viewers.
- Streamlit viewers: `streamlit_event_viewer.py` and `streamlit_navigator.py` (see below).
- `um_information_theory_appendix_v2.pdf` — appendix with background and suggested patterns.

Core ideas
- Object types: disturbance, tactic, primitive, buffer, metric, tripwire, mitigation, event-class.
- IDs follow RV-<TYPE>-NNNN (for example `RV-DST-0001`).
- Each object is minimal: `id`, `type`, `name`, `description`, and optional links to related objects.

How to use
- Log: record incidents as `event-class` entries or disturbances.
- Track: reference disturbance IDs in notes; attach metrics and tripwires for detection.
- Analyse: query relationships to reveal common tactics and effective mitigations.

Simple handling steps (practical)
1. Detect — use metrics & tripwires to decide if an event needs action.
2. Contain — apply short-term buffers (isolate accounts, pause communications, limit exposure).
3. Select — pick a mitigation mapped to the identified tactic or primitive.
4. Learn — record outcomes and update tripwires/mitigations for the future.

For more theory and longer guidance see the appendix at `taxonomy/um_information_theory_appendix_v2.pdf`.

Streamlit viewers
This folder includes two small Streamlit prototypes that help browse and annotate event classes:

- `streamlit_event_viewer.py` — filterable table view of `event_classes.csv` with download.
- `streamlit_navigator.py` — category tabs, quick enrichment, notes and scoring; can persist simple edits to the JSON files.

Quick run (from the `taxonomy` directory)

```bash
# create a venv and install minimal deps (macOS / zsh)
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install streamlit pandas

# run the event table viewer
streamlit run streamlit_event_viewer.py

or

python3 -m streamlit run streamlit_event_viewer.py

# or run the navigator prototype
streamlit run streamlit_navigator.py

or

python3 -m streamlit run streamlit_navigator.py
```

Notes
- The viewers are prototypes: they use local files (`event_classes.json`, `event_classes_enriched.json`) and will attempt to write small changes back to disk when you add entries or enrich records.
- Keep backups of your JSON/CSV files if you make edits via Streamlit.

Quick examples
- List mitigation IDs for a disturbance with `jq`:

```bash
jq '.objects | map(select(.id=="RV-DST-0002").mitigations[])' requisite_variety_taxonomy.json
```

- Resolve mitigation objects:

```bash
jq '.objects | map(select(.id=="RV-MIT-0001" or .id=="RV-MIT-0002"))' requisite_variety_taxonomy.json
```

Validation (node)

```bash
node -e 'const fs=require("fs");const Ajv=require("ajv");const ajv=new Ajv({allErrors:true});const schema=JSON.parse(fs.readFileSync("taxonomy/schema.json"));const data=JSON.parse(fs.readFileSync("taxonomy/requisite_variety_taxonomy.json"));console.log(ajv.validate(schema,data)?"VALID":"INVALID", ajv.errors||"")'
```

Contributing
- Add new objects as `draft` and keep entries focused.
- Validate against `schema.json` before committing.
- Deprecate rather than delete to preserve references.

License & provenance
- Seeded from operational experience and open research. See the appendix for sources and theory.