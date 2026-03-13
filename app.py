"""
MUJ Student Advisor AI - Complete Implementation
PS 01: Student Academic Performance Prediction
Enhanced UI/UX Version (Light Theme + Wide Sidebar)
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import base64
import re

# ==================== PAGE CONFIGURATION ====================
st.set_page_config(
    page_title="MUJ Student Advisor AI",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS (LIGHT THEME + WIDE SIDEBAR) ====================
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles & Light Theme Enforcements */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #1E293B !important; 
        background-color: #F8FAFC; 
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Poppins', sans-serif;
        font-weight: 600;
        letter-spacing: -0.02em;
    }
    
    /* Wider Sidebar */
    [data-testid="stSidebar"] {
        min-width: 480px !important;
        max-width: 500px !important;
        background-color: #FFFFFF !important;
        padding-top: 1.5rem;
        padding-right: 1.5rem;
        padding-left: 1.5rem;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Fix Streamlit Input Fields */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
    }
    .stNumberInput input, .stTextInput input {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* Main Header */
    .main-header {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        font-weight: 700;
    }
    
    .sub-header {
        font-size: 1.8rem;
        color: #1E3A8A !important;
        margin-bottom: 1.5rem;
        border-bottom: 3px solid #3B82F6;
        padding-bottom: 0.5rem;
        font-weight: 600;
    }
    
    .section-header {
        font-size: 1.4rem;
        color: #1E3A8A !important;
        margin: 1rem 0 1rem 0;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Result Boxes */
    .success-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    }
    .success-box div { color: white !important; }
    
    .warning-box {
        background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 20px rgba(245, 158, 11, 0.3);
    }
    .warning-box div { color: white !important; }
    
    .danger-box {
        background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 20px rgba(239, 68, 68, 0.3);
    }
    .danger-box div { color: white !important; }
    
    .info-box {
        background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white !important;
        margin: 1rem 0 2rem 0;
        box-shadow: 0 4px 20px rgba(59, 130, 246, 0.3);
    }
    .info-box div { color: white !important; }
    
    .grade-title { font-size: 2.2rem; font-weight: 700; margin-bottom: 0.5rem; }
    .grade-description { font-size: 1.1rem; opacity: 0.95; margin-bottom: 1rem; }
    .grade-badge { display: inline-block; background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; border-radius: 50px; font-size: 1rem; margin: 0.5rem 0; }
    
    /* Cards & Layout */
    .feature-card { background: #FFFFFF; padding: 1.2rem; border-radius: 12px; margin: 0.5rem 0; border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .feature-icon { font-size: 1.5rem; margin-right: 0.5rem; }
    .feature-label { font-weight: 600; color: #1E3A8A; margin-bottom: 0.25rem; }
    .feature-value { font-size: 1.1rem; color: #0F172A; }
    
    .metric-card { background: white; padding: 1.2rem; border-radius: 12px; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid #E2E8F0; }
    .metric-icon { font-size: 2rem; margin-bottom: 0.5rem; }
    .metric-label { font-size: 0.9rem; color: #64748B; text-transform: uppercase; }
    .metric-value { font-size: 2rem; font-weight: 700; color: #1E3A8A; margin: 0.5rem 0; }
    
    [data-testid="column"] { display: flex; flex-direction: column; }
    .contact-card { background: white; padding: 1.5rem; border-radius: 15px; border: 1px solid #E2E8F0; box-shadow: 0 4px 15px rgba(0,0,0,0.05); flex-grow: 1; display: flex; flex-direction: column; margin-top: 1rem;}
    .contact-title { font-size: 1.2rem; font-weight: 600; color: #1E3A8A !important; margin-bottom: 1rem; }
    .contact-detail { padding: 0.5rem 0; border-bottom: 1px solid #E2E8F0; color: #334155; }
    .contact-detail:last-child { border-bottom: none; }
    
    .recommendation-item { background: white; padding: 1rem; border-radius: 10px; margin: 0.5rem 0; border-left: 4px solid #3B82F6; box-shadow: 0 2px 8px rgba(0,0,0,0.05); color: #1E293B; }
    
    /* Confidence Bar */
    .confidence-item { margin: 0.75rem 0; }
    .confidence-label { display: flex; justify-content: space-between; margin-bottom: 0.25rem; font-weight: 500; color: #1E293B; }
    .confidence-bar-bg { background: #E2E8F0; border-radius: 10px; height: 24px; width: 100%; overflow: hidden; }
    .confidence-bar-fill { height: 24px; border-radius: 10px; transition: width 0.5s ease-in-out; }
    
    /* Buttons */
    .stButton > button { background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%); color: white !important; font-weight: 600; padding: 0.75rem 2rem; border-radius: 12px; border: none; width: 100%; font-size: 1.1rem; text-transform: uppercase; transition: all 0.3s; box-shadow: 0 4px 15px rgba(30, 58, 138, 0.3); }
    .stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(30, 58, 138, 0.4); }
    
    /* Tabs & Dividers */
    .stTabs [data-baseweb="tab-list"] { gap: 2rem; background: white; padding: 0.5rem; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
    .stTabs [data-baseweb="tab"] { height: 3rem; font-weight: 600; color: #64748B !important; border-radius: 8px; }
    .stTabs [aria-selected="true"] { background: #1E3A8A !important; color: white !important; }
    .custom-divider { height: 2px; background: linear-gradient(90deg, transparent, #3B82F6, transparent); margin: 2rem 0; }
    .footer { text-align: center; padding: 2rem; color: #64748B; font-size: 0.9rem; border-top: 1px solid #E2E8F0; margin-top: 2rem; }
</style>
""", unsafe_allow_html=True)

