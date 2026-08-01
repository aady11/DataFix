import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# TESTED LOGIC FROM COLAB
# ==========================================

def remove_duplicates(df, subset_cols=None):
    n_duplicates = df.duplicated(subset=subset_cols).sum()
    if n_duplicates == 0:
        return df.copy(), "No duplicates found."
    cleaned_df = df.drop_duplicates(subset=subset_cols, keep="first")
    col_info = "all columns" if subset_cols is None else f"columns: {subset_cols}"
    log = f"{n_duplicates} duplicate row(s) removed (checked {col_info})."
    return cleaned_df.reset_index(drop=True), log

# ==========================================
# APP CONFIG & LAYOUT
# ==========================================

st.set_page_config(page_title="DataFix", layout="wide")

# --- Sidebar ---
st.sidebar.title("🧹 DataFix")
st.sidebar.caption("A workbench for tidying messy data.")

station = st.sidebar.radio(
    "Choose a station:",
    ["1. Dedupe", "2. Clean Text & Dates", "3. Merge Files", "4. Summary Report"],
    label_visibility="collapsed"
)

# --- File Upload (Global) ---
# We put the uploader in the sidebar so it's always accessible
uploaded_file = st.sidebar.file_uploader(
    "Upload a spreadsheet",
    type=["csv", "xlsx"],
    help="CSV or Excel files, up to 200MB"
)

# Read file and store in session_state
if uploaded_file is not None:
    # Read the file
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    # Save to session state so it persists across station changes
    st.session_state.df = df
    st.session_state.filename = uploaded_file.name

# ==========================================
# STATION 1: DEDUPE
# ==========================================

if station == "1. Dedupe":
    st.header("Station 1: Remove Duplicates")
    
    if "df" not in st.session_state:
        st.info("Upload a file in the sidebar to get started.")
    else:
        df = st.session_state.df
        st.success(f"Loaded **{st.session_state.filename}** — {df.shape[0]} rows × {df.shape[1]} columns")

        # Column Picker
        all_columns = list(df.columns)
        selected_cols = st.multiselect(
            "Select columns to check for duplicates (leave empty to check all):",
            options=all_columns,
            default=[]
        )

        subset_to_check = selected_cols if len(selected_cols) > 0 else None

        # Run Dedupe
        cleaned_df, log = remove_duplicates(df, subset_cols=subset_to_check)

        # Change Log
        if "No duplicates" in log:
            st.info(log)
        else:
            st.warning(log)

        # Before / After Preview
        col1, col2 = st.columns(2)

        with col1:
            st.subheader(f"Before ({df.shape[0]} rows)")
            st.dataframe(df.head(20), use_container_width=True)

        with col2:
            st.subheader(f"After ({cleaned_df.shape[0]} rows)")
            st.dataframe(cleaned_df.head(20), use_container_width=True)

        # Download Button
        csv_buffer = BytesIO()
        cleaned_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue()

        st.download_button(
            label="📥 Download cleaned file",
            data=csv_bytes,
            file_name=f"deduped_{st.session_state.filename.replace('.xlsx', '.csv')}",
            mime="text/csv"
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
