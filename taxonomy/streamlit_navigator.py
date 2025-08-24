import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="CCDT Navigator", layout="wide")
st.title("Cognitive Civil Defense Taxonomy (CCDT) – Navigator (Prototype)")
st.caption("Requisite variety for individual and small-group defense & counteraction")

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
    view_mode = st.radio(
        "View mode",
        ["Tabs", "Matrix", "Table"],
        help="Tabs: per-category expanders. Matrix: flat editable list. Table: all categories side-by-side like ATT&CK Navigator."
    )
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
                    # Streamlit >=1.27 provides st.rerun; older versions used experimental_rerun
                    if hasattr(st, "rerun"):
                        st.rerun()
                    elif hasattr(st, "experimental_rerun"):
                        st.experimental_rerun()
    st.markdown("---")
    st.caption("Click a technique to expand details, add a note & score. Export below.")
    # Table view display options
    if view_mode == "Table":
        st.markdown("---")
        st.subheader("Table View Options")
        horizontal_scroll = st.checkbox("Horizontal scroll mode (read-only)", value=False, help="Show all categories in a wide horizontally scrollable strip with hover tooltips (no inline editing). Uncheck for paged interactive expanders.")
        if not horizontal_scroll:
            table_cols_per_page = st.slider("Columns per page", 4, 10, 6, help="Reduce number to widen each column; horizontal paging across category groups.")
            total_pages = (len(ordered_categories) + table_cols_per_page - 1) // table_cols_per_page
            table_page = st.number_input("Category page", min_value=1, max_value=total_pages, value=1, step=1, help=f"Navigate pages (total {total_pages})")
            st.session_state.__setitem__('table_cols_per_page', table_cols_per_page)
            st.session_state.__setitem__('table_page', table_page)
        st.session_state.__setitem__('table_horizontal_scroll', horizontal_scroll)

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
            details = enr.get('details')
            mitigations = enr.get('mitigation_suggestions')
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
            if details:
                st.markdown("**Details:**")
                st.write(details)
            if mitigations:
                st.markdown("**Mitigation suggestions:**")
                st.write(mitigations)
        # Notes & scoring
        note_key = ev['id']
        existing_note = st.session_state.notes.get(note_key, "")
        st.text_area("Note", key=f"note_{note_key}", value=existing_note, placeholder="Add analytical note...")
        score_val = st.session_state.scores.get(note_key, 0)
        st.slider("Score", 0, 100, key=f"score_{note_key}", value=score_val, help="Arbitrary scoring scale (0-100)")
        # Persist back when changed
        st.session_state.notes[note_key] = st.session_state.get(f"note_{note_key}", "")
        st.session_state.scores[note_key] = st.session_state.get(f"score_{note_key}", 0)

def render_event_compact(ev):
    """Compact expander for matrix/table layout with inline note & score editing."""
    enr = enriched_map.get(ev['id'])
    sev = (enr.get('severity') if enr else None)
    sev_norm = (sev or '').upper()
    sev_map = {"LOW":"🟢 LOW","MED":"🟡 MED","HIGH":"🟠 HIGH","CRITICAL":"🔴 CRIT"}
    badge = sev_map.get(sev_norm, "")
    title = f"{badge} {ev['code']}".strip()
    with st.expander(title, expanded=False):
        st.markdown(f"**{ev['name']}**")
        st.caption(f"ID {ev['id']} | Cat {ev['category']} | Route `{ev['default_route']}`")
        if enr:
            if enr.get('vector'):
                st.caption(f"Vector: {enr['vector']}")
            if enr.get('impacts'):
                st.caption("Impacts: " + ", ".join(enr['impacts']))
            if enr.get('details'):
                st.write(enr['details'])
        note_key = ev['id']
        st.text_area("Note", key=f"table_note_{note_key}", value=st.session_state.notes.get(note_key, ""), label_visibility='collapsed', placeholder='Note...')
        st.slider("Score", 0, 100, key=f"table_score_{note_key}", value=st.session_state.scores.get(note_key, 0))
        # Sync back
        st.session_state.notes[note_key] = st.session_state.get(f"table_note_{note_key}", "")
        st.session_state.scores[note_key] = st.session_state.get(f"table_score_{note_key}", 0)

if view_mode == "Tabs":
    tabs = st.tabs([f"{c} – {cat_meta[c]}" for c in ordered_categories])
    for idx, cat in enumerate(ordered_categories):
        with tabs[idx]:
            cat_events = [ev for ev in cats[cat] if pass_filters(ev)]
            st.caption(f"{len(cat_events)} techniques in this category after filters")
            for ev in cat_events:
                render_event(ev)
