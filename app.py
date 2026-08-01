import streamlit as st
import pandas as pd
from io import BytesIO

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="DataFix Pro",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# ADVANCED CSS STYLING
# ==========================================
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Main Container */
    .block-container {
        padding: 2rem 3rem !important;
        max-width: 1400px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.98);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(0,0,0,0.05);
        box-shadow: 4px 0 24px rgba(0,0,0,0.08);
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 2rem 1.5rem;
    }
    
    /* Station Selection Styling */
    .stRadio > label {
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stRadio [role="radiogroup"] {
        gap: 0.5rem;
    }
    
    .stRadio [role="radiogroup"] label {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border: 2px solid #dee2e6;
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        font-weight: 600;
        color: #495057;
        position: relative;
        overflow: hidden;
    }
    
    .stRadio [role="radiogroup"] label:hover {
        transform: translateX(4px);
        border-color: #667eea;
        background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%) !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    .stRadio [role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border-color: #667eea;
        color: white !important;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
        transform: translateX(8px);
    }
    
    /* Content Cards */
    .content-card {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 20px;
        padding: 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.12);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.8);
        margin-bottom: 2rem;
        animation: slideUp 0.5s ease-out;
    }
    
    @keyframes slideUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Hero Section */
    .hero-section {
        background: rgba(255, 255, 255, 0.98);
        border-radius: 24px;
        padding: 4rem 3rem;
        text-align: center;
        box-shadow: 0 30px 90px rgba(0,0,0,0.15);
        border: 1px solid rgba(255,255,255,0.9);
        margin-bottom: 3rem;
        position: relative;
        overflow: hidden;
    }
    
    .hero-section::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(102,126,234,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .hero-title {
        font-size: 4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        position: relative;
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #6c757d;
        font-weight: 400;
        position: relative;
    }
    
    /* Feature Cards Grid */
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        height: 220px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102,126,234,0.4);
    }
    
    .feature-card:hover::before {
        opacity: 1;
    }
    
    .feature-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
    }
    
    .feature-title {
        color: white;
        font-size: 1.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .feature-description {
        color: rgba(255,255,255,0.9);
        font-size: 0.95rem;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 800;
        color: #212529;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 1rem;
        font-weight: 600;
    }
    
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 16px;
        border: 2px solid #dee2e6;
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        border-color: #667eea;
        box-shadow: 0 8px 24px rgba(102,126,234,0.15);
        transform: translateY(-4px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2.5rem;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(102,126,234,0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(102,126,234,0.5);
    }
    
    .stButton > button:active {
        transform: translateY(-1px);
    }
    
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        width: 100%;
        font-size: 1.1rem;
        box-shadow: 0 4px 16px rgba(16,185,129,0.3);
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px rgba(16,185,129,0.5);
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 16px rgba(0,0,0,0.08);
        border: 1px solid #dee2e6;
    }
    
    /* Alert Boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        padding: 1.25rem;
        font-weight: 500;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        color: #065f46;
        border-left: 4px solid #10b981;
    }
    
    .stWarning {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        border-left: 4px solid #f59e0b;
    }
    
    .stInfo {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
        color: #1e3a8a;
        border-left: 4px solid #3b82f6;
    }
    
    .stError {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        color: #991b1b;
        border-left: 4px solid #ef4444;
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px;
        padding: 2rem;
        border: 3px dashed #adb5bd;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #667eea;
        background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%);
    }
    
    /* Multiselect */
    .stMultiSelect [data-baseweb="tag"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Headers */
    h1 {
        color: #212529;
        font-weight: 800;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    h2 {
        color: #495057;
        font-weight: 700;
        font-size: 2rem;
        margin-top: 2rem;
    }
    
    h3 {
        color: #6c757d;
        font-weight: 600;
        font-size: 1.5rem;
        margin-top: 1.5rem;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        font-weight: 600;
        padding: 1rem;
        border: 2px solid #dee2e6;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: #667eea;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(255,255,255,0.9);
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    /* Progress Bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    /* Sidebar Logo Area */
    .sidebar-logo {
        text-align: center;
        padding: 1.5rem 0 2rem 0;
        border-bottom: 2px solid #e9ecef;
        margin-bottom: 2rem;
    }
    
    .sidebar-title {
        font-size: 2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .sidebar-subtitle {
        color: #6c757d;
        font-size: 0.85rem;
        margin-top: 0.25rem;
        font-weight: 500;
    }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 2rem 0 1rem 0;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    /* Comparison Container */
    .comparison-container {
        background: rgba(255,255,255,0.5);
        border-radius: 16px;
        padding: 1.5rem;
        border: 2px solid #dee2e6;
    }
    
    .comparison-header {
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 1rem;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #dee2e6;
    }
    
    .before-header {
        color: #dc3545;
    }
    
    .after-header {
        color: #28a745;
    }
    
    /* Stats Badge */
    .stats-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
        font-size: 0.9rem;
        box-shadow: 0 4px 12px rgba(102,126,234,0.3);
    }
    
    /* Checkbox */
    .stCheckbox {
        font-weight: 600;
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

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    # Logo Section
    st.markdown("""
        <div class='sidebar-logo'>
            <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>🎯</div>
            <h1 class='sidebar-title'>DataFix Pro</h1>
            <p class='sidebar-subtitle'>Professional Data Cleaning</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Station Selection
    st.markdown("<h3 style='color: #495057; font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;'>⚡ Select Station</h3>", unsafe_allow_html=True)
    
    station = st.radio(
        "station_selector",
        ["🔍 Dedupe Master", "✨ Text Cleaner", "🔗 File Merger", "📊 Data Insights"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # File Upload Section
    st.markdown("<h3 style='color: #495057; font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;'>📁 Upload Data</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload your file",
        type=["csv", "xlsx"],
        help="Supports CSV and Excel files",
        label_visibility="collapsed"
    )
    
    # Process File
    if uploaded_file is not None:
        try:
            with st.spinner("Processing file..."):
                if uploaded_file.name.endswith(".csv"):
                    df = pd.read_csv(uploaded_file)
                else:
                    df = pd.read_excel(uploaded_file, engine="openpyxl")
                
                st.session_state.df = df
                st.session_state.filename = uploaded_file.name
            
            st.success("✅ File loaded successfully!")
            
            # File Stats
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                            padding: 1.25rem; border-radius: 12px; margin-top: 1rem;
                            border: 2px solid #dee2e6;'>
                    <div style='color: #495057; font-weight: 700; margin-bottom: 0.75rem; font-size: 0.85rem;'>
                        📄 {uploaded_file.name}
                    </div>
                    <div style='display: flex; justify-content: space-between; color: #6c757d; font-size: 0.85rem;'>
                        <div><strong>{df.shape[0]:,}</strong> rows</div>
                        <div><strong>{df.shape[1]}</strong> cols</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Quick Guide
    with st.expander("💡 Quick Guide"):
        st.markdown("""
            <div style='font-size: 0.85rem; line-height: 1.6;'>
                <p><strong>🔍 Dedupe Master:</strong><br/>Remove duplicate rows with precision</p>
                <p><strong>✨ Text Cleaner:</strong><br/>Fix formatting and text issues</p>
                <p><strong>🔗 File Merger:</strong><br/>Combine multiple datasets</p>
                <p><strong>📊 Data Insights:</strong><br/>Comprehensive data analysis</p>
            </div>
        """, unsafe_allow_html=True)

# ==========================================
# MAIN CONTENT
# ==========================================

# Landing Page
if "df" not in st.session_state:
    st.markdown("""
        <div class='hero-section'>
            <h1 class='hero-title'>DataFix Pro</h1>
            <p class='hero-subtitle'>Transform messy data into clean, actionable insights</p>
            <div style='margin-top: 2rem; color: #6c757d; font-size: 1.1rem;'>
                👆 Upload a file in the sidebar to get started
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Feature Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
            <div class='feature-card' style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);'>
                <div class='feature-icon'>🔍</div>
                <h3 class='feature-title'>Dedupe Master</h3>
                <p class='feature-description'>Smart duplicate detection</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class='feature-card' style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);'>
                <div class='feature-icon'>✨</div>
                <h3 class='feature-title'>Text Cleaner</h3>
                <p class='feature-description'>Advanced text processing</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class='feature-card' style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);'>
                <div class='feature-icon'>🔗</div>
                <h3 class='feature-title'>File Merger</h3>
                <p class='feature-description'>Intelligent data merging</p>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
            <div class='feature-card' style='background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);'>
                <div class='feature-icon'>📊</div>
                <h3 class='feature-title'>Data Insights</h3>
                <p class='feature-description'>Powerful analytics</p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    # Info Section
    st.markdown("""
        <div class='content-card'>
            <h2 style='text-align: center; margin-bottom: 2rem;'>Why Choose DataFix Pro?</h2>
            <div style='display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;'>
                <div style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>⚡</div>
                    <h3 style='color: #495057; margin: 0.5rem 0;'>Lightning Fast</h3>
                    <p style='color: #6c757d;'>Process millions of rows in seconds</p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>🎯</div>
                    <h3 style='color: #495057; margin: 0.5rem 0;'>Precision Tools</h3>
                    <p style='color: #6c757d;'>Advanced algorithms for accuracy</p>
                </div>
                <div style='text-align: center;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>🔒</div>
                    <h3 style='color: #495057; margin: 0.5rem 0;'>Secure & Private</h3>
                    <p style='color: #6c757d;'>Your data never leaves your browser</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# ==========================================
# STATION 1: DEDUPE MASTER
# ==========================================

elif station == "🔍 Dedupe Master":
    df = st.session_state.df
    
    # Header Section
    st.markdown("""
        <div class='content-card' style='background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); border: 2px solid rgba(102,126,234,0.3);'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <div style='font-size: 4rem;'>🔍</div>
                <div>
                    <h1 style='margin: 0; color: #212529;'>Dedupe Master</h1>
                    <p style='margin: 0.5rem 0 0 0; color: #6c757d; font-size: 1.1rem;'>
                        Identify and eliminate duplicate rows with precision
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Metrics Dashboard
    st.markdown("<div class='section-header'>📊 Dataset Overview</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📄 File", st.session_state.filename.split('.')[0][:10] + "...")
    with col2:
        st.metric("📊 Total Rows", f"{df.shape[0]:,}")
    with col3:
        st.metric("📋 Columns", df.shape[1])
    with col4:
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("💾 Memory", f"{memory_mb:.1f} MB")
    with col5:
        duplicates = df.duplicated().sum()
        st.metric("🔴 Duplicates", f"{duplicates:,}")
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Configuration Section
    st.markdown("<div class='section-header'>⚙️ Configuration</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        all_columns = list(df.columns)
        selected_cols = st.multiselect(
            "🎯 Select columns to check for duplicates",
            options=all_columns,
            default=[],
            help="Leave empty to check all columns"
        )
    
    with col2:
        st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
        check_all = st.checkbox("✅ Check all columns", value=len(selected_cols) == 0)
        if check_all:
            selected_cols = []
    
    subset_to_check = selected_cols if len(selected_cols) > 0 else None
    
    # Display selected columns info
    if selected_cols:
        st.info(f"🔍 Checking {len(selected_cols)} column(s): {', '.join(selected_cols[:5])}" + 
                (f" and {len(selected_cols)-5} more..." if len(selected_cols) > 5 else ""))
    else:
        st.info(f"🔍 Checking all {len(all_columns)} columns for duplicates")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Duplicate Preview
    duplicates_mask = df.duplicated(subset=subset_to_check, keep=False)
    n_duplicate_rows = duplicates_mask.sum()
    
    if n_duplicate_rows > 0:
        st.markdown("<div class='section-header'>⚠️ Duplicate Detection</div>", unsafe_allow_html=True)
        
        st.markdown(f"""
            <div class='content-card' style='background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%); 
                                              border: 2px solid #f59e0b;'>
                <div style='display: flex; align-items: center; gap: 1rem;'>
                    <div style='font-size: 3rem;'>⚠️</div>
                    <div>
                        <h3 style='margin: 0; color: #92400e;'>Found {n_duplicate_rows:,} duplicate rows</h3>
                        <p style='margin: 0.5rem 0 0 0; color: #b45309;'>
                            These rows will be removed, keeping only the first occurrence
                        </p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        with st.expander("👁️ Preview duplicate rows (first 50)", expanded=False):
            st.dataframe(
                df[duplicates_mask].head(50),
                use_container_width=True,
                height=400
            )
    else:
        st.markdown("<div class='section-header'>✅ Duplicate Detection</div>", unsafe_allow_html=True)
        st.success("🎉 No duplicates found! Your data is already clean.")
    
    # Run Deduplication
    cleaned_df, log, n_removed = remove_duplicates(df, subset_cols=subset_to_check)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Results Section
    st.markdown("<div class='section-header'>📈 Results & Analytics</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Original Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Cleaned Rows", f"{cleaned_df.shape[0]:,}", 
                 delta=f"-{n_removed:,}" if n_removed > 0 else "No change",
                 delta_color="normal")
    with col3:
        pct_removed = (n_removed / df.shape[0] * 100) if df.shape[0] > 0 else 0
        st.metric("Removed", f"{n_removed:,} ({pct_removed:.1f}%)")
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Before/After Comparison
    st.markdown("<div class='section-header'>🔄 Before & After Comparison</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
            <div class='comparison-container'>
                <div class='comparison-header before-header'>
                    ❌ Before Cleaning ({df.shape[0]:,} rows)
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(df.head(20), use_container_width=True, height=500)
    
    with col2:
        st.markdown(f"""
            <div class='comparison-container'>
                <div class='comparison-header after-header'>
                    ✅ After Cleaning ({cleaned_df.shape[0]:,} rows)
                </div>
            </div>
        """, unsafe_allow_html=True)
        st.dataframe(cleaned_df.head(20), use_container_width=True, height=500)
    
    st.markdown("<div style='margin: 3rem 0;'></div>", unsafe_allow_html=True)
    
    # Download Section
    st.markdown("<div class='section-header'>💾 Export Cleaned Data</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Prepare CSV
        csv_buffer = BytesIO()
        cleaned_df.to_csv(csv_buffer, index=False)
        csv_bytes = csv_buffer.getvalue()
        
        base_name = st.session_state.filename.rsplit('.', 1)[0]
        output_filename = f"{base_name}_cleaned.csv"
        
        st.download_button(
            label=f"📥 Download Cleaned Data ({cleaned_df.shape[0]:,} rows)",
            data=csv_bytes,
            file_name=output_filename,
            mime="text/csv",
            use_container_width=True
        )
        
        st.caption(f"💡 File will be saved as: `{output_filename}`")
        
        # Summary
        if n_removed > 0:
            st.success(f"✅ Successfully removed {n_removed:,} duplicate rows ({pct_removed:.2f}%)")
        else:
            st.info("ℹ️ No duplicates were found in your dataset")
    
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# OTHER STATIONS
# ==========================================

elif station == "✨ Text Cleaner":
    st.markdown("""
        <div class='content-card' style='background: linear-gradient(135deg, rgba(240,147,251,0.1) 0%, rgba(245,87,108,0.1) 100%); border: 2px solid rgba(240,147,251,0.3);'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <div style='font-size: 4rem;'>✨</div>
                <div>
                    <h1 style='margin: 0; color: #212529;'>Text Cleaner</h1>
                    <p style='margin: 0.5rem 0 0 0; color: #6c757d; font-size: 1.1rem;'>
                        Advanced text processing and formatting tools
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='content-card' style='margin-top: 2rem;'>
            <div style='text-align: center; padding: 3rem;'>
                <div style='font-size: 5rem; margin-bottom: 2rem;'>🚧</div>
                <h2 style='color: #495057;'>Coming Soon</h2>
                <p style='color: #6c757d; font-size: 1.1rem; max-width: 600px; margin: 1rem auto;'>
                    We're building powerful text cleaning features including trim, case conversion, 
                    special character removal, and date standardization.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif station == "🔗 File Merger":
    st.markdown("""
        <div class='content-card' style='background: linear-gradient(135deg, rgba(79,172,254,0.1) 0%, rgba(0,242,254,0.1) 100%); border: 2px solid rgba(79,172,254,0.3);'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <div style='font-size: 4rem;'>🔗</div>
                <div>
                    <h1 style='margin: 0; color: #212529;'>File Merger</h1>
                    <p style='margin: 0.5rem 0 0 0; color: #6c757d; font-size: 1.1rem;'>
                        Intelligently combine multiple datasets
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='content-card' style='margin-top: 2rem;'>
            <div style='text-align: center; padding: 3rem;'>
                <div style='font-size: 5rem; margin-bottom: 2rem;'>🚧</div>
                <h2 style='color: #495057;'>Coming Soon</h2>
                <p style='color: #6c757d; font-size: 1.1rem; max-width: 600px; margin: 1rem auto;'>
                    Advanced merge functionality with support for inner, outer, left, and right joins 
                    will be available soon.
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)

elif station == "📊 Data Insights":
    df = st.session_state.df
    
    st.markdown("""
        <div class='content-card' style='background: linear-gradient(135deg, rgba(67,233,123,0.1) 0%, rgba(56,249,215,0.1) 100%); border: 2px solid rgba(67,233,123,0.3);'>
            <div style='display: flex; align-items: center; gap: 1rem;'>
                <div style='font-size: 4rem;'>📊</div>
                <div>
                    <h1 style='margin: 0; color: #212529;'>Data Insights</h1>
                    <p style='margin: 0.5rem 0 0 0; color: #6c757d; font-size: 1.1rem;'>
                        Comprehensive analysis of your dataset
                    </p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div class='section-header'>📊 Key Metrics</div>", unsafe_allow_html=True)
    
    # Top Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("📄 Total Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("📋 Total Columns", df.shape[1])
    with col3:
        missing = df.isnull().sum().sum()
        st.metric("❓ Missing Values", f"{missing:,}")
    with col4:
        duplicates = df.duplicated().sum()
        st.metric("🔴 Duplicates", f"{duplicates:,}")
    with col5:
        memory_mb = df.memory_usage(deep=True).sum() / 1024**2
        st.metric("💾 Memory Usage", f"{memory_mb:.1f} MB")
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Column Analysis
    st.markdown("<div class='section-header'>📋 Column Analysis</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='content-card'>", unsafe_allow_html=True)
    
    col_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null': df.count().values,
        'Null Count': df.isnull().sum().values,
        'Null %': (df.isnull().sum() / len(df) * 100).round(2).values,
        'Unique Values': [df[col].nunique() for col in df.columns]
    })
    
    st.dataframe(col_info, use_container_width=True, height=400)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    # Data Preview
    st.markdown("<div class='section-header'>👁️ Data Preview</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs(["📄 First 20 Rows", "📄 Last 20 Rows", "🎲 Random Sample"])
    
    with tab1:
        st.dataframe(df.head(20), use_container_width=True, height=500)
    
    with tab2:
        st.dataframe(df.tail(20), use_container_width=True, height=500)
    
    with tab3:
        sample_size = min(20, len(df))
        st.dataframe(df.sample(n=sample_size), use_container_width=True, height=500)
        
