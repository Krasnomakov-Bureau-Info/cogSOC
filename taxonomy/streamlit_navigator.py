import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="Requisite Variety Navigator", layout="wide")
st.title("Requisite Variety Navigator (Prototype)")

BASE = Path(__file__).parent
JSON_EVENTS = BASE / "event_classes.json"
JSON_ENRICHED = BASE / "event_classes_enriched.json"

@st.cache_data(show_spinner=False)
def load_events():
    with JSON_EVENTS.open() as f:
        data = json.load(f)
    return data

@st.cache_data(show_spinner=False)
def load_enriched():
    if JSON_ENRICHED.exists():
        with JSON_ENRICHED.open() as f:
            try:
                enriched_list = json.load(f)
            except Exception:
                return {}
        return {e['id']: e for e in enriched_list}
    return {}

if 'events_data' not in st.session_state:
    st.session_state.events_data = load_events()
if 'enriched_map' not in st.session_state:
    st.session_state.enriched_map = load_enriched()

events = st.session_state.events_data
enriched_map = st.session_state.enriched_map

# Group by category
cats = {}
cat_meta = {}
for ev in events:
    cats.setdefault(ev['category'], []).append(ev)
    cat_meta[ev['category']] = ev['category_name']

# Sort events inside each category by code for stability
for k in cats:
    cats[k] = sorted(cats[k], key=lambda r: r['code'])

ordered_categories = sorted(cats.keys())  # A .. U

# Sidebar controls
with st.sidebar:
    st.header("Filters & Options")
    view_mode = st.radio("View mode", ["Tabs"], help="Matrix view can be added later.")
    search = st.text_input("Search techniques (name/code/id)")
    routes_all = sorted({ev['default_route'] for ev in events})
    sel_routes = st.multiselect("Default route", routes_all, default=routes_all)
    show_only_enriched = st.checkbox("Only enriched", value=False, help="Show only techniques present in enriched JSON")
    st.markdown("---")
    st.subheader("Add New Event")
    add_help = st.caption("Create a new event-class entry. Auto ID will be assigned.")
    with st.expander("New event form", expanded=False):
        # Derive category options from existing data
        categories_existing = sorted({(ev['category'], ev['category_name']) for ev in events}, key=lambda x: x[0])
        cat_codes = [c[0] for c in categories_existing]
        cat_display = {c: n for c, n in categories_existing}
        with st.form("add_event_form", clear_on_submit=True):
            sel_cat = st.selectbox("Category", cat_codes, format_func=lambda c: f"{c} – {cat_display[c]}")
            cat_name = cat_display[sel_cat]
            name_new = st.text_input("Technique name *")
            default_route_new = st.selectbox("Default route", options=routes_all)
            # Optional enrichment
            with st.expander("Optional enrichment"):
                sev = st.selectbox("Severity", options=["", "low", "medium", "high", "critical"], index=0)
                vector = st.text_input("Vector")
                impacts = st.text_area("Impacts (one per line)")
                evidence_hints = st.text_area("Evidence hints (one per line)")
            # Code helper
            def slugify(txt: str) -> str:
                import re
                core = re.sub(r"[^A-Za-z0-9]+", "-", txt.strip()).strip('-')
                return core.upper()
            suggested_code = f"{sel_cat}-{slugify(name_new)[:40]}" if name_new else ""
            code_new = st.text_input("Code *", value=suggested_code, help="Unique code; adjust if needed")
            submit_new = st.form_submit_button("Add Event")
            if submit_new:
                errors = []
                if not name_new:
                    errors.append("Name required")
                if not code_new:
                    errors.append("Code required")
                if any(ev['code'] == code_new for ev in events):
                    errors.append("Code already exists")
                if errors:
                    st.error("; ".join(errors))
                else:
                    # Generate next ID
                    try:
                        max_id_num = max(int(ev['id'].split('-')[-1]) for ev in events)
                    except ValueError:
                        max_id_num = 0
                    new_id = f"RV-EVT-{max_id_num+1:04d}"
                    new_event = {
                        'id': new_id,
                        'code': code_new,
                        'category': sel_cat,
                        'category_name': cat_name,
                        'name': name_new,
                        'default_route': default_route_new
                    }
                    # Update in-session list
                    st.session_state.events_data.append(new_event)
                    # Persist events JSON (sorted by id numeric)
                    try:
                        sorted_events = sorted(st.session_state.events_data, key=lambda e: int(e['id'].split('-')[-1]))
                        JSON_EVENTS.write_text(json.dumps(sorted_events, indent=2))
                        load_events.clear()
                    except Exception as e:
                        st.warning(f"Failed to write events file: {e}")
                    # Optional enrichment persistence
                    if any([sev, vector, impacts, evidence_hints]):
                        enr_entry = {
                            'id': new_id,
                            'severity': sev or None,
                            'vector': vector or None,
                            'impacts': [ln.strip() for ln in impacts.splitlines() if ln.strip()] or None,
                            'evidence_hints': [ln.strip() for ln in evidence_hints.splitlines() if ln.strip()] or None
                        }
                        # Refresh enrichment map
                        st.session_state.enriched_map[new_id] = {k:v for k,v in enr_entry.items() if v}
                        try:
                            JSON_ENRICHED.write_text(json.dumps(list(st.session_state.enriched_map.values()), indent=2))
                            load_enriched.clear()
                        except Exception as e:
                            st.warning(f"Failed to write enrichment file: {e}")
                    st.success(f"Added {new_id}")
                    st.experimental_rerun()
    st.markdown("---")
    st.caption("Click a technique to expand details, add a note & score. Export below.")