elif view_mode == "Matrix":
    import pandas as pd
    flat_rows = []
    for ev in events:
        if not pass_filters(ev):
            continue
        enr = enriched_map.get(ev['id'], {})
        sev = (enr.get('severity') or '').upper()
        # Normalize severity variants (low/LOW etc.)
        sev_map = {"LOW":"LOW","MED":"MED","MEDIUM":"MED","HIGH":"HIGH","CRIT":"CRITICAL","CRITICAL":"CRITICAL"}
        sev_std = sev_map.get(sev, sev)
        flat_rows.append({
            'ID': ev['id'],
            'Code': ev['code'],
            'Category': ev['category'],
            'Category Name': ev['category_name'],
            'Name': ev['name'],
            'Route': ev['default_route'],
            'Severity': sev_std,
            'Note': st.session_state.notes.get(ev['id'], ""),
            'Score': st.session_state.scores.get(ev['id'], 0)
        })
    df = pd.DataFrame(flat_rows)
    st.caption(f"Matrix view: {len(df)} techniques after filters. Edit Note/Score cells; press Apply to persist.")
    editable_cols = ['Note', 'Score']
    if not df.empty:
        edited = st.data_editor(
            df,
            hide_index=True,
            column_config={
                'Score': st.column_config.NumberColumn(min_value=0, max_value=100, step=1),
                'Severity': st.column_config.TextColumn(help="Severity (read-only from enrichment)")
            },
            disabled=[c for c in df.columns if c not in editable_cols],
            key='matrix_editor'
        )
        if st.button("Apply matrix edits"):
            for _, row in edited.iterrows():
                ev_id = row['ID']
                st.session_state.notes[ev_id] = row['Note'] or ""
                try:
                    st.session_state.scores[ev_id] = int(row['Score']) if row['Score'] != "" else 0
                except Exception:
                    st.session_state.scores[ev_id] = 0
            st.success("Matrix edits applied. Export section updated.")
    else:
        st.info("No techniques match current filters.")
elif view_mode == "Table":
    # Build filtered events per category (maintain original ordering)
    filtered_by_cat = {cat: [ev for ev in cats[cat] if pass_filters(ev)] for cat in ordered_categories}
    if st.session_state.get('table_horizontal_scroll'):
        # Horizontal scroll implementation (read-only, hover tooltips)
        max_rows = max((len(v) for v in filtered_by_cat.values()), default=0)
        if max_rows == 0:
            st.info("No techniques match current filters.")
        else:
            st.caption("Table view (horizontal scroll): hover a code to see full name; expand for details (read-only). Use other modes for editing notes & scores.")
            st.markdown(
                """
                <style>
                .rv-hscroll-wrapper {overflow-x:auto; padding-bottom:0.5rem;}
                .rv-flex {display:flex; gap:1rem; min-width:max-content;}
                .rv-col {flex:0 0 260px;}
                .rv-col h4 {margin:0 0 .25rem 0; font-size:0.9rem; white-space:nowrap;}
                .rv-evt summary {cursor:pointer; list-style:none;}
                .rv-evt summary::-webkit-details-marker {display:none;}
                .rv-evt {border:1px solid #444; border-radius:6px; margin-bottom:6px; padding:2px 6px; background:#1f2226;}
                .rv-evt:hover {border-color:#666; background:#262a2f;}
                .rv-code {font-size:0.75rem; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;}
                .rv-sev-low{color:#6fbf73;} .rv-sev-med{color:#f2c744;} .rv-sev-high{color:#f28c28;} .rv-sev-critical{color:#e55353;}
                .rv-meta {font-size:0.65rem; opacity:0.75;}
                </style>
                """,
                unsafe_allow_html=True
            )
            # Build HTML
            html_cols = []
            for cat in ordered_categories:
                col_events = filtered_by_cat[cat]
                parts = [f"<div class='rv-col'><h4>{cat} – {cat_meta[cat]}</h4>"]
                for ev in col_events:
                    enr = enriched_map.get(ev['id'], {})
                    sev = (enr.get('severity') or '').upper()
                    sev_cls = {"LOW":"rv-sev-low","MED":"rv-sev-med","HIGH":"rv-sev-high","CRITICAL":"rv-sev-critical"}.get(sev,"")
                    sev_label = f"<span class='{sev_cls}'>{sev}</span> " if sev else ""
                    tooltip = f"{ev['name']}".replace('"','&quot;')
                    parts.append(
                        f"<details class='rv-evt'><summary class='rv-code' title=\"{tooltip}\">{sev_label}{ev['code']}</summary>"
                        f"<div class='rv-meta'>ID {ev['id']} | Route {ev['default_route']}</div>"
                        f"<div style='font-size:0.7rem; line-height:1.1'>{ev['name']}</div>"
                        f"</details>"
                    )
                parts.append("</div>")
                html_cols.append("".join(parts))
            st.markdown(f"<div class='rv-hscroll-wrapper'><div class='rv-flex'>{''.join(html_cols)}</div></div>", unsafe_allow_html=True)
            with st.expander("Legend"):
                st.markdown("Hover shows full name via tooltip. Severity color: green=LOW yellow=MED orange=HIGH red=CRITICAL.")
    else:
        # Pagination for categories to avoid ultra-narrow columns with interactive expanders
        cols_per = st.session_state.get('table_cols_per_page', 6)
        page = st.session_state.get('table_page', 1)
        start_idx = (page - 1) * cols_per
        end_idx = start_idx + cols_per
        page_cats = ordered_categories[start_idx:end_idx]
        max_rows = max((len(v) for v in filtered_by_cat.values()), default=0)
        if max_rows == 0:
            st.info("No techniques match current filters.")
        else:
            st.caption(f"Table view: expandable cells; edit notes & scores inline. Showing categories {start_idx+1}-{min(end_idx, len(ordered_categories))} of {len(ordered_categories)}.")
            header_cols = st.columns(len(page_cats))
            for col, cat in zip(header_cols, page_cats):
                col.markdown(f"**{cat} – {cat_meta[cat]}**")
            for i in range(max_rows):
                row_cols = st.columns(len(page_cats))
                for col, cat in zip(row_cols, page_cats):
                    evs = filtered_by_cat[cat]
                    if i < len(evs):
                        with col:
                            render_event_compact(evs[i])
                    else:
                        col.write("")
            with st.expander("Legend"):
                st.markdown("Emoji legend: 🟢 LOW · 🟡 MED · 🟠 HIGH · 🔴 CRITICAL. Compact cells duplicate note/score state with other views.")

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
