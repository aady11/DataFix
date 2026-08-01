import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
import re

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
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
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
        top: 0; left: 0; right: 0; bottom: 0;
        background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 100%);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) scale(1.02);
        box-shadow: 0 20px 40px rgba(102,126,234,0.4);
    }
    
    .feature-card:hover::before { opacity: 1; }
    
    .feature-icon { font-size: 4rem; margin-bottom: 1rem; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2)); }
    .feature-title { color: white; font-size: 1.5rem; font-weight: 700; margin: 0.5rem 0; }
    .feature-description { color: rgba(255,255,255,0.9); font-size: 0.95rem; }
    
    /* Metrics */
    [data-testid="stMetricValue"] { font-size: 2.5rem; font-weight: 800; color: #212529; }
    [data-testid="stMetricLabel"] { font-size: 0.95rem; font-weight: 600; color: #6c757d; text-transform: uppercase; letter-spacing: 0.5px; }
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem; border-radius: 16px; border: 2px solid #dee2e6;
        transition: all 0.3s ease;
    }
    div[data-testid="metric-container"]:hover {
        border-color: #667eea; box-shadow: 0 8px 24px rgba(102,126,234,0.15); transform: translateY(-4px);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border: none; border-radius: 12px;
        padding: 0.75rem 2.5rem; font-weight: 700; font-size: 1rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 16px rgba(102,126,234,0.3);
        text-transform: uppercase; letter-spacing: 0.5px;
    }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(102,126,234,0.5); }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 16px; padding: 2rem; border: 3px dashed #adb5bd;
        transition: all 0.3s ease;
    }
    [data-testid="stFileUploader"]:hover { border-color: #667eea; background: linear-gradient(135deg, #fff 0%, #f8f9ff 100%); }
    
    /* Sidebar Logo Area */
    .sidebar-logo { text-align: center; padding: 1.5rem 0 2rem 0; border-bottom: 2px solid #e9ecef; margin-bottom: 2rem; }
    .sidebar-title { font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; }
    .sidebar-subtitle { color: #6c757d; font-size: 0.85rem; margin-top: 0.25rem; font-weight: 500; }
    
    /* Section Headers */
    .section-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 1.8rem; font-weight: 800; margin: 2rem 0 1rem 0;
        display: flex; align-items: center; gap: 0.75rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 1rem; background: transparent; }
    .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.7); border-radius: 12px; padding: 0.75rem 1.5rem; font-weight: 600; border: 2px solid transparent; }
    .stTabs [aria-selected="true"] { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; }
    
    /* DataFrames */
    [data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border: 1px solid #dee2e6; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def load_file(file):
    """Load CSV or Excel file"""
    try:
        if file.name.endswith(".csv"):
            return pd.read_csv(file)
        else:
            return pd.read_excel(file, engine="openpyxl")
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

def remove_duplicates(df, subset_cols=None, case_insensitive=False, ignore_whitespace=False):
    """Advanced duplicate removal"""
    working_df = df.copy()
    
    # Pre-processing for comparison
    if case_insensitive or ignore_whitespace:
        # Create a temporary copy for comparison logic
        compare_df = working_df.copy()
        if subset_cols:
            cols_to_process = subset_cols
        else:
            cols_to_process = working_df.select_dtypes(include=['object']).columns.tolist()
            
        for col in cols_to_process:
            if col in compare_df.columns:
                if ignore_whitespace:
                    compare_df[col] = compare_df[col].astype(str).str.strip()
                if case_insensitive:
                    compare_df[col] = compare_df[col].astype(str).str.lower()
        
        # Find duplicates based on processed data
        mask = compare_df.duplicated(subset=subset_cols, keep="first")
        cleaned_df = working_df[~mask].reset_index(drop=True)
        n_removed = len(working_df) - len(cleaned_df)
        return cleaned_df, n_removed
    else:
        # Standard removal
        n_duplicates = working_df.duplicated(subset=subset_cols).sum()
        if n_duplicates == 0:
            return working_df, 0
        cleaned_df = working_df.drop_duplicates(subset=subset_cols, keep="first").reset_index(drop=True)
        return cleaned_df, n_duplicates

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
        <div class='sidebar-logo'>
            <div style='font-size: 3.5rem; margin-bottom: 0.5rem;'>🎯</div>
            <h1 class='sidebar-title'>DataFix Pro</h1>
            <p class='sidebar-subtitle'>Professional Data Cleaning</p>
        </div>
    """, unsafe_allow_html=True)
    
    station = st.radio(
        "station_selector",
        ["🔍 Dedupe Master", "✨ Text Cleaner", "🔗 File Merger", "📊 Data Insights"],
        label_visibility="collapsed"
    )
    
    st.markdown("<div style='margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: #495057; font-size: 1rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;'>📁 Upload Data</h3>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Upload your file",
        type=["csv", "xlsx"],
        help="Supports CSV and Excel files",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        try:
            with st.spinner("Processing file..."):
                df = load_file(uploaded_file)
                if df is not None:
                    st.session_state.df = df
                    st.session_state.filename = uploaded_file.name
                    st.session_state.original_df = df.copy() # Keep original for reset
                    st.success("✅ File loaded successfully!")
                    
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
    
    if st.button("🔄 Reset All Data", use_container_width=True):
        if "df" in st.session_state:
            del st.session_state.df
            st.rerun()

# ==========================================
# MAIN CONTENT LOGIC
# ==========================================

# Initialize session state if not exists
if "df" not in st.session_state:
    # Landing Page
    st.markdown("""
        <div class='hero-section'>
            <h1 class='hero-title'>DataFix Pro</h1>
            <p class='hero-subtitle'>Transform messy data into clean, actionable insights</p>
            <div style='margin-top: 2rem; color: #6c757d; font-size: 1.1rem;'>
                👆 Upload a file in the sidebar to get started
            </div>
        </div>
    """, unsafe_allow_html=True)
    
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

else:
    df = st.session_state.df
    
    # ==========================================
    # STATION 1: DEDUPE MASTER
    # ==========================================
    if station == "🔍 Dedupe Master":
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
        
        # Metrics
        col1, col2, col3 = st.columns(3)
        with col1: st.metric("Total Rows", f"{df.shape[0]:,}")
        with col2: st.metric("Columns", df.shape[1])
        with col3: st.metric("Current Duplicates", f"{df.duplicated().sum():,}")
        
        st.markdown("<div class='section-header'>⚙️ Configuration</div>", unsafe_allow_html=True)
        
        with st.expander("Advanced Options", expanded=False):
            case_insensitive = st.checkbox("Case Insensitive Matching (e.g., 'Apple' == 'apple')")
            ignore_whitespace = st.checkbox("Ignore Leading/Trailing Whitespace")
        
        all_columns = list(df.columns)
        selected_cols = st.multiselect(
            "🎯 Select columns to check (Leave empty for all)",
            options=all_columns,
            default=[]
        )
        
        subset_to_check = selected_cols if selected_cols else None
        
        if st.button("🚀 Run Deduplication", type="primary"):
            with st.spinner("Cleaning data..."):
                cleaned_df, n_removed = remove_duplicates(
                    df, 
                    subset_cols=subset_to_check, 
                    case_insensitive=case_insensitive, 
                    ignore_whitespace=ignore_whitespace
                )
                
                st.session_state.df = cleaned_df
                
                st.success(f"✅ Removed {n_removed:,} duplicate rows!")
                st.rerun()
        
        # Download Section
        if n_removed > 0 if 'n_removed' in locals() else False:
             st.markdown("<div class='section-header'>💾 Export</div>", unsafe_allow_html=True)
             csv = cleaned_df.to_csv(index=False).encode('utf-8')
             st.download_button("📥 Download Cleaned CSV", csv, "cleaned_data.csv", "text/csv", use_container_width=True)

    # ==========================================
    # STATION 2: TEXT CLEANER
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
        
        text_cols = df.select_dtypes(include=['object']).columns.tolist()
        
        if not text_cols:
            st.warning("No text columns found in this dataset.")
        else:
            cols_to_clean = st.multiselect("Select columns to clean", text_cols, default=text_cols)
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Transformations**")
                do_trim = st.checkbox("Trim Whitespace", value=True)
                do_lower = st.checkbox("Convert to Lowercase")
                do_upper = st.checkbox("Convert to Uppercase")
                do_title = st.checkbox("Convert to Title Case")
                remove_special = st.checkbox("Remove Special Characters (Keep A-Z, 0-9)")
            
            with col2:
                st.markdown("**Missing Values**")
                fill_method = st.selectbox("How to handle empty cells?", ["Leave Empty", "Fill with 'N/A'", "Forward Fill", "Backward Fill"])
            
            if st.button("✨ Apply Text Cleaning", type="primary"):
                with st.spinner("Processing text..."):
                    temp_df = df.copy()
                    
                    for col in cols_to_clean:
                        if col in temp_df.columns:
                            # Ensure string type
                            temp_df[col] = temp_df[col].astype(str)
                            
                            if do_trim:
                                temp_df[col] = temp_df[col].str.strip()
                            if do_lower:
                                temp_df[col] = temp_df[col].str.lower()
                            if do_upper:
                                temp_df[col] = temp_df[col].str.upper()
                            if do_title:
                                temp_df[col] = temp_df[col].str.title()
                            if remove_special:
                                temp_df[col] = temp_df[col].apply(lambda x: re.sub(r'[^A-Za-z0-9\s]', '', str(x)))
                            
                            # Handle NaN/Empty specifically
                            if fill_method == "Fill with 'N/A'":
                                temp_df[col] = temp_df[col].replace('nan', 'N/A').replace('', 'N/A')
                            elif fill_method == "Forward Fill":
                                temp_df[col] = temp_df[col].replace('nan', np.nan).ffill()
                            elif fill_method == "Backward Fill":
                                temp_df[col] = temp_df[col].replace('nan', np.nan).bfill()
                    
                    st.session_state.df = temp_df
                    st.success("✅ Text cleaning applied successfully!")
                    st.rerun()

    # ==========================================
    # STATION 3: FILE MERGER
    # ==========================================
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
        
        st.info(f"📂 Current Base File: **{st.session_state.filename}** ({df.shape[0]:,} rows)")
        
        uploaded_merge_file = st.file_uploader("Upload file to merge", type=["csv", "xlsx"], key="merge_file")
        
        if uploaded_merge_file:
            merge_df = load_file(uploaded_merge_file)
            if merge_df is not None:
                st.success(f"✅ Loaded: {uploaded_merge_file.name} ({merge_df.shape[0]:,} rows)")
                
                merge_type = st.radio("Merge Strategy", ["Append (Stack Rows)", "Join (Merge Columns)"])
                
                if merge_type == "Append (Stack Rows)":
                    # Check columns match
                    if list(df.columns) == list(merge_df.columns):
                        if st.button("🔗 Append Data"):
                            combined_df = pd.concat([df, merge_df], ignore_index=True)
                            st.session_state.df = combined_df
                            st.success(f"Merged! New total rows: {combined_df.shape[0]:,}")
                            st.rerun()
                    else:
                        st.error("Columns do not match exactly. Cannot append.")
                        st.write("Base Columns:", list(df.columns))
                        st.write("New Columns:", list(merge_df.columns))
                
                elif merge_type == "Join (Merge Columns)":
                    common_cols = list(set(df.columns) & set(merge_df.columns))
                    if common_cols:
                        key_col = st.selectbox("Select Key Column to Join On", common_cols)
                        join_type = st.selectbox("Join Type", ["inner", "left", "right", "outer"])
                        
                        if st.button("🔗 Perform Join"):
                            try:
                                merged_df = pd.merge(df, merge_df, on=key_col, how=join_type, suffixes=('_base', '_new'))
                                st.session_state.df = merged_df
                                st.success(f"Join successful! New shape: {merged_df.shape}")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Merge error: {e}")
                    else:
                        st.error("No common columns found to join on.")

    # ==========================================
    # STATION 4: DATA INSIGHTS
    # ==========================================
    elif station == "📊 Data Insights":
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
        
        # Top Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1: st.metric("Rows", f"{df.shape[0]:,}")
        with col2: st.metric("Columns", df.shape[1])
        with col3: 
            missing = df.isnull().sum().sum()
            st.metric("Missing Values", f"{missing:,}")
        with col4: 
            mem = df.memory_usage(deep=True).sum() / 1024**2
            st.metric("Memory", f"{mem:.2f} MB")
        
        st.markdown("<div class='section-header'>📋 Column Analysis</div>", unsafe_allow_html=True)
        
        # Detailed Analysis Table
        analysis_data = []
        for col in df.columns:
            analysis_data.append({
                "Column": col,
                "Type": str(df[col].dtype),
                "Unique": df[col].nunique(),
                "Missing": df[col].isnull().sum(),
                "Missing %": f"{(df[col].isnull().sum() / len(df) * 100):.1f}%"
            })
        
        analysis_df = pd.DataFrame(analysis_data)
        st.dataframe(analysis_df, use_container_width=True, height=300)
        
        st.markdown("<div class='section-header'>👁️ Data Preview</div>", unsafe_allow_html=True)
        st.dataframe(df.head(10), use_container_width=True)
        
        # Download Report
        csv_report = analysis_df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Download Analysis Report", csv_report, "data_report.csv", "text/csv")

    # ==========================================
    # GLOBAL DOWNLOAD (Always visible if data exists)
    # ==========================================
    st.markdown("<div style='margin-top: 4rem; border-top: 1px solid rgba(255,255,255,0.3); padding-top: 2rem;'>", unsafe_allow_html=True)
    col_d1, col_d2 = st.columns([4, 1])
    with col_d1:
        st.markdown("### 💾 Final Export")
        st.caption("Download your processed data in CSV format.")
    with col_d2:
        csv_bytes = st.session_state.df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv_bytes,
            file_name=f"processed_{st.session_state.filename.split('.')[0]}.csv",
            mime="text/csv",
            use_container_width=True
        )
    st.markdown("</div>", unsafe_allow_html=True)
