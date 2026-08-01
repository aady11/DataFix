import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="DataFix - Data Cleaning Workbench",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS STYLING
# ==========================================
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Main container styling */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e1b4b 0%, #312e81 100%);
    }
    
    [data-testid="stSidebar"] .css-1d391kg, 
    [data-testid="stSidebar"] .stMarkdown,
    [data-testid="stSidebar"] label {
        color: #e0e7ff !important;
    }
    
    /* Station cards */
    .station-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .stDownloadButton>button {
        background: linear-gradient(90deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        font-weight: 600;
        width: 100%;
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
        font-weight: 700;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #f8fafc;
        border-radius: 8px;
        padding: 1rem;
        border: 2px dashed #cbd5e1;
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #6366f1;
        color: white;
    }
    
    /* Radio buttons */
    .stRadio > label {
        background: rgba(255, 255, 255, 0.1);
        padding: 0.75rem;
        border-radius: 8px;
        margin: 0.25rem 0;
        transition: all 0.2s ease;
    }
    
    .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.2);
    }
    
    /* Stats container */
    .stats-container {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        border: 1px solid #bae6fd;
    }
    
    /* Preview container */
    .preview-container {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def remove_duplicates(df, subset_cols=None):
    """Remove duplicate rows from dataframe"""
    n_duplicates = df.duplicated(subset=subset_cols).sum()
    if n_duplicates == 0:
        return df.copy(), "No duplicates found.", 0
    cleaned_df = df.drop_duplicates(subset=subset_cols, keep="first")
    col_info = "all columns" if subset_cols is None else f"selected columns"
    log = f"{n_duplicates} duplicate row(s) removed (checked {col_info})."
    return cleaned_df.reset_index(drop=True), log, n_duplicates

def create_metric_card(label, value, delta=None):
    """Create a styled metric card"""
    if delta:
        st.metric(label=label, value=value, delta=delta)
    else:
        st.metric(label=label, value=value)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 1rem 0;'>
            <h1 style='color: white; margin: 0;'>🧹 DataFix</h1>
            <p style='color: #a5b4fc; margin: 0.5rem 0;'>Your Data Cleaning Workbench</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Station selection
    st.markdown("<p style='color: #e0e7ff; font-weight: 600; margin-bottom: 0.5rem;'>Select a Station:</p>", unsafe_allow_html=True)
    
    station = st.radio(
        "station_selector",
        ["🔍 Dedupe", "✨ Clean Text & Dates", "🔗 Merge Files", "📊 Summary Report"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # File uploader
    st.markdown("<p style='color: #e0e7ff; font-weight: 600; margin-bottom: 0.5rem;'>Upload Your Data:</p>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload a spreadsheet",
        type=["csv", "xlsx"],
        help="Supported formats: CSV, Excel (up to 200MB)",
        label_visibility="collapsed"
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file, engine="openpyxl")
            
            st.session_state.df = df
            st.session_state.filename = uploaded_file.name
            
            st.success(f"✅ Loaded successfully!")
            st.markdown(f"""
                <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 6px; margin-top: 0.5rem;'>
                    <p style='color: #e0e7ff; margin: 0; font-size: 0.85rem;'>
                        📄 <strong>{uploaded_file.name}</strong><br>
                        📊 {df.shape[0]:,} rows × {df.shape[1]} columns
                    </p>
                </div>
            """, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
    
    st.markdown("---")
    
    # Help section
    with st.expander("ℹ️ Quick Guide", expanded=False):
        st.markdown("""
            <div style='color: #e0e7ff; font-size: 0.85rem;'>
                <p><strong>🔍 Dedupe:</strong> Remove duplicate rows</p>
                <p><strong>✨ Clean Text:</strong> Fix formatting issues</p>
                <p><strong>🔗 Merge Files:</strong> Combine datasets</p>
                <p><strong>📊 Summary:</strong> View data insights</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# MAIN CONTENT AREA
# ==========================================

# Welcome screen if no file uploaded
if "df" not in st.session_state:
    st.markdown("""
        <div style='text-align: center; padding: 4rem 2rem;'>
            <h1 style='font-size: 3rem; margin-bottom: 1rem;'>🧹 Welcome to DataFix</h1>
            <p style='font-size: 1.2rem; color: #64748b; max-width: 600px; margin: 0 auto;'>
                Your professional data cleaning workbench. Upload a file to get started!
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; height: 200px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🔍</div>
                <h3 style='color: white; margin: 0;'>Dedupe</h3>
                <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;'>Remove duplicates intelligently</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; height: 200px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>✨</div>
                <h3 style='color: white; margin: 0;'>Clean Text</h3>
                <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;'>Fix formatting issues</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; height: 200px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>🔗</div>
                <h3 style='color: white; margin: 0;'>Merge Files</h3>
                <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;'>Combine datasets easily</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); padding: 2rem; border-radius: 12px; text-align: center; color: white; height: 200px;'>
                <div style='font-size: 3rem; margin-bottom: 1rem;'>📊</div>
                <h3 style='color: white; margin: 0;'>Summary</h3>
                <p style='font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.9;'>Get data insights</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# STATION 1: DEDUPE
# ==========================================

elif station == "🔍 Dedupe":
    # Header
    st.markdown("""
        <div class='station-card'>
            <h1 style='color: white; margin: 0;'>🔍 Station 1: Remove Duplicates</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
                Identify and remove duplicate rows from your dataset
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    df = st.session_state.df
    
    # File info metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_metric_card("📄 File Name", st.session_state.filename)
    with col2:
        create_metric_card("📊 Total Rows", f"{df.shape[0]:,}")
    with col3:
        create_metric_card("📋 Columns", df.shape[1])
    with col4:
        memory_usage = df.memory_usage(deep=True).sum() / 1024**2
        create_metric_card("💾 Size", f"{memory_usage:.2f} MB")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Configuration section
    st.markdown("### ⚙️ Configuration")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        all_columns = list(df.columns)
        selected_cols = st.multiselect(
            "Select columns to check for duplicates:",
            options=all_columns,
            default=[],
            help="Leave empty to check all columns for duplicates"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        check_all = st.checkbox("Check all columns", value=len(selected_cols) == 0)
        if check_all:
            selected_cols = []
    
    subset_to_check = selected_cols if len(selected_cols) > 0 else None
    
    # Preview duplicates before removing
    duplicates_mask = df.duplicated(subset=subset_to_check, keep=False)
    n_duplicate_rows = duplicates_mask.sum()
    
    if n_duplicate_rows > 0:
        st.warning(f"⚠️ Found {n_duplicate_rows} rows that are duplicates")
        
        with st.expander("👀 Preview duplicate rows", expanded=False):
            st.dataframe(df[duplicates_mask], use_container_width=True)
    else:
        st.success("✅ No duplicates found!")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Run deduplication
    cleaned_df, log, n_removed = remove_duplicates(df, subset_cols=subset_to_check)
    
    # Results section
    st.markdown("### 📊 Results")
    
    # Change summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        create_metric_card("Original Rows", f"{df.shape[0]:,}")
    with col2:
        create_metric_card("Cleaned Rows", f"{cleaned_df.shape[0]:,}", 
                          delta=f"-{n_removed}" if n_removed > 0 else "No change")
    with col3:
        pct_removed = (n_removed / df.shape[0] * 100) if df.shape[0] > 0 else 0
        create_metric_card("Removed", f"{n_removed:,} ({pct_removed:.1f}%)")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Before/After comparison
    st.markdown("### 🔄 Before & After Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div class='preview-container'>
                <h4 style='color: #ef4444; margin-top: 0;'>📋 Before ({:,} rows)</h4>
            </div>
        """.format(df.shape[0]), unsafe_allow_html=True)
        st.dataframe(df.head(20), use_container_width=True, height=400)
    
    with col2:
        st.markdown("""
            <div class='preview-container'>
                <h4 style='color: #10b981; margin-top: 0;'>✨ After ({:,} rows)</h4>
            </div>
        """.format(cleaned_df.shape[0]), unsafe_allow_html=True)
        st.dataframe(cleaned_df.head(20), use_container_width=True, height=400)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download section
    st.markdown("### 💾 Download Cleaned Data")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Prepare download
        csv_buffer = BytesIO()
        cleaned_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue()
        
        output_filename = f"deduped_{st.session_state.filename.replace('.xlsx', '.csv').replace('.csv', '_cleaned.csv')}"
        
        st.download_button(
            label="📥 Download Cleaned File",
            data=csv_bytes,
            file_name=output_filename,
            mime="text/csv",
            use_container_width=True
        )
        
        st.caption(f"File will be saved as: {output_filename}")

# ==========================================
# STATION 2: CLEAN TEXT & DATES
# ==========================================

elif station == "✨ Clean Text & Dates":
    st.markdown("""
        <div class='station-card'>
            <h1 style='color: white; margin: 0;'>✨ Station 2: Clean Text & Dates</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
                Fix formatting issues, standardize text, and clean date columns
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This station is under construction. Coming soon!")
    
    st.markdown("""
        ### Planned Features:
        - 🔤 **Text Cleaning**: Remove extra spaces, fix capitalization
        - 📅 **Date Standardization**: Convert dates to consistent format
        - 🧹 **Trim Whitespace**: Remove leading/trailing spaces
        - 🔄 **Case Conversion**: Convert to uppercase, lowercase, or title case
        - 🚫 **Remove Special Characters**: Clean unwanted symbols
    """)

# ==========================================
# STATION 3: MERGE FILES
# ==========================================

elif station == "🔗 Merge Files":
    st.markdown("""
        <div class='station-card'>
            <h1 style='color: white; margin: 0;'>🔗 Station 3: Merge Files</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
                Combine multiple datasets using various join strategies
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("🚧 This station is under construction. Coming soon!")
    
    st.markdown("""
        ### Planned Features:
        - 🔗 **Inner Join**: Keep only matching rows
        - 🔄 **Left/Right Join**: Keep all rows from one side
        - 🌐 **Outer Join**: Keep all rows from both files
        - 🎯 **Smart Column Matching**: Auto-detect join keys
        - 📊 **Preview Results**: See merge results before downloading
    """)

# ==========================================
# STATION 4: SUMMARY REPORT
# ==========================================

elif station == "📊 Summary Report":
    st.markdown("""
        <div class='station-card'>
            <h1 style='color: white; margin: 0;'>📊 Station 4: Summary Report</h1>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0;'>
                Get comprehensive insights about your dataset
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    if "df" in st.session_state:
        df = st.session_state.df
        
        # Overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            create_metric_card("Total Rows", f"{df.shape[0]:,}")
        with col2:
            create_metric_card("Total Columns", df.shape[1])
        with col3:
            missing_cells = df.isnull().sum().sum()
            create_metric_card("Missing Values", f"{missing_cells:,}")
        with col4:
            duplicates = df.duplicated().sum()
            create_metric_card("Duplicate Rows", f"{duplicates:,}")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Column information
        st.markdown("### 📋 Column Information")
        
        col_info = pd.DataFrame({
            'Column': df.columns,
            'Type': df.dtypes.astype(str),
            'Non-Null Count': df.count(),
            'Null Count': df.isnull().sum(),
            'Null %': (df.isnull().sum() / len(df) * 100).round(2)
        })
        
        st.dataframe(col_info, use_container_width=True)
        
        # Data preview
        st.markdown("### 👀 Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
    else:
        st.info("📁 Upload a file to see the summary report")

# ==========================================
# FOOTER
# ==========================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #94a3b8; border-top: 1px solid #e2e8f0;'>
        <p style='margin: 0;'>Made with ❤️ using Streamlit | DataFix v1.0</p>
    </div>
""", unsafe_allow_html=True)
