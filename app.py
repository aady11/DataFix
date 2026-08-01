import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# CUSTOM CSS — THE WORKBENCH AESTHETIC
# ==========================================
def load_css():
    st.markdown("""
    <style>
    /* Remove default Streamlit top padding and header */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Force monospace font on data tables */
    .stDataFrame {
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace !important;
        font-size: 0.85rem !important;
    }
    
    /* Clean up the sidebar */
    [data-testid="stSidebar"] {
        border-right: 1px solid #E0DCD5;
    }
    
    /* Style the radio buttons to look like station buttons */
    .stRadio > div {
        gap: 0.5rem;
    }
    .stRadio label {
        border: 1px solid #E0DCD5;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
    }
    .stRadio label:hover {
        border-color: #7A9E7E; /* Sage green */
        background-color: #F4F8F4;
    }
    
    /* Signature metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        font-weight: 700 !important;
        color: #2D2D2D !important;
        font-family: 'JetBrains Mono', monospace !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 1rem !important;
    }
    [data-testid="stMetricDeltaNegative"] {
        color: #C45B28 !important; /* Clay/rust for attention */
    }
    
    /* Custom alert styles */
    .stAlert {
        border-radius: 0.5rem;
        border-left: 4px solid;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# TESTED LOGIC FROM COLAB
# ==========================================

def remove_duplicates(df, subset_cols=None):
    n_duplicates = df.duplicated(subset=subset_cols).sum()
    if n_duplicates == 0:
        return df.copy(), "No duplicates found.", 0
    cleaned_df = df.drop_duplicates(subset=subset_cols, keep="first")
    col_info = "all columns" if subset_cols is None else f"columns: {subset_cols}"
    log = f"{n_duplicates} duplicate row(s) removed (checked {col_info})."
    return cleaned_df.reset_index(drop=True), log, n_duplicates

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

# Read file and store in session_state
if uploaded_file is not None:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    st.session_state.df = df
    st.session_state.filename = uploaded_file.name

# ==========================================
# STATION 1: DEDUPE (With Live Counter)
# ==========================================

if station == "1. Dedupe":
    st.header("Station 1: Remove Duplicates")
    
    if "df" not in st.session_state:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df

        # Column Picker
        all_columns = list(df.columns)
        selected_cols = st.multiselect(
            "Select columns to check for duplicates (leave empty to check all):",
            options=all_columns,
            default=[]
        )

        subset_to_check = selected_cols if len(selected_cols) > 0 else None

        # Run Dedupe
        cleaned_df, log, n_duplicates = remove_duplicates(df, subset_cols=subset_to_check)

        # --- LIVE ROW COUNTER (Signature Detail) ---
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("BEFORE", f"{df.shape[0]:,} rows")
        with col2:
            st.metric("AFTER", f"{cleaned_df.shape[0]:,} rows", delta=f"-{n_duplicates:,} removed", delta_color="inverse")
        with col3:
            # Change log inside the counter area
            if "No duplicates" in log:
                st.success(log)
            else:
                st.warning(log)
        st.divider()

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
# PLACEHOLDERS FOR OTHER STATIONS
# ==========================================

elif station == "2. Clean Text & Dates":
    st.header("Station 2: Clean Text & Dates")
    st.info("Station logic coming soon.")

elif station == "3. Merge Files":
    st.header("Station 3: Merge Two Files")
    st.info("Station logic coming soon.")

elif station == "4. Summary Report":
    st.header("Station 4: Summary Report")
    st.info("Station logic coming soon.")