# Prepare filtered data
search_lower = search.lower().strip()

def pass_filters(ev):
    if ev['default_route'] not in sel_routes:
        return False
    if show_only_enriched and ev['id'] not in enriched_map:
        return False
    if search_lower:
        blob = f"{ev['id']} {ev['code']} {ev['name']} {ev['category_name']}".lower()
        if search_lower not in blob:
            return False
    return True

# Session state for notes & scores
if 'notes' not in st.session_state:
    st.session_state.notes = {}
if 'scores' not in st.session_state:
    st.session_state.scores = {}

# Severity color mapping helper
SEV_COLORS = {
    'low': '#6fbf73',
    'medium': '#f2c744',
    'high': '#f28c28',
    'critical': '#e55353'
}

def render_event(ev):
    enr = enriched_map.get(ev['id'])
    title = ev['name']
    if enr and enr.get('severity'):
        sev = enr['severity'].lower()
        badge_map = {
            'low': '🟢 LOW',
            'medium': '🟡 MED',
            'high': '🟠 HIGH',
            'critical': '🔴 CRIT'
        }
        badge = badge_map.get(sev, enr['severity'].upper())
        title = f"{badge} · {title}"
    exp = st.expander(title, expanded=False)
    with exp:
        col1, col2, col3 = st.columns([1.3,1,1])
        col1.markdown(f"**ID:** {ev['id']}  ")
        col1.markdown(f"**Code:** {ev['code']}")
        col2.markdown(f"**Category:** {ev['category']} – {ev['category_name']}")
        col2.markdown(f"**Default route:** `{ev['default_route']}`")
        if enr:
            sev = enr.get('severity')
            vector = enr.get('vector')
            impacts = enr.get('impacts')
            hints = enr.get('evidence_hints')
            if sev:
                col3.markdown(f"**Severity:** {sev}")
            if vector:
                col3.markdown(f"**Vector:** {vector}")
            if impacts:
                st.markdown("**Impacts:**")
                st.write(impacts)
            if hints:
                st.markdown("**Evidence hints:**")
                st.write(hints)
        # Notes & scoring
        note_key = ev['id']
        existing_note = st.session_state.notes.get(note_key, "")
        st.text_area("Note", key=f"note_{note_key}", value=existing_note, placeholder="Add analytical note...")
        score_val = st.session_state.scores.get(note_key, 0)
        st.slider("Score", 0, 100, key=f"score_{note_key}", value=score_val, help="Arbitrary scoring scale (0-100)")
        # Persist back when changed
        st.session_state.notes[note_key] = st.session_state.get(f"note_{note_key}", "")
        st.session_state.scores[note_key] = st.session_state.get(f"score_{note_key}", 0)

if view_mode == "Tabs":
    tabs = st.tabs([f"{c} – {cat_meta[c]}" for c in ordered_categories])
    for idx, cat in enumerate(ordered_categories):
        with tabs[idx]:
            cat_events = [ev for ev in cats[cat] if pass_filters(ev)]
            st.caption(f"{len(cat_events)} techniques in this category after filters")
            for ev in cat_events:
                render_event(ev)

# Export section
export_payload = []
for ev in events:
    ev_id = ev['id']
    if ev_id in st.session_state.notes or ev_id in st.session_state.scores:
        export_payload.append({
            'id': ev_id,
            'code': ev['code'],
            'note': st.session_state.notes.get(ev_id, ""),
            'score': st.session_state.scores.get(ev_id, 0)
        })

st.markdown("---")
colA, colB = st.columns([1,2])
with colA:
    if export_payload:
        export_json = json.dumps(export_payload, indent=2).encode()
        st.download_button("Download notes & scores JSON", data=export_json, file_name="event_notes_scores.json", mime="application/json")
    else:
        st.caption("No notes or scores to export yet.")
with colB:
    st.caption("Prototype: future enhancements could include a full matrix layout, color gradients, bulk scoring, linkage overlays, and enrichment editing.")
