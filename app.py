import streamlit as st
from predictor import show_predict_page
from bulk_scanner import show_bulk_scanner_page

st.set_page_config(
    page_title="Developer Salary Predictor",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced professional theme with modern design
st.markdown("""
<style>
    /* Root color variables */
    :root {
        --primary-color: #007bff;
        --primary-dark: #0056b3;
        --success-color: #28a745;
        --info-color: #17a2b8;
        --danger-color: #dc3545;
        --light-bg: #f8f9fa;
        --card-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    /* Main background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
    }
    
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #e9ecef 100%);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        color: #1e3c72;
    }
    
    [data-testid="stSidebar"] label {
        color: #2a5298;
        font-weight: 600;
        font-size: 0.95rem;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: #1e3c72;
    }
    
    [data-testid="stSidebar"] h3 {
        color: #007bff;
        font-size: 1.1rem;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div > div {
        background-color: white;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: var(--transition);
        color: #1e3c72;
    }
    
    [data-testid="stSidebar"] .stSelectbox > div > div > div:focus-within {
        border-color: #007bff;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.2);
    }
    
    /* Main container */
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #1e3c72;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    
    h1 {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        background: linear-gradient(135deg, #007bff 0%, #0056b3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.8rem;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #007bff;
        padding-bottom: 0.5rem;
    }
    
    h3 {
        font-size: 1.3rem;
        color: #2a5298;
        margin-top: 1.5rem;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #007bff 0%, #0056b3 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 28px;
        font-size: 16px;
        font-weight: 600;
        transition: var(--transition);
        box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #0056b3 0%, #003d82 100%);
        box-shadow: 0 6px 16px rgba(0, 123, 255, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Form inputs */
    .stSelectbox > div > div > div,
    .stTextInput > div > div > input,
    .stSlider > div > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: var(--transition);
        background-color: white;
    }
    
    .stSelectbox > div > div > div:focus-within,
    .stTextInput > div > div > input:focus,
    .stSlider > div > div > div:hover {
        border-color: #007bff;
        box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.1);
    }
    
    .stTextInput label,
    .stSelectbox label,
    .stSlider label {
        color: #2a5298;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
    }
    
    /* Success messages */
    .stSuccess {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border-left: 5px solid #28a745;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(40, 167, 69, 0.1);
        animation: slideIn 0.3s ease-out;
    }
    
    /* Info messages */
    .stInfo {
        background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%);
        border-left: 5px solid #17a2b8;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(23, 162, 184, 0.1);
        animation: slideIn 0.3s ease-out;
    }
    
    /* Error messages */
    .stError {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border-left: 5px solid #dc3545;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(220, 53, 69, 0.1);
        animation: slideIn 0.3s ease-out;
    }
    
    /* Warning messages */
    .stWarning {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 5px solid #ffc107;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 4px 12px rgba(255, 193, 7, 0.1);
    }
    
    /* Divider styling */
    hr {
        border: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #007bff 50%, transparent 100%);
        margin: 2rem 0;
        opacity: 0.6;
    }
    
    /* Cards */
    .card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
        border: 1px solid #e9ecef;
        margin-bottom: 1.5rem;
        transition: var(--transition);
    }
    
    .card:hover {
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
        transform: translateY(-2px);
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #007bff;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #0056b3;
    }
    
    /* Text styling */
    .stMarkdown {
        color: #333333;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        h1 {
            font-size: 2rem;
        }
        h2 {
            font-size: 1.5rem;
        }
        .block-container {
            padding: 1rem 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header section
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("# 💼 Developer Salary Predictor")
    st.markdown("*Discover your potential earnings based on your skills and experience*")

with col2:
    st.markdown("")
    st.markdown("")
    st.info("🔍 ML-Powered Salary Insights")

st.markdown("---")

# Sidebar configuration
st.sidebar.markdown("### ⚙️ Navigation")
page = st.sidebar.selectbox(
    "Choose a page",
    ("Predict Salary", "Bulk Scanner", "About"),  # ← ADDED "Bulk Scanner"
    help="Select a page to navigate"
)

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 How It Works
1. **Input** your experience level
2. **Select** your role and skills
3. **Get** accurate salary estimates
4. **Compare** with market trends
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 💡 Tips
- More experience = Higher salary
- In-demand skills boost earnings
- Your location affects compensation
""")

# Page routing
if page == "Predict Salary":
    show_predict_page()

elif page == "Bulk Scanner":          # ← NEW ROUTE
    show_bulk_scanner_page()

else:
    st.title("📊 About This Predictor")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎯 Our Mission
        Help developers understand their market value and make informed career decisions.
        
        ### 📈 Data Source
        - Based on real survey data from thousands of developers
        - Updated machine learning models
        - Covers global salary ranges
        """)
    
    with col2:
        st.markdown("""
        ### ✨ Features
        - **Accurate Predictions** using advanced ML models
        - **Multiple Factors** considered in calculation
        - **Real-time Results** instant salary estimates
        - **Bulk Scanner** predict salaries for many records at once
        - **Completely Free** no hidden costs
        """)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Models Used", "Linear Regression", "✓")
    
    with col2:
        st.metric("Data Points", "10K+", "📊")
    
    with col3:
        st.metric("Accuracy", "High", "📈")
    
    st.markdown("---")
    
    st.markdown("""
    ### 🚀 Get Started
    Click on **"Predict Salary"** in the sidebar to begin calculating your estimated salary,
    or use **"Bulk Scanner"** to predict salaries for multiple developers at once.
    """)
    
    st.success("Made with ❤️ for developers worldwide")
