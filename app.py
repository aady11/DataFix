import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# TESTED LOGIC FROM COLAB (The Engine)
# ==========================================

def remove_duplicates(df, subset_cols=None):
    n_duplicates = df.duplicated(subset=subset_cols).sum()
    if n_duplicates == 0:
        return df.copy(), "No duplicates found.", 0
    cleaned_df = df.drop_duplicates(subset=subset_cols, keep="first")
    col_info = "all columns" if subset_cols is None else f"columns: {subset_cols}"
    log = f"{n_duplicates} duplicate row(s) removed (checked {col_info})."
    return cleaned_df.reset_index(drop=True), log, n_duplicates

def clean_text(df, columns):
    cleaned_df = df.copy()
    total_changes = 0
    for col in columns:
        original_col = cleaned_df[col].astype(str)
        cleaned_col = original_col.str.strip()
        cleaned_col = cleaned_col.str.replace(r'\s+', ' ', regex=True)
        cleaned_col = cleaned_col.str.title()
        changes_in_col = (original_col != cleaned_col).sum()
        total_changes += changes_in_col
        cleaned_df[col] = cleaned_col
    if total_changes == 0:
        log = "Text cleaning: No changes needed."
    else:
        log = f"Text cleaned: {total_changes} cell(s) updated across {len(columns)} column(s)."
    return cleaned_df, log

def clean_dates(df, columns, output_format='%Y-%m-%d', dayfirst=False):
    cleaned_df = df.copy()
    total_changes = 0
    for col in columns:
        original_col = cleaned_df[col].astype(str).str.strip()
        parsed = pd.to_datetime(cleaned_df[col], errors='coerce', format='mixed', dayfirst=dayfirst)
        formatted = parsed.dt.strftime(output_format)
        cleaned_col = original_col.copy()
        valid_mask = parsed.notna()
        cleaned_col[valid_mask] = formatted[valid_mask]
        changes_in_col = (original_col != cleaned_col).sum()
        total_changes += changes_in_col
        cleaned_df[col] = cleaned_col
    if total_changes == 0:
        log = "Date cleaning: No changes needed."
    else:
        log = f"Date cleaned: {total_changes} cell(s) updated across {len(columns)} column(s)."
    return cleaned_df, log

def merge_files(df_left, df_right, left_on, right_on, how="outer"):
    merged_df = pd.merge(df_left, df_right, left_on=left_on, right_on=right_on, how=how, indicator=True)
    status_map = {"both": "Matched", "left_only": "Left Only", "right_only": "Right Only"}
    merged_df["match_status"] = merged_df["_merge"].map(status_map).astype(str)
    merged_df.drop(columns=["_merge"], inplace=True)
    counts = merged_df["match_status"].value_counts().to_dict()
    matched_count = counts.get("Matched", 0)
    left_only_count = counts.get("Left Only", 0)
    right_only_count = counts.get("Right Only", 0)
    log = (f"Merge complete ({how.upper()} join): {len(merged_df)} total rows | "
           f"{matched_count} matched | {left_only_count} left only | {right_only_count} right only")
    return merged_df, log

def generate_summary_report(df, group_col, numeric_cols=None):
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include='number').columns.drop(group_col, errors='ignore').tolist()
    if not numeric_cols:
        return df.copy(), "No numeric columns found to summarize."
    grouped = df.groupby(group_col)[numeric_cols].agg(['count', 'sum', 'mean'])
    grouped.columns = [f"{col}_{stat}" for col, stat in grouped.columns]
    grouped.reset_index(inplace=True)
    totals = {col: "" for col in grouped.columns}
    totals[group_col] = "TOTAL"
    for col in grouped.columns:
        if col.endswith("_count") or col.endswith("_sum"):
            totals[col] = grouped[col].sum()
        elif col.endswith("_mean"):
            totals[col] = grouped[col].sum() / max(len(grouped), 1)
    summary_df = pd.concat([grouped, pd.DataFrame([totals])], ignore_index=True)
    log = f"Summary report generated: {len(grouped)} group(s) by '{group_col}', {len(numeric_cols)} numeric column(s) summarized."
    return summary_df, log