# ==================== LOAD MODEL AND METADATA ====================
@st.cache_resource
def load_model():
    """Load the trained model and metadata"""
    try:
        with open('student_performance_predictor.pkl', 'rb') as f:
            model = pickle.load(f)
        try:
            with open('model_metadata.pkl', 'rb') as f:
                metadata = pickle.load(f)
        except:
            metadata = None
        return model, metadata
    except FileNotFoundError:
        st.error("❌ Model file not found! Please run train_model.py first.")
        st.stop()

model, metadata = load_model()

# ==================== LOAD GUIDELINES ====================
def load_guidelines():
    """Load MUJ student success guidelines"""
    try:
        with open('muj_guidelines.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
MUJ STUDENT SUCCESS GUIDELINES:

GRADE CATEGORY 0 (Highest Performers):
- Invite to the 'Student Excellence' Research Program for guided undergraduate research.
- Suggest applying for Peer Mentor or Teaching Assistant (TA) roles for junior CSE batches.
- Recommend advanced certification courses in specialized domains like AI/ML or Cloud Computing.
- Encourage submitting their semester projects to national hackathons.

GRADE CATEGORY 1 (Above Average):
- Suggest joining technical clubs like IEEE CIS MUJ.
- Recommend exploring elective subjects in specialized CSE domains.
- Encourage participation in coding competitions and hackathons.
- Suggest taking up leadership roles in student chapters.

GRADE CATEGORY 2 (Below Average):
- Recommend attending weekly Faculty Office Hours.
- Suggest the 'Time Management & Study Skills' workshop.
- Encourage forming study groups with peers.
- Recommend using online learning resources like NPTEL.

GRADE CATEGORY 3 (At-Risk):
- Immediate mandatory referral to the Student Success Center for an academic recovery plan.
- Require a confidential meeting with the Campus Counselor to address potential stress or burnout.
- Recommend a strict 50% reduction in extracurricular and club commitments to prioritize core academics.
- Assign a dedicated senior peer mentor for weekly accountability and assignment tracking.
- Suggest a review of their current course load to see if dropping a non-core elective is necessary to protect their GPA.
"""

guidelines = load_guidelines()

# ==================== FEATURE DEFINITIONS ====================
FEATURE_INFO = {
    'StudyHours': {'description': 'Weekly hours spent studying', 'range': (5, 43), 'default': 20, 'icon': '📚'},
    'Attendance': {'description': 'Class attendance percentage', 'range': (60, 100), 'default': 80, 'icon': '📊'},
    'Resources': {'description': 'Access to learning resources', 'options': {0: 'Limited', 1: 'Basic', 2: 'Extensive'}, 'default': 1, 'icon': '📖'},
    'Extracurricular': {'description': 'Participation in extracurricular activities', 'options': {0: 'No', 1: 'Yes'}, 'default': 0, 'icon': '⚽'},
    'Motivation': {'description': 'Student motivation level', 'options': {0: 'Low', 1: 'Medium', 2: 'High'}, 'default': 1, 'icon': '🎯'},
    'Internet': {'description': 'Internet access availability', 'options': {0: 'No', 1: 'Yes'}, 'default': 1, 'icon': '🌐'},
    'Gender': {'description': 'Student gender', 'options': {0: 'Male', 1: 'Female'}, 'default': 0, 'icon': '👤'},
    'Age': {'description': 'Student age', 'range': (18, 30), 'default': 21, 'icon': '🎂'},
    'LearningStyle': {'description': 'Preferred learning style', 'options': {0: 'Visual', 1: 'Auditory', 2: 'Reading/Writing', 3: 'Kinesthetic'}, 'default': 0, 'icon': '🧠'},
    'OnlineCourses': {'description': 'Number of online courses taken', 'range': (0, 20), 'default': 5, 'icon': '💻'},
    'Discussions': {'description': 'Participation in academic discussions', 'options': {0: 'No', 1: 'Yes'}, 'default': 1, 'icon': '💬'},
    'AssignmentCompletion': {'description': 'Percentage of assignments completed', 'range': (50, 100), 'default': 85, 'icon': '📝'},
    'ExamScore': {'description': 'Score on primary examination', 'range': (40, 100), 'default': 75, 'icon': '📋'},
    'EduTech': {'description': 'Use of educational technology tools', 'options': {0: 'No', 1: 'Yes'}, 'default': 1, 'icon': '🖥️'},
    'StressLevel': {'description': 'Reported stress level', 'options': {0: 'Low', 1: 'Medium', 2: 'High'}, 'default': 1, 'icon': '😰'}
}

GRADE_INFO = {
    0: {'name': 'Highest Performer', 'description': 'Excellent academic standing - Top of the class', 'color': '#10B981', 'emoji': '🌟', 'range': '90-100%', 'short': 'Best'},
    1: {'name': 'Above Average', 'description': 'Good academic standing - Above peer average', 'color': '#3B82F6', 'emoji': '📈', 'range': '75-89%', 'short': 'Above Avg'},
    2: {'name': 'Below Average', 'description': 'Needs improvement - Below peer average', 'color': '#F59E0B', 'emoji': '⚠️', 'range': '60-74%', 'short': 'Below Avg'},
    3: {'name': 'At-Risk', 'description': 'Requires immediate intervention', 'color': '#EF4444', 'emoji': '🚨', 'range': 'Below 60%', 'short': 'At-Risk'}
}

# ==================== CALLBACK FOR DEMO PROFILES ====================
def apply_demo_profile(demo_data):
    st.session_state['ExamScore'] = demo_data['ExamScore']
    st.session_state['Attendance'] = demo_data['Attendance']
    st.session_state['StudyHours'] = demo_data['StudyHours']
    st.session_state['StressLevel'] = demo_data['Stress']
    
    for key in FEATURE_INFO.keys():
        if key not in ['ExamScore', 'Attendance', 'StudyHours', 'StressLevel']:
            st.session_state[key] = FEATURE_INFO[key]['default']
    
    st.session_state['auto_predict'] = True

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown('<div class="sidebar-header">🎓 MUJ Student Portal</div>', unsafe_allow_html=True)
    
    # IMAGE REMOVED - No logo displayed
    st.markdown("### 📋 Student Information")
    st.markdown("Enter the student's complete profile below:")
    st.markdown("---")
    
    input_data = {}
    
    with st.expander("📚 Academic Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['StudyHours'] = st.slider("📚 Study Hours", FEATURE_INFO['StudyHours']['range'][0], FEATURE_INFO['StudyHours']['range'][1], FEATURE_INFO['StudyHours']['default'], key='StudyHours')
            input_data['AssignmentCompletion'] = st.slider("📝 Assignment %", FEATURE_INFO['AssignmentCompletion']['range'][0], FEATURE_INFO['AssignmentCompletion']['range'][1], FEATURE_INFO['AssignmentCompletion']['default'], key='AssignmentCompletion')
        with col2:
            input_data['Attendance'] = st.slider("📊 Attendance %", FEATURE_INFO['Attendance']['range'][0], FEATURE_INFO['Attendance']['range'][1], FEATURE_INFO['Attendance']['default'], key='Attendance')
            input_data['ExamScore'] = st.slider("📋 Exam Score", FEATURE_INFO['ExamScore']['range'][0], FEATURE_INFO['ExamScore']['range'][1], FEATURE_INFO['ExamScore']['default'], key='ExamScore')
    
    with st.expander("🧠 Psychological Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['Motivation'] = st.selectbox("🎯 Motivation", list(FEATURE_INFO['Motivation']['options'].keys()), format_func=lambda x: FEATURE_INFO['Motivation']['options'][x], key='Motivation')
            input_data['LearningStyle'] = st.selectbox("🧠 Learning Style", list(FEATURE_INFO['LearningStyle']['options'].keys()), format_func=lambda x: FEATURE_INFO['LearningStyle']['options'][x], key='LearningStyle')
        with col2:
            input_data['StressLevel'] = st.selectbox("😰 Stress Level", list(FEATURE_INFO['StressLevel']['options'].keys()), format_func=lambda x: FEATURE_INFO['StressLevel']['options'][x], key='StressLevel')
    
    with st.expander("👥 Demographic Factors", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['Gender'] = st.radio("👤 Gender", list(FEATURE_INFO['Gender']['options'].keys()), format_func=lambda x: FEATURE_INFO['Gender']['options'][x], horizontal=True, key='Gender')
        with col2:
            input_data['Age'] = st.number_input("🎂 Age", FEATURE_INFO['Age']['range'][0], FEATURE_INFO['Age']['range'][1], FEATURE_INFO['Age']['default'], key='Age')
    
    with st.expander("🌐 Environmental & Social", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            input_data['Internet'] = st.selectbox("🌐 Internet", list(FEATURE_INFO['Internet']['options'].keys()), format_func=lambda x: FEATURE_INFO['Internet']['options'][x], key='Internet')
            input_data['Resources'] = st.selectbox("📖 Resources", list(FEATURE_INFO['Resources']['options'].keys()), format_func=lambda x: FEATURE_INFO['Resources']['options'][x], key='Resources')
            input_data['OnlineCourses'] = st.slider("💻 Online Courses", FEATURE_INFO['OnlineCourses']['range'][0], FEATURE_INFO['OnlineCourses']['range'][1], FEATURE_INFO['OnlineCourses']['default'], key='OnlineCourses')
        with col2:
            input_data['EduTech'] = st.selectbox("🖥️ EduTech Use", list(FEATURE_INFO['EduTech']['options'].keys()), format_func=lambda x: FEATURE_INFO['EduTech']['options'][x], key='EduTech')
            input_data['Extracurricular'] = st.selectbox("⚽ Extracurricular", list(FEATURE_INFO['Extracurricular']['options'].keys()), format_func=lambda x: FEATURE_INFO['Extracurricular']['options'][x], key='Extracurricular')
            input_data['Discussions'] = st.selectbox("💬 Discussions", list(FEATURE_INFO['Discussions']['options'].keys()), format_func=lambda x: FEATURE_INFO['Discussions']['options'][x], key='Discussions')
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    predict_clicked = st.button("🔮 GENERATE SUCCESS PLAN", use_container_width=True)
    
    if predict_clicked or st.session_state.get('auto_predict', False):
        if 'auto_predict' in st.session_state:
            st.session_state['auto_predict'] = False
            
        feature_order = ['StudyHours', 'Attendance', 'Resources', 'Extracurricular',
                        'Motivation', 'Internet', 'Gender', 'Age', 'LearningStyle',
                        'OnlineCourses', 'Discussions', 'AssignmentCompletion',
                        'ExamScore', 'EduTech', 'StressLevel']
        
        input_list = [input_data[feature] for feature in feature_order]
        input_df = pd.DataFrame([input_list], columns=feature_order)
        
        prediction = model.predict(input_df)[0]
        probabilities = model.predict_proba(input_df)[0]
        
        st.session_state['prediction'] = prediction
        st.session_state['probabilities'] = probabilities
        st.session_state['input_data'] = input_data
        st.success("✅ Prediction generated! Scroll down to view results.")

# ==================== MAIN CONTENT ====================
st.markdown('<h1 class="main-header">🎓 MUJ Student Advisor AI</h1>', unsafe_allow_html=True)
st.markdown("""<p style="text-align: center; font-size: 1.2rem; color: #64748B; margin-bottom: 2rem;">Intelligent Student Performance Prediction & Personalized Intervention System</p>""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 PREDICTION & ANALYSIS", "📈 DEEP DIVE", "📚 GUIDELINES", "ℹ️ ABOUT"])

with tab1:
    st.markdown('<h2 class="sub-header">🚀 Quick Start: Demo Profiles</h2>', unsafe_allow_html=True)
    st.write("Load a sample student profile to instantly generate a prediction and personalized success plan.")
    
    demo_cols = st.columns(4)
    demos = [
        {"name": "🌟 High Performer", "ExamScore": 95, "Attendance": 98, "StudyHours": 35, "Stress": 0, "color": "#10B981"},
        {"name": "📈 Above Average", "ExamScore": 82, "Attendance": 85, "StudyHours": 25, "Stress": 1, "color": "#3B82F6"},
        {"name": "⚠️ Below Average", "ExamScore": 68, "Attendance": 70, "StudyHours": 15, "Stress": 1, "color": "#F59E0B"},
        {"name": "🚨 At-Risk", "ExamScore": 45, "Attendance": 60, "StudyHours": 8, "Stress": 2, "color": "#EF4444"}
    ]
    
    for col, demo in zip(demo_cols, demos):
        with col:
            st.markdown(f"""
            <div class="content-card" style="text-align: center; height: 100%; border-left: 4px solid {demo['color']}; padding: 1rem; border-radius: 12px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <h4 style="margin-bottom: 1rem; color: {demo['color']};">{demo['name']}</h4>
                <p style="margin: 0.2rem 0; font-weight: 500;">📋 Exam: {demo['ExamScore']}</p>
                <p style="margin: 0.2rem 0; font-weight: 500;">📊 Att: {demo['Attendance']}%</p>
                <p style="margin: 0.2rem 0; font-weight: 500;">📚 Study: {demo['StudyHours']}h</p>
            </div>
            <div style="margin-top: 10px;"></div>
            """, unsafe_allow_html=True)
            
            st.button(
                f"Load {demo['name'].split()[1]}", 
                key=f"demo_tab1_{demo['name']}", 
                use_container_width=True,
                on_click=apply_demo_profile,
                args=(demo,)
            )

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">👤 Student Profile Summary</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<p class="section-header">📚 Academic</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card"><span class="feature-icon">📚</span><span class="feature-label">Study Hours</span><br><span class="feature-value">{input_data['StudyHours']} hrs/week</span></div>
        <div class="feature-card"><span class="feature-icon">📊</span><span class="feature-label">Attendance</span><br><span class="feature-value">{input_data['Attendance']}%</span></div>
        <div class="feature-card"><span class="feature-icon">📝</span><span class="feature-label">Assignment Completion</span><br><span class="feature-value">{input_data['AssignmentCompletion']}%</span></div>
        <div class="feature-card"><span class="feature-icon">📋</span><span class="feature-label">Exam Score</span><br><span class="feature-value">{input_data['ExamScore']}</span></div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown('<p class="section-header">🧠 Psychological</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card"><span class="feature-icon">🎯</span><span class="feature-label">Motivation</span><br><span class="feature-value">{FEATURE_INFO['Motivation']['options'][input_data['Motivation']]}</span></div>
        <div class="feature-card"><span class="feature-icon">😰</span><span class="feature-label">Stress Level</span><br><span class="feature-value">{FEATURE_INFO['StressLevel']['options'][input_data['StressLevel']]}</span></div>
        <div class="feature-card"><span class="feature-icon">🧠</span><span class="feature-label">Learning Style</span><br><span class="feature-value">{FEATURE_INFO['LearningStyle']['options'][input_data['LearningStyle']]}</span></div>
        <div class="feature-card"><span class="feature-icon">🎂</span><span class="feature-label">Age</span><br><span class="feature-value">{input_data['Age']} years</span></div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown('<p class="section-header">🌐 Environmental</p>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="feature-card"><span class="feature-icon">🌐</span><span class="feature-label">Internet Access</span><br><span class="feature-value">{FEATURE_INFO['Internet']['options'][input_data['Internet']]}</span></div>
        <div class="feature-card"><span class="feature-icon">📖</span><span class="feature-label">Learning Resources</span><br><span class="feature-value">{FEATURE_INFO['Resources']['options'][input_data['Resources']]}</span></div>
        <div class="feature-card"><span class="feature-icon">💻</span><span class="feature-label">Online Courses</span><br><span class="feature-value">{input_data['OnlineCourses']}</span></div>
        <div class="feature-card"><span class="feature-icon">⚽</span><span class="feature-label">Extracurricular</span><br><span class="feature-value">{FEATURE_INFO['Extracurricular']['options'][input_data['Extracurricular']]}</span></div>
        """, unsafe_allow_html=True)
    
    if 'prediction' in st.session_state:
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        st.markdown('<h2 class="sub-header">🎯 Prediction Results</h2>', unsafe_allow_html=True)
        
        pred = st.session_state['prediction']
        probabilities = st.session_state['probabilities']
        grade_info = GRADE_INFO[pred]
        
        box_class = ["success-box", "info-box", "warning-box", "danger-box"][pred]
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown(f"""
            <div class="{box_class}">
                <span class="grade-badge">Predicted Grade Category: {pred}</span>
                <div class="grade-title">{grade_info['emoji']} {grade_info['name']}</div>
                <div class="grade-description">{grade_info['description']}</div>
                <div style="font-size: 1.2rem; margin-top: 1rem;">Expected Score Range: <strong>{grade_info['range']}</strong></div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("#### 📊 Confidence Meter")
            for i, prob in enumerate(probabilities):
                st.markdown(f"""
                <div class="confidence-item">
                    <div class="confidence-label"><span>{GRADE_INFO[i]['short']}</span><span>{prob:.1%}</span></div>
                    <div class="confidence-bar-bg"><div class="confidence-bar-fill" style="width: {prob*100}%; background: {GRADE_INFO[i]['color']};"></div></div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
        
        # FIXED SECTION - Properly indented with hardcoded recommendations
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown('<h2 class="sub-header">📋 Personalized Success Plan</h2>', unsafe_allow_html=True)
            st.markdown('<div class="contact-card" style="min-height: 280px;">', unsafe_allow_html=True)
            
            # DIRECT HARDCODED RECOMMENDATIONS - NO FILE DEPENDENCY
            if pred == 0:
                st.markdown("""
                <div class="recommendation-item" style="margin: 5px 0;">✅ Invite to the 'Student Excellence' Research Program for guided undergraduate research.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest applying for Peer Mentor or Teaching Assistant (TA) roles for junior CSE batches.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend advanced certification courses in specialized domains like AI/ML or Cloud Computing.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Encourage submitting their semester projects to national hackathons.</div>
                """, unsafe_allow_html=True)
            elif pred == 1:
                st.markdown("""
                <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest joining technical clubs like IEEE CIS MUJ.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend exploring elective subjects in specialized CSE domains.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Encourage participation in coding competitions and hackathons.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest taking up leadership roles in student chapters.</div>
                """, unsafe_allow_html=True)
            elif pred == 2:
                st.markdown("""
                <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend attending weekly Faculty Office Hours.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest the 'Time Management & Study Skills' workshop.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Encourage forming study groups with peers.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend using online learning resources like NPTEL.</div>
                """, unsafe_allow_html=True)
            else:  # pred == 3 (At-Risk) - This matches your image
                st.markdown("""
                <div class="recommendation-item" style="margin: 5px 0;">✅ Immediate mandatory referral to the Student Success Center for an academic recovery plan.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Require a confidential meeting with the Campus Counselor to address potential stress or burnout.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend a strict 50% reduction in extracurricular and club commitments to prioritize core academics.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Assign a dedicated senior peer mentor for weekly accountability and assignment tracking.</div>
                <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest a review of their current course load to see if dropping a non-core elective is necessary to protect their GPA.</div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<h2 class="sub-header">📞 Contact Points</h2>', unsafe_allow_html=True)
            if pred == 0:
                st.markdown("""<div class="contact-card" style="min-height: 280px;"><div class="contact-title">👨‍🏫 Research Coordinator</div><div class="contact-detail"><strong>Dr. Rajesh Kumar</strong></div><div class="contact-detail">📧 rajesh.kumar@muj.edu</div><div class="contact-detail">📍 AB-1, Room 204</div></div>""", unsafe_allow_html=True)
            elif pred == 1:
                st.markdown("""<div class="contact-card" style="min-height: 280px;"><div class="contact-title">🤖 IEEE CIS MUJ</div><div class="contact-detail"><strong>Prof. Priya Sharma</strong></div><div class="contact-detail">📧 priya.sharma@muj.edu</div><div class="contact-detail">📍 AB-2, Room 105</div></div>""", unsafe_allow_html=True)
            elif pred == 2:
                st.markdown("""<div class="contact-card" style="min-height: 280px;"><div class="contact-title">👨‍🏫 Academic Advisor</div><div class="contact-detail"><strong>Dr. Amit Patel</strong></div><div class="contact-detail">🕒 Tue/Thu 2-4 PM</div><div class="contact-detail">📍 AB-1, Room 305</div></div>""", unsafe_allow_html=True)
            else:
                st.markdown("""<div class="contact-card" style="min-height: 280px;"><div class="contact-title">🆘 Student Success Center</div><div class="contact-detail">📧 success@muj.edu</div><div class="contact-detail">📞 +91-123-4567890</div><div class="contact-detail">📍 Student Services Block</div></div>""", unsafe_allow_html=True)
    else:
        st.info("👆 Load a demo profile above or click 'GENERATE SUCCESS PLAN' in the sidebar to see prediction results.")

with tab2:
    st.markdown('<h2 class="sub-header">📈 Performance Analysis Dashboard</h2>', unsafe_allow_html=True)
    if 'prediction' in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if metadata and 'feature_importance' in metadata:
                st.markdown("#### 🔍 Top Predictive Features")
                import_df = pd.DataFrame(metadata['feature_importance']).head(8)
                fig = px.bar(import_df, x='importance', y='feature', orientation='h', title='Most Important Factors', color='importance', color_continuous_scale='Blues')
                fig.update_layout(height=400, showlegend=False, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font=dict(color='#1E293B'))
                st.plotly_chart(fig, use_container_width=True)
            
            stress_impact = {
                0: "✨ **Low Stress**: Students with low stress typically perform 10-15% better than peers",
                1: "⚖️ **Moderate Stress**: Can be motivating if managed well through proper techniques",
                2: "⚠️ **High Stress**: Reduces performance by 20-30% - immediate intervention recommended"
            }
            st.markdown("#### 🧠 Stress Impact Analysis")
            st.info(stress_impact[st.session_state['input_data']['StressLevel']])
        
        with col2:
            st.markdown("#### 📊 Profile Comparison")
            st.markdown("*Comparing with MUJ student averages*")
            metrics = [
                ("Exam Score", st.session_state['input_data']['ExamScore'], 75, "📋"),
                ("Attendance", st.session_state['input_data']['Attendance'], 85, "📊"),
                ("Study Hours", st.session_state['input_data']['StudyHours'], 20, "📚"),
                ("Assignment Completion", st.session_state['input_data']['AssignmentCompletion'], 85, "📝")
            ]
            for name, value, avg, icon in metrics:
                diff = value - avg
                diff_class = "diff-positive" if diff > 0 else "diff-negative" if diff < 0 else "diff-neutral"
                st.markdown(f'<div class="metric-card"><div class="metric-icon">{icon}</div><div class="metric-label">{name}</div><div class="metric-value">{value}</div><div><span class="metric-diff {diff_class}">{"+" if diff > 0 else ""}{diff:.1f} vs avg</span></div></div>', unsafe_allow_html=True)
    else:
        st.info("👆 Generate a prediction first to see detailed analysis")

with tab3:
    st.markdown('<h2 class="sub-header">📚 MUJ Student Success Guidelines</h2>', unsafe_allow_html=True)
    
    # Simple display without regex complications
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 2rem;">
        <h3 style="color: #10B981; margin-bottom: 1rem;">🌟 GRADE CATEGORY 0 (Highest Performers)</h3>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Invite to the 'Student Excellence' Research Program for guided undergraduate research.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest applying for Peer Mentor or Teaching Assistant (TA) roles for junior CSE batches.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend advanced certification courses in specialized domains like AI/ML or Cloud Computing.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Encourage submitting their semester projects to national hackathons.</div>
    </div>
    
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 2rem;">
        <h3 style="color: #3B82F6; margin-bottom: 1rem;">📈 GRADE CATEGORY 1 (Above Average)</h3>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest joining technical clubs like IEEE CIS MUJ.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend exploring elective subjects in specialized CSE domains.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Encourage participation in coding competitions and hackathons.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest taking up leadership roles in student chapters.</div>
    </div>
    
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 2rem;">
        <h3 style="color: #F59E0B; margin-bottom: 1rem;">⚠️ GRADE CATEGORY 2 (Below Average)</h3>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend attending weekly Faculty Office Hours.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest the 'Time Management & Study Skills' workshop.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Encourage forming study groups with peers.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend using online learning resources like NPTEL.</div>
    </div>
    
    <div style="background: white; padding: 2rem; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); margin-bottom: 2rem;">
        <h3 style="color: #EF4444; margin-bottom: 1rem;">🚨 GRADE CATEGORY 3 (At-Risk)</h3>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Immediate mandatory referral to the Student Success Center for an academic recovery plan.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Require a confidential meeting with the Campus Counselor to address potential stress or burnout.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Recommend a strict 50% reduction in extracurricular and club commitments to prioritize core academics.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Assign a dedicated senior peer mentor for weekly accountability and assignment tracking.</div>
        <div class="recommendation-item" style="margin: 5px 0;">✅ Suggest a review of their current course load to see if dropping a non-core elective is necessary to protect their GPA.</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.download_button(
        label="📥 Download Guidelines PDF", 
        data=guidelines, 
        file_name="MUJ_Guidelines.txt", 
        mime="text/plain", 
        use_container_width=True
    )

with tab4:
    st.markdown('<h2 class="sub-header">ℹ️ About This System</h2>', unsafe_allow_html=True)
    st.markdown("### 🎯 System Purpose & Objectives")
    st.write("""
    The **MUJ Student Advisor AI** is a proactive, data-driven institutional tool designed to transform academic advising from a reactive process into a predictive science. 
    
    By continuously analyzing 15 distinct factors across academic performance, psychological well-being, demographic background, and environmental circumstances, this system empowers faculty and administrators to:
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("**🔍 Identify At-Risk Students Early**\n\nDetect subtle behavioral and academic patterns—such as fluctuating attendance or high stress levels—weeks before they result in failed examinations.")
        st.warning("**📈 Optimize Resource Allocation**\n\nDirect campus counselors, peer mentors, and academic advisors exactly where they are needed most, maximizing the impact of support staff.")
    with col2:
        st.success("**🎯 Personalize Interventions**\n\nMove beyond generic advising by providing hyper-specific, automated recovery plans dynamically tailored to the student's risk profile.")
        st.error("**⚖️ Mitigate Assessment Bias**\n\nProvide an equitable, objective, and consistent assessment of every student's trajectory, free from human error or demographic assumptions.")

# Footer
st.markdown("""
<div class="footer">
    <div style="font-size: 1.2rem; font-weight: 600; margin-bottom: 0.5rem;">🎓 MUJ Student Advisor AI</div>
    <div style="margin-bottom: 0.5rem;">Developed for IEEE CIS AI Model Quest 2.0 | PS 01: Student Academic Performance Prediction</div>
    <div>📍 Manipal University Jaipur | Department of Computer Science & Engineering</div>
    <div style="margin-top: 1rem; font-size: 0.8rem; color: #94A3B8;">© 2026 All Rights Reserved</div>
</div>
""", unsafe_allow_html=True)