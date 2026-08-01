import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# PREMIUM WORKBENCH CSS
# ==========================================
def load_css():
    st.markdown("""
    <style>
    /* --- Main Workspace Gradient --- */
    .stApp {
        background: linear-gradient(180deg, #FAFAF8 0%, #F0EDE8 100%);
    }
    
    /* Remove default padding for a flush layout */
    .block-container {
        padding-top: 3rem;
        padding-bottom: 2rem;
    }

    /* --- Dark Sidebar Styling --- */
    [data-testid="stSidebar"] {
        background-color: #2C3639 !important;
        border-right: none !important;
    }
    /* Force all sidebar text/labels to be light */
    [data-testid="stSidebar"] * {
        color: #F0F0F0 !important;
    }
    /* Style the file uploader in the dark sidebar */
    [data-testid="stFileUploader"] {
        border: 1px dashed #7A9E7E !important;
        background-color: rgba(122, 158, 126, 0.1) !important;
        border-radius: 0.5rem !important;
    }

    /* --- Station Radio Buttons --- */
    .stRadio > div {
        gap: 0.5rem;
    }
    .stRadio label {
        border: 1px solid transparent;
        border-radius: 0.5rem;
        padding: 0.75rem 1rem;
        transition: all 0.2s ease;
        color: #A0A0A0 !important;
    }
    .stRadio label:hover {
        border-color: #7A9E7E;
        background-color: rgba(122, 158, 126, 0.15);
        color: #FFFFFF !important;
    }
    /* Active station styling */
    .stRadio div[data-baseweb="radio-group"] div[aria-checked="true"] label {
        background-color: rgba(122, 158, 126, 0.25);
        border-color: #7A9E7E;
        color: #FFFFFF !important;
        font-weight: 600;
    }

    /* --- Workbench Cards (Metrics & DataFrames) --- */
    [data-testid="stMetric"], .dataframe-container {
        background-color: #FFFFFF;
        border: 1px solid #E8E4DE;
        border-radius: 0.75rem;
        padding: 1.25rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
    }

    /* --- Live Row Counter Typography --- */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #2C3639 !important;
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        letter-spacing: -0.02em;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #7A9E7E !important;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    [data-testid="stMetricDelta"] {
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricDeltaNegative"] {
        color: #C45B28 !important; /* Clay/rust for attention */
    }

    /* --- Data Table Font --- */
    .stDataFrame {
        font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
        font-size: 0.85rem !important;
    }
    
    /* --- Custom Alert Styles --- */
    .stAlert {
        border-radius: 0.5rem;
        border-left: 4px solid;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .stAlert[data-baseweb="notification"] {
        background-color: #FFFFFF !important;
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
