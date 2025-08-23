
Tiered response catalog you can wire to your taxonomy and protocol. It’s ordered from highest escalation (systemic, formal, public) down to micro, reversible actions and finally “ignore.” Use deterministic routing: each event class maps to exactly one measure at the lowest tier that fully addresses it; escalate only on tripwires.

Level 7 — Strategic, system-wide escalation (rare, high-impact)

- Multi-agency formal case bundle: compile signed dossier (timeline, evidence hashes, logs, affected accounts, witness statements), file with relevant regulators, ombuds, consumer protection, data protection authority, telecom regulator, and platform trust/safety in parallel.
- Coordinated legal action: engage counsel; send preservation letters; file civil claims (defamation, harassment, CFAA-like), injunction requests, and protective orders where applicable.
- Law enforcement referral: lodge a formal complaint with case numbers, attach evidence index; request incident numbers for chain-of-custody.
- Institutional escalation: notify employer/uni/association via compliance channels; request internal investigation with documented process.
- Media strategy: background brief to reputable journalists; provide verifiable artifacts, signed integrity proofs, and minimal narrative; consider NGO/advocacy partnerships.
- Third-party audits: independent forensic assessment (devices, network, accounts); publish signed executive summary.
- Contingency relocation/identity protections: temporary relocation; confidential address services; credit freeze and identity monitoring.

Level 6 — Cross-jurisdiction and platform escalation

- Cross-platform takedown wave: synchronized submissions to all platforms implicated (impersonation, doxxing, coordinated harassment).
- Regulator notifications: privacy commissioner/DPA complaint (processing without basis), telecom complaints (SIM swap), consumer authority (unfair practices).
- Corporate trust \& safety escalation: verified reporter channels, enterprise abuse desks (if you have business accounts).
- Data broker opt-out batch: purge/opt-out requests with signed identity attestations.

Level 5 — Formalization and public anchoring

- Trust anchor publication: signed statement of verification policy, contact protocol, and official channels for claims; include public keys/fingerprints.
- Public integrity proofs: signed hashes of critical documents, timelines, and device state; reproducible build manifests where relevant.
- Case register page: minimal, regularly updated index of case IDs (police, regulator, platform) to centralize references without re-litigating in social feeds.
- Cease-and-desist notices: template letters to specific actors/entities when identified.

Level 4 — Targeted containment and restoration

- Deep-clean escalation: fresh OS install with selective restore; rotate device fleet over maintenance window; migrate critical accounts to hardware keys; revoke all tokens/sessions.
- Credential and recovery hardening: regenerate passwords, rotate recovery emails/phones, regenerate recovery codes; remove legacy auth methods.
- Network rebaseline: new router firmware/config; split SSIDs/VLANs; DNS over HTTPS with known resolver; disable UPnP; audit port forwards.
- Account hygiene sweep: remove unused apps, disconnect third-party integrations, enable login alerts; tighten privacy settings.
- Identity integrity countermeasures: verified profile banners linking to trust anchor; verified handles where available; takedowns of clones/typosquats.
- Physical risk reduction: predictable-but-nondisclosive schedules; check-in protocol with trusted contact; documented route variations.

Level 3 — Operational buffers and automation

- Canonical intake pipeline: one inbox, schema-based event capture, near-duplicate collapse, hashing, and auto-labeling.
- Deterministic triage automation: rules engine mapping event codes to actions (IGNORE, VERIFY, HARDEN, ESCALATE) with tie-breaking by risk → reversibility → info gain.
- Notification discipline: batch windows, no real-time engagement with theater; time-shifted processing to break coupling.
- Content signing automation: one-click signing/hashing and posting to trust anchor; template-driven statements.
- Monitoring dashboards: DNR (distinct novelty rate), decision latency, incident counts, sleep score; threshold alerts.
- Evidence vault: append-only, timestamped, hashed storage for artifacts; exportable case bundles.

Level 2 — Minimal, reversible countermeasures

- Account-level: rotate single credential; enable/confirm 2FA; revoke active sessions; review recent security events.
- Device-level: remove high-risk apps; permission audit; disable developer options/sideloading; reset network settings; re-check profiles/configs.
- Network-level: forget untrusted SSIDs; rotate Wi-Fi passphrase; disable WPS; toggle MAC randomization.
- Communication hygiene: move sensitive conversations to a single, verified channel; turn off read receipts/active status globally.
- Narrative hygiene: post a short, signed clarification only when there’s an active impersonation—otherwise point to trust anchor.
- Physical micro-variations: adjust departure windows ±10 minutes; alternate pre-vetted routes; avoid ad-hoc confrontations.
- Sleep integrity: pre-sleep anchor, no devices in bedroom, constant white noise, fixed wake time.

Level 1 — Documentation, deferral, and pruning

- Document: capture screenshots, headers, logs; note time/place/actors; hash artifacts; add to event record.
- Defer: batch for next processing window; avoid real-time reactions.
- Prune: close unused accounts; uninstall nonessential apps; disable inbox rules/filters; consolidate channels; disable notifications from untrusted sources.
- Mute/Block/Report: apply platform tools without engaging; submit minimal evidence via form.

Level 0 — Ignore (default for non-actionable theater)

- Ignore unverifiable, non-intersecting theatrics by policy; log once, no engagement, no amplification.

Tripwire examples (to jump tiers deterministically)

- ≥2 verified account intrusions in 7 days → escalate to Level 4 deep-clean.
- ≥3 impersonations across distinct platforms in 30 days → Level 5 trust anchor + coordinated takedown (Level 6 if platforms fail).
- Decision latency median >15 min for 3 days → tighten schemas, add pre-triage filters (Level 3).
- Sleep disruption score ≥3 for 3 consecutive nights → environmental changes and device exclusion (Level 2); if persists → professional consult (Level 4 targeted).
- Physical tailing confirmed ≥3 times in a week on fixed routes → check-in protocol + predictable windows (Level 4); file incident if escalation continues (Level 6/7).

Routing guidance

- Map each taxonomy event code to a minimum effective level; do not skip levels.
- Only escalate when a defined tripwire is breached or a higher level is explicitly required (e.g., legal harm).
- All public communications should be templated, signed, and minimal; point back to the trust anchor.

Artifacts and templates to prepare now

- Dossier template (index, timeline, evidence list with hashes, incident summaries, ask).
- Regulator/LE complaint templates per jurisdiction (fill-in fields, attachments list).
- Platform impersonation/takedown templates with evidence checklist.
- Trust anchor boilerplate (verification policy, keys, contact protocol).
- One-click signing/hashing scripts and export-to-bundle function.
- Intake schema (JSON) and a codebook mapping event classes → default level, evidence hints, and escalation tripwires.

This gives a full ladder from “file comprehensive cases and brief media” down to “ignore.” Hook it into your pipeline so a single labeled observation deterministically picks the least necessary action, and let metrics handle when to climb the ladder.

