import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(page_title="DataFix — Workbench", layout="wide", page_icon="🧰")

# ==========================================
# DESIGN SYSTEM
# Concept: a physical workbench for tidying messy data.
# Warm parchment surfaces, wood-toned dividers, sage = clean,
# rust = needs attention. Space Grotesk for structure, JetBrains
# Mono for anything that is actually data.
# ==========================================
def load_css():
    st.markdown("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>

    :root {
        --paper: #F6F1E7;
        --paper-deep: #EDE4D3;
        --card: #FFFDF8;
        --ink: #2B2620;
        --ink-soft: #6B6255;
        --line: #DCD0B8;
        --sage: #6B8F71;
        --sage-deep: #56765C;
        --rust: #BF5B2E;
        --rust-soft: #F3E1D4;
        --sage-soft: #E4ECE2;
    }

    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
        color: var(--ink);
    }

    .stApp {
        background:
            radial-gradient(circle at 100% 0%, rgba(191,91,46,0.05), transparent 40%),
            var(--paper);
    }

    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1180px;
    }

    h1, h2, h3, h4 {
        font-family: 'Space Grotesk', sans-serif !important;
        color: var(--ink) !important;
        letter-spacing: -0.01em;
    }

    /* ---------- Header band ---------- */
    .bench-header {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        border-bottom: 2px solid var(--ink);
        padding-bottom: 0.9rem;
        margin-bottom: 1.6rem;
    }
    .bench-title {
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 700;
        font-size: 1.9rem;
        letter-spacing: -0.02em;
    }
    .bench-title span { color: var(--sage-deep); }
    .bench-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--ink-soft);
        background: var(--card);
        border: 1px solid var(--line);
        padding: 0.3rem 0.6rem;
        border-radius: 4px;
    }

    /* ---------- Sidebar: pegboard ---------- */
    [data-testid="stSidebar"] {
        background-color: var(--paper-deep) !important;
        border-right: 1px solid var(--line) !important;
    }
    [data-testid="stSidebar"] .block-container { padding-top: 2rem; }

    .peg-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: var(--ink-soft);
        margin-bottom: 0.6rem;
        border-bottom: 1px dashed var(--line);
        padding-bottom: 0.4rem;
    }

    /* Station radio -> tool tags hanging on the pegboard */
    .stRadio [role="radiogroup"] { gap: 0.5rem; }
    .stRadio label {
        border: 1px solid var(--line) !important;
        border-radius: 6px !important;
        padding: 0.7rem 0.9rem !important;
        background-color: var(--card) !important;
        transition: all 0.15s ease;
        font-family: 'Space Grotesk', sans-serif;
        font-weight: 500;
        box-shadow: 0 1px 0 rgba(43,38,32,0.04);
    }
    .stRadio label:hover {
        border-color: var(--sage) !important;
        transform: translateX(2px);
    }
    .stRadio div[aria-checked="true"] label {
        background-color: var(--ink) !important;
        border-color: var(--ink) !important;
        color: var(--paper) !important;
        font-weight: 600;
    }

    /* ---------- Cards / metrics ---------- */
    [data-testid="stMetric"] {
        background: var(--card);
        border: 1px solid var(--line);
        border-radius: 10px;
        padding: 1.1rem 1.3rem;
        box-shadow: 0 1px 2px rgba(43,38,32,0.05);
    }
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
        font-size: 2.1rem !important;
        color: var(--ink) !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.72rem !important;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--sage-deep) !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricDelta"] svg { display: none; }

    /* ---------- Data tables ---------- */
    .stDataFrame {
        border: 1px solid var(--line) !important;
        border-radius: 8px !important;
        overflow: hidden;
    }
    .stDataFrame [data-testid="stDataFrameResizable"] { font-family: 'JetBrains Mono', monospace; }

    /* ---------- Section label (pegboard tag above each block) ---------- */
    .tag {
        display: inline-block;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: var(--ink-soft);
        border: 1px solid var(--line);
        border-radius: 4px;
        padding: 0.15rem 0.5rem;
        margin-bottom: 0.5rem;
    }

    /* ---------- Alerts ---------- */
    div[data-testid="stAlertContentSuccess"] { color: var(--sage-deep) !important; }
    div[data-testid="stAlertContentInfo"] { color: var(--ink-soft) !important; }
    .stAlert {
        border-radius: 8px !important;
        border: 1px solid var(--line) !important;
        background: var(--card) !important;
    }

    /* ---------- Buttons ---------- */
    .stDownloadButton button, .stButton button {
        background-color: var(--sage) !important;
        color: #FFFDF8 !important;
        border: none !important;
        border-radius: 7px !important;
        font-weight: 600 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        padding: 0.6rem 1.3rem !important;
        transition: all 0.15s ease;
    }
    .stDownloadButton button:hover, .stButton button:hover {
        background-color: var(--sage-deep) !important;
        box-shadow: 0 2px 8px rgba(107,143,113,0.35);
    }

    /* ---------- Divider ---------- */
    hr { border-color: var(--line) !important; }

    /* ---------- File uploader ---------- */
    [data-testid="stFileUploaderDropzone"] {
        background: var(--card) !important;
        border: 1.5px dashed var(--line) !important;
        border-radius: 8px !important;
    }

    </style>
    """, unsafe_allow_html=True)


def section_tag(label):
    st.markdown(f'<div class="tag">{label}</div>', unsafe_allow_html=True)


# ==========================================
# TESTED LOGIC (prototyped in Colab)
# ==========================================

def remove_duplicates(df, subset_cols=None):
    n_duplicates = int(df.duplicated(subset=subset_cols).sum())
    if n_duplicates == 0:
        return df.copy(), "No duplicates found — data is already clean on this check.", 0
    cleaned_df = df.drop_duplicates(subset=subset_cols, keep="first")
    col_info = "all columns" if not subset_cols else f"columns: {', '.join(subset_cols)}"
    log = f"{n_duplicates} duplicate row(s) removed (checked {col_info})."
    return cleaned_df.reset_index(drop=True), log, n_duplicates


def clean_text_and_dates(df, text_cols=None, date_cols=None):
    cleaned = df.copy()
    changes = 0
    notes = []

    for col in (text_cols or []):
        if col not in cleaned.columns:
            continue
        before = cleaned[col].astype(str)
        after = before.str.strip()
        after = after.apply(lambda x: re.sub(r"\s+", " ", x))
        after = after.str.title()
        changed = (before != after).sum()
        cleaned[col] = after
        changes += int(changed)
        if changed:
            notes.append(f"{changed} value(s) tidied in '{col}' (whitespace/casing).")

    for col in (date_cols or []):
        if col not in cleaned.columns:
            continue
        before = cleaned[col]
        parsed = pd.to_datetime(before, errors="coerce", dayfirst=True)
        failed = int(parsed.isna().sum() - before.isna().sum())
        cleaned[col] = parsed.dt.strftime("%Y-%m-%d")
        reformatted = int((before.astype(str) != cleaned[col].astype(str)).sum())
        changes += reformatted
        note = f"{reformatted} date(s) standardized to YYYY-MM-DD in '{col}'."
        if failed > 0:
            note += f" {failed} value(s) could not be parsed and were left blank."
        notes.append(note)

    log = " ".join(notes) if notes else "No columns selected — nothing changed yet."
    return cleaned, log, changes


def merge_files(df_left, df_right, key_left, key_right, how="left"):
    merged = df_left.merge(
        df_right, left_on=key_left, right_on=key_right,
        how="outer", indicator=True
    )
    matched = int((merged["_merge"] == "both").sum())
    left_only = int((merged["_merge"] == "left_only").sum())
    right_only = int((merged["_merge"] == "right_only").sum())
    log = f"{matched} row(s) matched. {left_only} unmatched from file 1, {right_only} unmatched from file 2."
    return merged, log, matched, left_only, right_only


def build_summary(df, group_col, value_col=None):
    if value_col and value_col != "(count only)":
        summary = df.groupby(group_col)[value_col].agg(["count", "sum", "mean"]).reset_index()
        summary.columns = [group_col, "count", "total", "average"]
        summary["total"] = summary["total"].round(2)
        summary["average"] = summary["average"].round(2)
    else:
        summary = df.groupby(group_col).size().reset_index(name="count")
    return summary.sort_values(summary.columns[-1], ascending=False)


def to_csv_bytes(df):
    buf = BytesIO()
    df.to_csv(buf, index=False)
    return buf.getvalue()


# ==========================================
# APP
# ==========================================
load_css()

st.markdown(
    '<div class="bench-header">'
    '<div class="bench-title">🧰 Data<span>Fix</span></div>'
    '<div class="bench-tag">workbench for messy spreadsheets</div>'
    '</div>',
    unsafe_allow_html=True
)

# --- Sidebar: the pegboard ---
st.sidebar.markdown('<div class="peg-label">Stations</div>', unsafe_allow_html=True)
station = st.sidebar.radio(
    "Choose a station",
    ["1 · Dedupe", "2 · Clean Text & Dates", "3 · Merge Files", "4 · Summary Report"],
    label_visibility="collapsed"
)

st.sidebar.markdown('<div class="peg-label" style="margin-top:1.6rem;">Main File</div>', unsafe_allow_html=True)
uploaded_file = st.sidebar.file_uploader(
    "Upload a spreadsheet", type=["csv", "xlsx"],
    help="CSV or Excel, up to 200MB", label_visibility="collapsed"
)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        st.session_state.df = df
        st.session_state.filename = uploaded_file.name
    except Exception as e:
        st.sidebar.error(f"Couldn't read that file: {e}")

has_file = "df" in st.session_state

# ==========================================
# STATION 1 — DEDUPE
# ==========================================
if station == "1 · Dedupe":
    st.header("Remove Duplicates")
    if not has_file:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df
        section_tag("settings")
        selected_cols = st.multiselect(
            "Check for duplicates across:", options=list(df.columns),
            default=[], placeholder="Leave empty to check all columns"
        )
        subset = selected_cols if selected_cols else None
        cleaned_df, log, n_dup = remove_duplicates(df, subset)

        st.divider()
        c1, c2, c3 = st.columns([1, 1, 2])
        c1.metric("BEFORE", f"{df.shape[0]:,} rows")
        c2.metric("AFTER", f"{cleaned_df.shape[0]:,} rows", delta=f"-{n_dup:,}", delta_color="inverse")
        with c3:
            st.success(log) if n_dup == 0 else st.warning(log)
        st.divider()

        section_tag("preview")
        p1, p2 = st.columns(2)
        with p1:
            st.caption("Raw")
            st.dataframe(df.head(30), use_container_width=True, height=280)
        with p2:
            st.caption("Cleaned")
            st.dataframe(cleaned_df.head(30), use_container_width=True, height=280)

        st.download_button("📥 Download cleaned file", to_csv_bytes(cleaned_df),
                            file_name=f"deduped_{st.session_state.filename.rsplit('.',1)[0]}.csv",
                            mime="text/csv", use_container_width=True)

# ==========================================
# STATION 2 — CLEAN TEXT & DATES
# ==========================================
elif station == "2 · Clean Text & Dates":
    st.header("Clean Text & Dates")
    if not has_file:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df
        section_tag("settings")
        s1, s2 = st.columns(2)
        with s1:
            text_cols = st.multiselect("Text columns to tidy (whitespace + casing):", options=list(df.columns))
        with s2:
            date_cols = st.multiselect("Date columns to standardize:", options=list(df.columns))

        cleaned_df, log, changes = clean_text_and_dates(df, text_cols, date_cols)

        st.divider()
        c1, c2 = st.columns([1, 3])
        c1.metric("VALUES CHANGED", f"{changes:,}")
        with c2:
            st.info(log) if changes == 0 else st.success(log)
        st.divider()

        section_tag("preview")
        p1, p2 = st.columns(2)
        with p1:
            st.caption("Raw")
            st.dataframe(df.head(30), use_container_width=True, height=280)
        with p2:
            st.caption("Cleaned")
            st.dataframe(cleaned_df.head(30), use_container_width=True, height=280)

        st.download_button("📥 Download cleaned file", to_csv_bytes(cleaned_df),
                            file_name=f"cleaned_{st.session_state.filename.rsplit('.',1)[0]}.csv",
                            mime="text/csv", use_container_width=True)

# ==========================================
# STATION 3 — MERGE FILES
# ==========================================
elif station == "3 · Merge Files":
    st.header("Merge Two Files")
    if not has_file:
        st.info("Upload your first file in the sidebar to get started.")
    else:
        df_left = st.session_state.df
        section_tag("second file")
        second_file = st.file_uploader("Upload the file to merge in", type=["csv", "xlsx"], key="second")

        if second_file is not None:
            try:
                df_right = pd.read_csv(second_file) if second_file.name.endswith(".csv") else pd.read_excel(second_file, engine="openpyxl")
            except Exception as e:
                st.error(f"Couldn't read that file: {e}")
                df_right = None

            if df_right is not None:
                section_tag("settings")
                m1, m2 = st.columns(2)
                key_left = m1.selectbox("Match column — file 1", options=list(df_left.columns))
                key_right = m2.selectbox("Match column — file 2", options=list(df_right.columns))

                merged, log, matched, l_only, r_only = merge_files(df_left, df_right, key_left, key_right)

                st.divider()
                c1, c2, c3 = st.columns(3)
                c1.metric("MATCHED", f"{matched:,}")
                c2.metric("UNMATCHED · FILE 1", f"{l_only:,}")
                c3.metric("UNMATCHED · FILE 2", f"{r_only:,}")
                st.info(log)
                st.divider()

                section_tag("merged preview")
                st.dataframe(merged.head(50), use_container_width=True, height=320)

                st.download_button("📥 Download merged file", to_csv_bytes(merged),
                                    file_name="merged_data.csv", mime="text/csv", use_container_width=True)
        else:
            st.caption("Waiting on a second file to merge against.")

# ==========================================
# STATION 4 — SUMMARY REPORT
# ==========================================
elif station == "4 · Summary Report":
    st.header("Summary Report")
    if not has_file:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df
        section_tag("settings")
        s1, s2 = st.columns(2)
        with s1:
            group_col = st.selectbox("Group by:", options=list(df.columns))
        with s2:
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            value_col = st.selectbox("Summarize:", options=["(count only)"] + numeric_cols)

        summary = build_summary(df, group_col, value_col)

        st.divider()
        c1, c2 = st.columns([1, 3])
        c1.metric("GROUPS", f"{summary.shape[0]:,}")
        c2.info(f"Grouped by '{group_col}'" + (f", summarizing '{value_col}'." if value_col != "(count only)" else "."))
        st.divider()

        section_tag("report")
        st.dataframe(summary, use_container_width=True, height=320)

        if value_col != "(count only)":
            st.bar_chart(summary.set_index(group_col)["total"])

        st.download_button("📥 Download summary", to_csv_bytes(summary),
                            file_name="summary_report.csv", mime="text/csv", use_container_width=True)