# ==========================================
# PREMIUM WORKBENCH CSS
# ==========================================
def load_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap');
    
    .stApp { background-color: #FAF9F6; }
    .block-container { padding-top: 3rem; padding-bottom: 2rem; max-width: 1200px; }

    /* --- Sidebar --- */
    [data-testid="stSidebar"] {
        background-color: #F0EDE8 !important;
        border-right: 1px solid #E0DCD5 !important;
    }
    [data-testid="stSidebar"] * { font-family: 'Inter', sans-serif !important; }

    /* --- Station Radio Buttons --- */
    .stRadio > div { gap: 0.5rem; }
    .stRadio label {
        font-family: 'Inter', sans-serif !important;
        border: 1px solid #E0DCD5;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.2s ease;
        background-color: #FFFFFF;
        color: #5A5A5A !important;
        font-weight: 500 !important;
    }
    .stRadio label:hover {
        border-color: #7A9E7E;
        color: #2D2D2D !important;
    }
    .stRadio div[data-baseweb="radio-group"] div[aria-checked="true"] label {
        background-color: #7A9E7E !important;
        border-color: #7A9E7E !important;
        color: #FFFFFF !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(122, 158, 126, 0.2);
    }

    /* --- Workbench Cards --- */
    .workbench-card {
        background-color: #FFFFFF;
        border: 1px solid #E0DCD5;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.04), 0 2px 4px -1px rgba(0, 0, 0, 0.02);
        margin-bottom: 1rem;
    }

    /* --- Live Row Counter Typography --- */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2D2D2D !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        font-size: 0.8rem !important;
        font-weight: 600 !important;
        color: #7A9E7E !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricDeltaNegative"] {
        color: #C45B28 !important; /* Clay/Rust */
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* --- Data Tables --- */
    .stDataFrame {
        border: 1px solid #E0DCD5;
        border-radius: 8px;
    }
    .stDataFrame table {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.85rem !important;
    }

    /* --- Buttons --- */
    .stButton > button, .stDownloadButton > button {
        background-color: #7A9E7E !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        font-family: 'Inter', sans-serif !important;
        transition: all 0.2s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        background-color: #6B8E6F !important;
        box-shadow: 0 4px 6px rgba(122, 158, 126, 0.3) !important;
    }
    
    /* --- Custom Header --- */
    .station-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.5rem;
        font-weight: 700;
        color: #2D2D2D;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .station-header span {
        color: #7A9E7E;
        font-size: 1.8rem;
    }
    
    /* --- Arrow for Before/After --- */
    .arrow-column {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: #7A9E7E;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# APP CONFIG & LAYOUT
# ==========================================

st.set_page_config(page_title="DataFix", layout="wide")
load_css()

# --- Sidebar ---
st.sidebar.title("🧹 DataFix")
st.sidebar.caption("A workbench for tidying messy data.")

station = st.sidebar.radio(
    "Choose a station:",
    ["1. Dedupe", "2. Clean Text & Dates", "3. Merge Files", "4. Summary Report"],
    label_visibility="collapsed"
)

# --- File Upload (Global) ---
uploaded_file = st.sidebar.file_uploader(
    "Upload a spreadsheet",
    type=["csv", "xlsx"],
    help="CSV or Excel files, up to 200MB"
)

if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    st.session_state.df = df
    st.session_state.filename = uploaded_file.name

# ==========================================
# STATION 1: DEDUPE
# ==========================================

if station == "1. Dedupe":
    st.markdown('<div class="station-header"><span>🔍</span> Station 1: Remove Duplicates</div>', unsafe_allow_html=True)
    
    if "df" not in st.session_state:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df

        with st.container():
            all_columns = list(df.columns)
            selected_cols = st.multiselect(
                "Select columns to check for duplicates (leave empty to check all):",
                options=all_columns,
                default=[]
            )
            subset_to_check = selected_cols if len(selected_cols) > 0 else None

            cleaned_df, log, n_duplicates = remove_duplicates(df, subset_cols=subset_to_check)

            # --- SIGNATURE DETAIL: LIVE ROW COUNTER ---
            st.markdown("<div class='workbench-card'>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([2, 0.5, 2])
            with col1:
                st.metric("BEFORE", f"{df.shape[0]:,} rows")
            with col2:
                st.markdown('<div class="arrow-column">➔</div>', unsafe_allow_html=True)
            with col3:
                st.metric("AFTER", f"{cleaned_df.shape[0]:,} rows", delta=f"-{n_duplicates:,} removed", delta_color="inverse")
            st.markdown("</div>", unsafe_allow_html=True)

            if "No duplicates" in log:
                st.success(log)
            else:
                st.warning(log)

        # Before / After Data Preview
        col_before, col_after = st.columns(2)

        with col_before:
            st.subheader("Raw Data Preview")
            st.dataframe(df.head(50), use_container_width=True, height=300)

        with col_after:
            st.subheader("Cleaned Data Preview")
            st.dataframe(cleaned_df.head(50), use_container_width=True, height=300)

        # Download Button
        csv_buffer = BytesIO()
        cleaned_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue()

        st.download_button(
            label="📥 Download cleaned file",
            data=csv_bytes,
            file_name=f"deduped_{st.session_state.filename.replace('.xlsx', '.csv')}",
            mime="text/csv",
            use_container_width=True
        )

# ==========================================
# STATION 2: CLEAN TEXT & DATES
# ==========================================

elif station == "2. Clean Text & Dates":
    st.markdown('<div class="station-header"><span>✨</span> Station 2: Clean Text & Dates</div>', unsafe_allow_html=True)
    
    if "df" not in st.session_state:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df
        
        # --- Text Cleaning Section ---
        st.markdown("<div class='workbench-card'>", unsafe_allow_html=True)
        st.subheader("Text Cleaning")
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not text_cols:
            st.warning("No text columns found in this dataset.")
        else:
            cols_to_clean = st.multiselect("Select text columns to clean:", text_cols, default=text_cols)
            
            if st.button("Clean Text (Trim, Fix Spaces, Title Case)", use_container_width=True):
                cleaned_text_df, text_log = clean_text(df, cols_to_clean)
                st.session_state.df = cleaned_text_df
                st.success(text_log)
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # --- Date Cleaning Section ---
        st.markdown("<div class='workbench-card'>", unsafe_allow_html=True)
        st.subheader("Date Cleaning")
        
        # Let user select columns that might be dates
        all_cols = list(df.columns)
        date_cols = st.multiselect("Select columns to parse as dates:", all_cols)
        dayfirst = st.checkbox("Day-first format (e.g., 31/12/2024 instead of 12/31/2024)")
        
        if st.button("Clean Dates (Standardize to YYYY-MM-DD)", use_container_width=True):
            if date_cols:
                cleaned_dates_df, date_log = clean_dates(df, date_cols, dayfirst=dayfirst)
                st.session_state.df = cleaned_dates_df
                st.success(date_log)
                st.rerun()
            else:
                st.warning("Please select at least one column to clean.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STATION 3: MERGE FILES
# ==========================================

elif station == "3. Merge Files":
    st.markdown('<div class="station-header"><span>🔗</span> Station 3: Merge Two Files</div>', unsafe_allow_html=True)
    
    if "df" not in st.session_state:
        st.info("Upload your primary file in the sidebar first.")
    else:
        df_left = st.session_state.df
        
        st.markdown("<div class='workbench-card'>", unsafe_allow_html=True)
        st.subheader("Primary File (Left)")
        st.write(f"**{st.session_state.filename}** — {df_left.shape[0]} rows × {df_left.shape[1]} columns")
        st.markdown("</div>", unsafe_allow_html=True)

        # Upload second file
        st.markdown("<div class='workbench-card'>", unsafe_allow_html=True)
        st.subheader("Secondary File (Right)")
        uploaded_merge_file = st.file_uploader("Upload file to merge", type=["csv", "xlsx"], key="merge_file")
        
        if uploaded_merge_file is not None:
            if uploaded_merge_file.name.endswith(".csv"):
                df_right = pd.read_csv(uploaded_merge_file)
            else:
                df_right = pd.read_excel(uploaded_merge_file, engine="openpyxl")
            
            st.write(f"**{uploaded_merge_file.name}** — {df_right.shape[0]} rows × {df_right.shape[1]} columns")
            
            # Merge options
            st.markdown("---")
            st.subheader("Merge Configuration")
            
            left_cols = list(df_left.columns)
            right_cols = list(df_right.columns)
            
            col1, col2 = st.columns(2)
            with col1:
                left_on = st.selectbox("Left Key Column:", left_cols)
            with col2:
                right_on = st.selectbox("Right Key Column:", right_cols)
                
            how = st.selectbox("Merge Type:", ["outer", "inner", "left", "right"])
            
            if st.button("🔗 Merge Files", use_container_width=True):
                merged_df, merge_log = merge_files(df_left, df_right, left_on, right_on, how=how)
                st.session_state.df = merged_df
                st.success(merge_log)
                
                # Show unmatched rows stats
                unmatched = merged_df[merged_df["match_status"] != "Matched"]
                if not unmatched.empty:
                    with st.expander("⚠️ View Unmatched Rows"):
                        st.dataframe(unmatched, use_container_width=True)
                
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# STATION 4: SUMMARY REPORT
# ==========================================

elif station == "4. Summary Report":
    st.markdown('<div class="station-header"><span>📊</span> Station 4: Summary Report</div>', unsafe_allow_html=True)
    
    if "df" not in st.session_state:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df
        
        st.markdown("<div class='workbench-card'>", unsafe_allow_html=True)
        all_cols = list(df.columns)
        group_col = st.selectbox("Select column to group by:", all_cols)
        
        # Auto-detect numeric columns
        numeric_cols = df.select_dtypes(include='number').columns.drop(group_col, errors='ignore').tolist()
        
        if not numeric_cols:
            st.warning("No numeric columns found to summarize (excluding the group column).")
        else:
            selected_numeric = st.multiselect("Select numeric columns to summarize:", numeric_cols, default=numeric_cols)
            
            if st.button("Generate Summary Report", use_container_width=True):
                summary_df, report_log = generate_summary_report(df, group_col, selected_numeric)
                st.success(report_log)
                st.dataframe(summary_df, use_container_width=True)
                
                # Download
                csv_buffer = BytesIO()
                summary_df.to_csv(csv_buffer, index=False)
                csv_bytes = csv_buffer.getvalue()
                
                st.download_button(
                    label="📥 Download Summary Report",
                    data=csv_bytes,
                    file_name=f"summary_{st.session_state.filename.replace('.xlsx', '.csv')}",
                    mime="text/csv",
                    use_container_width=True
                )
        st.markdown("</div>", unsafe_allow_html=True)
