import streamlit as st
import firebase_admin
from firebase_admin import credentials, auth, firestore, storage
import os
import tempfile
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import time
import base64
from PIL import Image
import io
import re
import random
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import altair as alt
from streamlit_lottie import st_lottie
import json
import requests

# Initialize Firebase if not already initialized
if not firebase_admin._apps:
    # Firebase configuration
    firebase_config = {
        "apiKey": "AIzaSyC7e1RJyWeRTa7rDguJrEC1XQhQfxriddQ",
        "authDomain": "hiresense-ai-fcb1e.firebaseapp.com",
        "projectId": "hiresense-ai-fcb1e",
        "storageBucket": "hiresense-ai-fcb1e.firebasestorage.app",
        "messagingSenderId": "305429336097",
        "appId": "1:305429336097:web:d3f703fba63c6e5e75d360",
        "measurementId": "G-W39QLGECW8"
    }
    
    # Use a service account or initialize with config
    try:
        cred = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(cred, {
            'storageBucket': firebase_config["storageBucket"]
        })
    except:
        # For development/demo purposes
        firebase_admin.initialize_app(options={
            'projectId': firebase_config["projectId"],
            'storageBucket': firebase_config["storageBucket"]
        })

# Import other modules after Firebase initialization
from utils.auth import check_auth, login_user, signup_user, logout_user
from utils.resume_analyzer import analyze_resume, verify_resume, extract_contact_info
from utils.ui_components import (
    render_navbar, render_footer, render_hero_section, 
    render_features_section, render_animated_pattern,
    render_testimonials, render_stats_counter, render_pricing_section,
    render_card, render_skill_badge, render_avatar, render_progress_bar,
    load_lottie_file, load_lottie_url, render_dashboard_visualization,
    render_tech_visualization
)

# Set page config
st.set_page_config(
    page_title="HireSense.AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
def load_css():
    with open("static/styles.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'user' not in st.session_state:
    st.session_state.user = None
if 'auth_status' not in st.session_state:
    st.session_state.auth_status = None
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'uploaded_resumes' not in st.session_state:
    st.session_state.uploaded_resumes = []
if 'verified_resumes' not in st.session_state:
    st.session_state.verified_resumes = []
if 'job_details' not in st.session_state:
    st.session_state.job_details = {
        'title': '',
        'description': '',
        'responsibilities': '',
        'skills': []
    }
if 'results' not in st.session_state:
    st.session_state.results = []
if 'selected_candidate' not in st.session_state:
    st.session_state.selected_candidate = None
if 'jobs' not in st.session_state:
    st.session_state.jobs = []
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'monthly_stats' not in st.session_state:
    # Generate mock monthly stats for dashboard
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    st.session_state.monthly_stats = {
        'applications': [random.randint(50, 200) for _ in range(12)],
        'interviews': [random.randint(10, 50) for _ in range(12)],
        'hires': [random.randint(1, 15) for _ in range(12)],
        'months': months
    }

# Navigation functions
def navigate_to(page):
    st.session_state.page = page
    # Reset specific page states when navigating
    if page == 'home':
        if 'uploaded_resumes' in st.session_state:
            st.session_state.uploaded_resumes = []
        if 'verified_resumes' in st.session_state:
            st.session_state.verified_resumes = []
        if 'job_details' in st.session_state:
            st.session_state.job_details = {
                'title': '',
                'description': '',
                'responsibilities': '',
                'skills': []
            }

# Toggle dark mode
def toggle_dark_mode():
    st.session_state.dark_mode = not st.session_state.dark_mode
    # Apply dark mode CSS
    if st.session_state.dark_mode:
        st.markdown("""
        <style>
        :root {
            --background-color: #121212;
            --text-color: #f0f0f0;
            --card-bg-color: #1e1e1e;
            --border-color: #333;
            --primary-color: #4f6df5;
            --secondary-color: #bb86fc;
        }
        body {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .card {
            background-color: var(--card-bg-color);
            border-color: var(--border-color);
        }
        .stApp {
            background-color: var(--background-color);
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <style>
        :root {
            --background-color: #ffffff;
            --text-color: #262730;
            --card-bg-color: #ffffff;
            --border-color: #e0e0e0;
            --primary-color: #0A21C0;
            --secondary-color: #4f6df5;
        }
        body {
            background-color: var(--background-color);
            color: var(--text-color);
        }
        .card {
            background-color: var(--card-bg-color);
            border-color: var(--border-color);
        }
        .stApp {
            background-color: var(--background-color);
        }
        </style>
        """, unsafe_allow_html=True)

# Main app structure
def main():
    # Render navbar
    render_navbar(toggle_dark_mode)
    
    # Route to the correct page
    if st.session_state.page == 'home':
        render_home_page()
    elif st.session_state.page == 'auth':
        render_auth_page()
    elif st.session_state.page == 'about':
        render_about_page()
    elif st.session_state.page == 'contact':
        render_contact_page()
    elif st.session_state.page == 'upload':
        if check_auth():
            render_upload_page()
        else:
            st.warning("Please sign in to access this page")
            navigate_to('auth')
    elif st.session_state.page == 'job_creation':
        if check_auth():
            render_job_creation_page()
        else:
            st.warning("Please sign in to access this page")
            navigate_to('auth')
    elif st.session_state.page == 'results':
        if check_auth():
            render_results_page()
        else:
            st.warning("Please sign in to access this page")
            navigate_to('auth')
    elif st.session_state.page == 'candidate_details':
        if check_auth():
            render_candidate_details_page()
        else:
            st.warning("Please sign in to access this page")
            navigate_to('auth')
    elif st.session_state.page == 'dashboard':
        if check_auth():
            render_dashboard_page()
        else:
            st.warning("Please sign in to access this page")
            navigate_to('auth')
    elif st.session_state.page == 'pricing':
        render_pricing_page()
    elif st.session_state.page == 'jobs':
        if check_auth():
            render_jobs_page()
        else:
            st.warning("Please sign in to access this page")
            navigate_to('auth')
    
    # Render footer
    render_footer()

# Page renderers
def render_home_page():
    # Hero section
    render_hero_section()
    
    # Stats counter
    render_stats_counter()
    
    # Animated pattern showcasing ranking parameters
    render_animated_pattern()
    
    # Features section
    render_features_section()
    
    # Testimonials
    render_testimonials()
    
    # Call to action
    st.markdown("---")
    st.header("Ready to Transform Your Hiring Process?")
    st.write("Join hundreds of companies using HireSense AI to find the best talent faster and more efficiently.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.session_state.user:
            if st.button("Upload Resumes", key="home_upload_btn", use_container_width=True):
                navigate_to('upload')
        else:
            if st.button("Get Started Free", key="home_get_started_btn", use_container_width=True):
                navigate_to('auth')
        
        if st.button("View Pricing", key="home_pricing_btn", use_container_width=True):
            navigate_to('pricing')

def render_auth_page():
    cols = st.columns([1, 2, 1])
    with cols[1]:
        render_card(
            title="Authentication",
            content=lambda: render_auth_content(),
            icon="🔐"
        )

def render_auth_content():
    # Create tabs for Sign In and Sign Up
    tab1, tab2 = st.tabs(["Sign In", "Sign Up"])
    
    with tab1:  # Sign In tab
        st.subheader("Sign in to your account")
        
        # Load Lottie animation
        lottie_url = "https://assets5.lottiefiles.com/packages/lf20_q5pk6p1k.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=200, key="signin_lottie")
        
        email = st.text_input("Email", key="signin_email")
        password = st.text_input("Password", type="password", key="signin_password")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Sign In", use_container_width=True):
                with st.spinner("Signing in..."):
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.session_state.auth_status = "success"
                        time.sleep(1)
                        navigate_to('dashboard')
                        st.rerun()
                    else:
                        st.error(message)
        
        with col2:
            if st.button("Sign In with Google", use_container_width=True):
                st.info("Google Sign In is not available in this demo. Please use email/password.")
    
    with tab2:  # Sign Up tab
        st.subheader("Create an account")
        
        # Load Lottie animation
        lottie_url = "https://assets9.lottiefiles.com/packages/lf20_kks3uigh.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=200, key="signup_lottie")
        
        email = st.text_input("Email", key="signup_email")
        phone = st.text_input("Phone Number (optional)", key="signup_phone")
        password = st.text_input("Password", type="password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm_password")
        
        if st.button("Sign Up", use_container_width=True):
            if password != confirm_password:
                st.error("Passwords do not match")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters long")
            else:
                with st.spinner("Creating account..."):
                    success, message = signup_user(email, password, phone)
                    if success:
                        st.success(message)
                        st.session_state.auth_status = "success"
                        time.sleep(1)
                        navigate_to('dashboard')
                        st.rerun()
                    else:
                        st.error(message)

def render_about_page():
    st.title("About HireSense AI")
    
    # Company mission with animation
    st.header("Our Mission")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        At HireSense AI, we're revolutionizing the hiring process by leveraging cutting-edge artificial
        intelligence to help recruiters find the perfect candidates for their positions. Our mission is to
        streamline the resume screening process, reduce bias in hiring, and help companies build diverse,
        talented teams more efficiently.
        """)
    
    with col2:
        # Load Lottie animation
        lottie_url = "https://assets3.lottiefiles.com/packages/lf20_kkflmtur.json"
        lottie_json = load_lottie_url(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, speed=1, height=200, key="mission_lottie")
    
    # Our Technology section
    st.header("Our Technology")
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("""
        HireSense AI uses advanced natural language processing and machine learning algorithms to analyze
        resumes and job descriptions. Our technology goes beyond simple keyword matching to understand the
        context, skills, and experience that make a candidate truly qualified for a position.
        """)
        
        st.markdown("""
        - Advanced resume parsing and analysis
        - Contextual understanding of job requirements
        - Bias-reducing algorithms for fair candidate evaluation
        - Customizable scoring parameters
        - Seamless integration with existing HR systems
        """)
    
    with col2:
        # Render tech visualization instead of static image
        render_tech_visualization()
    
    # Our Team section with improved styling
    st.header("Our Team")
    st.write("""
    HireSense AI was founded by a team of HR professionals, data scientists, and software engineers who
    recognized the challenges in traditional resume screening processes. With decades of combined experience
    in talent acquisition and artificial intelligence, our team is dedicated to creating solutions that make
    hiring more efficient and effective.
    """)
    
    # Team members with avatars
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_avatar("Alex Johnson", "CEO & Co-Founder", "https://randomuser.me/api/portraits/men/32.jpg")
        st.write("Former HR Director with 15+ years experience in talent acquisition")
    
    with col2:
        render_avatar("Dr. Sarah Chen", "CTO & Co-Founder", "https://randomuser.me/api/portraits/women/44.jpg")
        st.write("PhD in Machine Learning with expertise in NLP and AI systems")
    
    with col3:
        render_avatar("Michael Rodriguez", "Head of Product", "https://randomuser.me/api/portraits/men/67.jpg")
        st.write("Product leader with background in HR tech and SaaS platforms")
    
    # Our Values section with cards
    st.header("Our Values")
    col1, col2 = st.columns(2)
    
    with col1:
        render_card(
            title="Fairness & Inclusion",
            content=lambda: st.write("We're committed to reducing bias in hiring and helping companies build diverse teams."),
            icon="⚖️"
        )
        
        render_card(
            title="Innovation",
            content=lambda: st.write("We continuously improve our algorithms and features to stay at the cutting edge of AI technology."),
            icon="💡"
        )
    
    with col2:
        render_card(
            title="Privacy & Security",
            content=lambda: st.write("We maintain the highest standards of data protection and privacy for both recruiters and candidates."),
            icon="🔒"
        )
        
        render_card(
            title="Customer Success",
            content=lambda: st.write("We measure our success by the success of our customers in finding and hiring great talent."),
            icon="🚀"
        )

def render_contact_page():
    st.title("Contact Us")
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        render_card(
            title="Get in Touch",
            content=lambda: render_contact_form(),
            icon="✉️"
        )
    
    with col2:
        render_card(
            title="Contact Information",
            content=lambda: render_contact_info(),
            icon="📞"
        )

def render_contact_form():
    st.write("Fill out the form and our team will get back to you within 24 hours.")
    
    # Load Lottie animation
    lottie_url = "https://assets1.lottiefiles.com/packages/lf20_u8o7BL.json"
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=200, key="contact_lottie")
    
    contact_form = st.form("contact_form")
    with contact_form:
        name = st.text_input("Name")
        email = st.text_input("Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message", height=150)
        
        submitted = st.form_submit_button("Send Message")
        if submitted:
            if name and email and subject and message:
                with st.spinner("Sending message..."):
                    # Simulate API call
                    time.sleep(1.5)
                    st.success("Message sent successfully! We'll get back to you soon.")
            else:
                st.error("Please fill in all fields")

def render_contact_info():
    st.subheader("Email")
    st.write("contact@hiresense.ai")
    st.write("support@hiresense.ai")
    
    st.subheader("Phone")
    st.write("+1 (555) 123-4567")
    st.write("+1 (555) 987-6543")
    
    st.subheader("Office")
    st.write("""
    123 Innovation Drive
    Suite 400
    San Francisco, CA 94107
    """)
    
    st.subheader("Business Hours")
    st.write("Monday - Friday: 9:00 AM - 6:00 PM PST")
    st.write("Saturday: 10:00 AM - 4:00 PM PST")
    st.write("Sunday: Closed")
    
    st.subheader("Connect With Us")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.button("Facebook", key="fb_btn")
    with col2:
        st.button("Twitter", key="tw_btn")
    with col3:
        st.button("LinkedIn", key="li_btn")
    with col4:
        st.button("Instagram", key="ig_btn")

def render_upload_page():
    st.title("Upload Resumes")
    
    # Create tabs for the upload process
    tab1, tab2 = st.tabs(["Upload Resumes", "Create Job"])
    
    with tab1:
        render_card(
            title="Upload and Verify Resumes",
            content=lambda: render_upload_content(),
            icon="📄"
        )
    
    with tab2:
        render_card(
            title="Create Job",
            content=lambda: render_job_creation_content(),
            icon="💼"
        )

def render_upload_content():
    st.write("Upload the resumes you want to screen. We accept PDF files only.")
    
    # Load Lottie animation
    lottie_url = "https://assets9.lottiefiles.com/packages/lf20_vvbgxrn3.json"
    lottie_json = load_lottie_url(lottie_url)
    if lottie_json:
        st_lottie(lottie_json, speed=1, height=200, key="upload_lottie")
    
    # File uploader
    uploaded_files = st.file_uploader(
        "Drag and drop your resumes here",
        type=["pdf"],
        accept_multiple_files=True,
        key="resume_uploader"
    )
    
    if uploaded_files:
        st.session_state.uploaded_resumes = uploaded_files
        st.success(f"{len(uploaded_files)} resumes uploaded successfully")
        
        # Display uploaded files
        st.subheader("Uploaded Resumes")
        for i, file in enumerate(uploaded_files):
            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.write(f"{i+1}. {file.name}")
            with col2:
                st.write(f"{round(file.size/1024, 2)} KB")
            with col3:
                if st.button("Remove", key=f"remove_{i}"):
                    st.session_state.uploaded_resumes.pop(i)
                    st.rerun()
        
        # Verify resumes button
        if st.button("Verify Resumes", use_container_width=True):
            with st.spinner("Verifying resumes..."):
                progress_bar = st.progress(0)
                verified_resumes = []
                verification_stats = {"total": len(uploaded_files), "verified": 0, "suspicious": 0}
                
                for i, file in enumerate(uploaded_files):
                    # Simulate verification process
                    result = verify_resume(file)
                    verified_file = {
                        "file": file,
                        "name": file.name,
                        "size": file.size,
                        "verified": True,
                        "suspicious": result["suspicious"],
                        "verification_message": result["message"]
                    }
                    verified_resumes.append(verified_file)
                    
                    if result["suspicious"]:
                        verification_stats["suspicious"] += 1
                    else:
                        verification_stats["verified"] += 1
                    
                    # Update progress
                    progress = (i + 1) / len(uploaded_files)
                    progress_bar.progress(progress)
                    time.sleep(0.1)  # Simulate processing time
                
                st.session_state.verified_resumes = verified_resumes
                
                # Display verification stats
                st.success(f"Verification complete: {verification_stats['verified']} verified, {verification_stats['suspicious']} suspicious")
                
                # Display verified resumes
                st.subheader("Verification Results")
                for i, file in enumerate(verified_resumes):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"{i+1}. {file['name']}")
                    with col2:
                        if file["suspicious"]:
                            st.warning("⚠️ Suspicious")
                        else:
                            st.success("✓ Verified")
                    with col3:
                        if st.button("Details", key=f"details_{i}"):
                            st.info(file["verification_message"])
                
                # Next step button
                if st.button("Proceed to Job Creation", use_container_width=True):
                    tab2.active = True

def render_job_creation_content():
    st.write("Define the job position to match with the uploaded resumes.")
    
    # Check if resumes have been verified
    if not st.session_state.verified_resumes:
        st.warning("Please upload and verify resumes first")
    else:
        # Job details form
        job_title = st.text_input("Job Title", key="job_title", value=st.session_state.job_details.get('title', ''))
        job_description = st.text_area("Job Description", key="job_description", height=150, value=st.session_state.job_details.get('description', ''))
        job_responsibilities = st.text_area("Responsibilities", key="job_responsibilities", height=100, value=st.session_state.job_details.get('responsibilities', ''))
        job_skills = st.text_input("Required Skills (comma separated)", key="job_skills", value=",".join(st.session_state.job_details.get('skills', [])))
        
        # Additional job details
        col1, col2 = st.columns(2)
        with col1:
            job_location = st.text_input("Location", key="job_location", value=st.session_state.job_details.get('location', ''))
            job_type = st.selectbox("Job Type", ["Full-time", "Part-time", "Contract", "Internship"], key="job_type")
        
        with col2:
            job_salary = st.text_input("Salary Range (optional)", key="job_salary", value=st.session_state.job_details.get('salary', ''))
            job_deadline = st.date_input("Application Deadline", key="job_deadline")
        
        # Save job details
        if st.button("Process Resumes", use_container_width=True):
            if not job_title or not job_description:
                st.error("Please fill in all required fields")
            else:
                with st.spinner("Processing resumes..."):
                    # Save job details to session state
                    st.session_state.job_details = {
                        'title': job_title,
                        'description': job_description,
                        'responsibilities': job_responsibilities,
                        'skills': [skill.strip() for skill in job_skills.split(',') if skill.strip()],
                        'location': job_location,
                        'type': job_type,
                        'salary': job_salary,
                        'deadline': job_deadline.strftime("%Y-%m-%d"),
                        'created_at': datetime.now().strftime("%Y-%m-%d"),
                        'status': 'Active'
                    }
                    
                    # Add job to jobs list
                    job_id = str(uuid.uuid4())
                    job = {
                        'id': job_id,
                        **st.session_state.job_details
                    }
                    st.session_state.jobs.append(job)
                    
                    # Process resumes (simulate)
                    progress_bar = st.progress(0)
                    for i in range(100):
                        time.sleep(0.03)  # Simulate processing time
                        progress_bar.progress(i + 1)
                    
                    # Generate mock results
                    st.session_state.results = generate_mock_results(
                        st.session_state.verified_resumes,
                        st.session_state.job_details
                    )
                    
                    st.success("Resumes processed successfully!")
                    time.sleep(1)
                    navigate_to('results')
                    st.rerun()

def render_job_creation_page():
    st.title("Create Job")
    
    # Check if resumes have been uploaded
    if not st.session_state.verified_resumes:
        st.warning("Please upload and verify resumes first")
        if st.button("Go to Upload Page"):
            navigate_to('upload')
            st.rerun()
        return
    
    render_card(
        title="Job Details",
        content=lambda: render_job_creation_content(),
        icon="💼"
    )

def render_results_page():
    st.title("Resume Ranking & Leaderboard")
    
    # Check if results exist
    if not st.session_state.results:
        st.warning("No results found. Please upload resumes and create a job first.")
        if st.button("Go to Upload Page"):
            navigate_to('upload')
            st.rerun()
        return
    
    # Display job details
    with st.expander("Job Details", expanded=True):
        st.subheader(st.session_state.job_details.get('title', 'Job Title'))
        st.write(st.session_state.job_details.get('description', ''))
        
        if st.session_state.job_details.get('skills'):
            st.write("**Required Skills:**")
            skills_cols = st.columns(min(5, len(st.session_state.job_details.get('skills', []))))
            for i, skill in enumerate(st.session_state.job_details.get('skills', [])[:5]):
                with skills_cols[i % 5]:
                    render_skill_badge(skill)
            
            if len(st.session_state.job_details.get('skills', [])) > 5:
                st.write(f"And {len(st.session_state.job_details.get('skills', [])) - 5} more skills")
    
    # Top 3 candidates with animations
    st.header("Top Candidates")
    
    # Sort results by score
    sorted_results = sorted(st.session_state.results, key=lambda x: x['score'], reverse=True)
    top_candidates = sorted_results[:3]
    
    # Display top 3 candidates
    top_cols = st.columns(3)
    medal_colors = ["gold", "silver", "#cd7f32"]  # Gold, Silver, Bronze
    medal_emojis = ["🥇", "🥈", "🥉"]
    
    for i, candidate in enumerate(top_candidates):
        with top_cols[i]:
            st.markdown(f"<h3 style='text-align: center; color: {medal_colors[i]};'>{medal_emojis[i]} {candidate['name']}</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='text-align: center;'>Score: {candidate['score']}%</p>", unsafe_allow_html=True)
            
            # Display candidate card
            with st.container():
                st.markdown(f"""
                <div style='border: 2px solid {medal_colors[i]}; border-radius: 10px; padding: 10px; text-align: center;'>
                    <p><strong>Email:</strong> {candidate['email']}</p>
                    <p><strong>Phone:</strong> {candidate['phone']}</p>
                    <p><strong>Experience:</strong> {candidate['experience']} years</p>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("View Details", key=f"view_{i}", use_container_width=True):
                    st.session_state.selected_candidate = candidate
                    navigate_to('candidate_details')
                    st.rerun()
    
    # Visualization of candidate scores
    st.header("Candidate Score Distribution")
    
    # Create a bar chart of all candidates
    chart_data = pd.DataFrame({
        'Candidate': [r['name'] for r in sorted_results],
        'Score': [r['score'] for r in sorted_results]
    })
    
    fig = px.bar(
        chart_data, 
        x='Candidate', 
        y='Score',
        color='Score',
        color_continuous_scale='blues',
        labels={'Score': 'Match Score (%)'},
        title='Candidate Match Scores'
    )
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Complete list of all ranked resumes
    st.header("All Candidates")
    
    # Search and filter
    col1, col2 = st.columns([3, 1])
    with col1:
        search_term = st.text_input("Search candidates", key="search_candidates")
    with col2:
        show_suspicious = st.checkbox("Show Suspicious", value=True, key="show_suspicious")
    
    # Filter results
    filtered_results = sorted_results
    if search_term:
        filtered_results = [r for r in filtered_results if search_term.lower() in r['name'].lower()]
    if not show_suspicious:
        filtered_results = [r for r in filtered_results if not r.get('suspicious', False)]
    
    # Display results in a table
    if filtered_results:
        result_df = pd.DataFrame(filtered_results)
        result_df = result_df[['name', 'score', 'experience', 'education', 'suspicious']]
        result_df.columns = ['Name', 'Score (%)', 'Experience (years)', 'Education', 'Suspicious']
        
        # Add view details button
        st.dataframe(result_df, use_container_width=True)
        
        # Select candidate to view details
        selected_name = st.selectbox("Select a candidate to view details", [r['name'] for r in filtered_results])
        selected_candidate = next((r for r in filtered_results if r['name'] == selected_name), None)
        
        if selected_candidate and st.button("View Candidate Details", use_container_width=True):
            st.session_state.selected_candidate = selected_candidate
            navigate_to('candidate_details')
            st.rerun()
    else:
        st.info("No candidates match your search criteria")

def render_candidate_details_page():
    # Check if a candidate is selected
    if not st.session_state.selected_candidate:
        st.warning("No candidate selected")
        if st.button("Back to Results"):
            navigate_to('results')
            st.rerun()
        return
    
    candidate = st.session_state.selected_candidate
    
    # Back button
    if st.button("← Back to Results"):
        navigate_to('results')
        st.rerun()
    
    # Candidate header
    st.title(candidate['name'])
    
    # Warning if suspicious
    if candidate.get('suspicious', False):
        st.warning(f"⚠️ Suspicious Resume: {candidate.get('verification_message', 'This resume has been flagged as potentially suspicious.')}")
    
    # Main content
    col1, col2 = st.columns([1, 1])
    
    with col1:
        render_card(
            title="Candidate Details",
            content=lambda: render_candidate_details(candidate),
            icon="👤"
        )
    
    with col2:
        render_card(
            title="Resume",
            content=lambda: render_candidate_resume(candidate),
            icon="📄"
        )
        
        render_card(
            title="Contact Options",
            content=lambda: render_contact_options(candidate),
            icon="📞"
        )

def render_candidate_details(candidate):
    # Score with progress bar
    st.subheader("Match Score")
    render_progress_bar(candidate['score'], "match_score")
    
    # Basic info
    st.subheader("Contact Information")
    st.write(f"**Email:** {candidate['email']}")
    st.write(f"**Phone:** {candidate['phone']}")
    
    # Experience and education
    st.subheader("Experience & Education")
    st.write(f"**Experience:** {candidate['experience']} years")
    st.write(f"**Education:** {candidate['education']}")
    
    # Skills
    st.subheader("Skills")
    skills_cols = st.columns(min(5, len(candidate['skills'])))
    for i, skill in enumerate(candidate['skills'][:5]):
        with skills_cols[i % 5]:
            render_skill_badge(skill)
    
    if len(candidate['skills']) > 5:
        st.write(f"And {len(candidate['skills']) - 5} more skills")
    
    # Personality assessment
    st.subheader("Personality Assessment")
    st.write(candidate.get('personality_assessment', 'Candidate shows strong analytical skills and teamwork capabilities.'))
    
    # Skill match visualization
    st.subheader("Skill Match")
    
    # Create radar chart for skills
    job_skills = st.session_state.job_details.get('skills', [])
    if job_skills:
        # Find common skills
        common_skills = [skill for skill in candidate['skills'] if skill in job_skills]
        missing_skills = [skill for skill in job_skills if skill not in candidate['skills']]
        
        # Create data for radar chart
        categories = job_skills
        values = [100 if skill in common_skills else 0 for skill in categories]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='Skill Match',
            line=dict(color='#0A21C0')
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display missing skills
        if missing_skills:
            st.subheader("Missing Skills")
            for skill in missing_skills:
                st.write(f"- {skill}")

def render_candidate_resume(candidate):
    # Display mock resume
    st.info("Resume preview would be displayed here in a real implementation")
    
    # Mock resume content
    st.markdown(f"""
    ### {candidate['name']}
    {candidate['email']} | {candidate['phone']}
    
    #### Summary
    Experienced professional with {candidate['experience']} years in the industry.
    
    #### Skills
    {', '.join(candidate['skills'])}
    
    #### Education
    {candidate['education']}
    
    #### Experience
    - Senior Position, Company A (2018-Present)
    - Junior Position, Company B (2015-2018)
    """)
    
    # Download resume button
    if st.button("Download Resume", use_container_width=True):
        # In a real implementation, this would generate a download link
        st.info("In a real implementation, this would download the candidate's resume")

def render_contact_options(candidate):
    # Send SMS
    with st.expander("Send SMS"):
        sms_message = st.text_area("Message", height=100, placeholder=f"Enter your message to {candidate['name']}...")
        if st.button("Send SMS", use_container_width=True):
            if sms_message:
                with st.spinner("Sending SMS..."):
                    # Simulate sending SMS
                    time.sleep(1.5)
                    st.success(f"SMS sent to {candidate['name']} successfully!")
            else:
                st.error("Please enter a message")
    
    # Schedule interview
    with st.expander("Schedule Interview"):
        interview_date = st.date_input("Interview Date", value=datetime.now() + timedelta(days=3))
        interview_time = st.time_input("Interview Time", value=datetime.now().replace(hour=10, minute=0))
        interview_duration = st.number_input("Duration (minutes)", min_value=15, max_value=120, value=60, step=15)
        
        if st.button("Schedule Interview", use_container_width=True):
            with st.spinner("Scheduling interview..."):
                # Simulate scheduling
                time.sleep(1.5)
                meet_link = f"https://meet.google.com/{uuid.uuid4().hex[:8]}"
                st.success(f"Interview scheduled with {candidate['name']} successfully!")
                st.markdown(f"**Google Meet Link:** [{meet_link}]({meet_link})")
    
    # Select candidate
    if st.button("Select This Candidate", use_container_width=True):
        with st.spinner("Processing selection..."):
            # Simulate processing
            time.sleep(1.5)
            st.success(f"{candidate['name']} has been selected for the position!")
            st.info("An interview invitation has been automatically sent and the job listing has been closed.")
            
            # Option to go back to results
            if st.button("Back to Results"):
                navigate_to('results')
                st.rerun()

def render_dashboard_page():
    st.title("Recruiter Dashboard")
    
    # Welcome message
    st.write(f"Welcome back, {st.session_state.user.get('displayName', 'User')}!")
    
    # Dashboard stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        render_card(
            title="Active Jobs",
            content=lambda: st.markdown(f"<h1 style='text-align: center;'>{len([j for j in st.session_state.jobs if j.get('status') == 'Active'])}</h1>", unsafe_allow_html=True),
            icon="💼"
        )
    
    with col2:
        render_card(
            title="Candidates",
            content=lambda: st.markdown(f"<h1 style='text-align: center;'>{len(st.session_state.results)}</h1>", unsafe_allow_html=True),
            icon="👥"
        )
    
    with col3:
        render_card(
            title="Interviews",
            content=lambda: st.markdown("<h1 style='text-align: center;'>3</h1>", unsafe_allow_html=True),
            icon="📅"
        )
    
    with col4:
        render_card(
            title="Hires",
            content=lambda: st.markdown("<h1 style='text-align: center;'>1</h1>", unsafe_allow_html=True),
            icon="🎯"
        )
    
    # Dashboard visualization
    st.header("Recruitment Analytics")
    render_dashboard_visualization()
    
    # Recent activity
    st.header("Recent Activity")
    
    # Create tabs for different activities
    tab1, tab2, tab3 = st.tabs(["Recent Jobs", "Recent Candidates", "Upcoming Interviews"])
    
    with tab1:
        if st.session_state.jobs:
            for job in st.session_state.jobs[:3]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{job.get('title')}**")
                    st.write(f"Created on {job.get('created_at')}")
                with col2:
                    st.write(f"Status: {job.get('status')}")
                    if st.button("View", key=f"view_job_{job.get('id')}", use_container_width=True):
                        # Set the selected job and navigate to results
                        st.session_state.job_details = job
                        navigate_to('results')
                        st.rerun()
                st.markdown("---")
        else:
            st.info("No jobs created yet. Create your first job to get started.")
            if st.button("Create Job", use_container_width=True):
                navigate_to('upload')
                st.rerun()
    
    with tab2:
        if st.session_state.results:
            for candidate in st.session_state.results[:3]:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{candidate.get('name')}**")
                    st.write(f"{candidate.get('education')} | {candidate.get('experience')} years experience")
                with col2:
                    st.write(f"Score: {candidate.get('score')}%")
                    if st.button("View", key=f"view_candidate_{candidate.get('name')}", use_container_width=True):
                        # Set the selected candidate and navigate to details
                        st.session_state.selected_candidate = candidate
                        navigate_to('candidate_details')
                        st.rerun()
                st.markdown("---")
        else:
            st.info("No candidates analyzed yet. Upload resumes to get started.")
            if st.button("Upload Resumes", use_container_width=True):
                navigate_to('upload')
                st.rerun()
    
    with tab3:
        # Mock upcoming interviews
        interviews = [
            {"candidate": "John Smith", "date": "2023-06-15", "time": "10:00 AM", "position": "Senior Developer"},
            {"candidate": "Emily Johnson", "date": "2023-06-16", "time": "2:30 PM", "position": "UX Designer"},
            {"candidate": "Michael Chen", "date": "2023-06-17", "time": "11:15 AM", "position": "Data Scientist"}
        ]
        
        for interview in interviews:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"**{interview.get('candidate')}**")
                st.write(f"{interview.get('position')} | {interview.get('date')} at {interview.get('time')}")
            with col2:
                if st.button("Join", key=f"join_interview_{interview.get('candidate')}", use_container_width=True):
                    st.markdown(f"[Join Google Meet](https://meet.google.com/{uuid.uuid4().hex[:8]})")
            st.markdown("---")
    
    # Quick actions
    st.header("Quick Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Upload Resumes", key="dashboard_upload", use_container_width=True):
            navigate_to('upload')
            st.rerun()
    
    with col2:
        if st.button("View All Jobs", key="dashboard_jobs", use_container_width=True):
            navigate_to('jobs')
            st.rerun()
    
    with col3:
        if st.button("Create New Job", key="dashboard_create_job", use_container_width=True):
            navigate_to('job_creation')
            st.rerun()

def render_pricing_page():
    st.title("Pricing Plans")
    
    st.write("Choose the plan that fits your hiring needs")
    
    # Render pricing section
    render_pricing_section()
    
    # FAQ section
    st.header("Frequently Asked Questions")
    
    with st.expander("What's included in the free trial?"):
        st.write("The free trial includes all features of the Pro plan for 14 days, with a limit of 50 resume analyses.")
    
    with st.expander("Can I upgrade or downgrade my plan?"):
        st.write("Yes, you can upgrade or downgrade your plan at any time. Changes will take effect at the start of your next billing cycle.")
    
    with st.expander("Do you offer custom enterprise solutions?"):
        st.write("Yes, our Enterprise plan can be customized to meet your organization's specific needs. Contact our sales team for more information.")
    
    with st.expander("How does billing work?"):
        st.write("We offer monthly and annual billing options. Annual plans come with a 20% discount compared to monthly billing.")
    
    with st.expander("What payment methods do you accept?"):
        st.write("We accept all major credit cards, PayPal, and bank transfers for Enterprise plans.")
    
    # Call to action
    st.markdown("---")
    st.header("Ready to Transform Your Hiring Process?")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Start Free Trial", key="pricing_trial_btn", use_container_width=True):
            navigate_to('auth')
            st.rerun()
    
    with col2:
        if st.button("Contact Sales", key="pricing_contact_btn", use_container_width=True):
            navigate_to('contact')
            st.rerun()

def render_jobs_page():
    st.title("Manage Jobs")
    
    # Create a new job button
    if st.button("Create New Job", key="create_new_job_btn"):
        navigate_to('upload')
        st.rerun()
    
    # Tabs for different job statuses
    tab1, tab2, tab3 = st.tabs(["Active Jobs", "Draft Jobs", "Closed Jobs"])
    
    with tab1:
        active_jobs = [j for j in st.session_state.jobs if j.get('status') == 'Active']
        if active_jobs:
            for job in active_jobs:
                render_job_card(job)
        else:
            st.info("No active jobs found.")
    
    with tab2:
        draft_jobs = [j for j in st.session_state.jobs if j.get('status') == 'Draft']
        if draft_jobs:
            for job in draft_jobs:
                render_job_card(job)
        else:
            st.info("No draft jobs found.")
    
    with tab3:
        closed_jobs = [j for j in st.session_state.jobs if j.get('status') == 'Closed']
        if closed_jobs:
            for job in closed_jobs:
                render_job_card(job)
        else:
            st.info("No closed jobs found.")

def render_job_card(job):
    with st.container():
        st.markdown(f"""
        <div style='border: 1px solid var(--border-color, #e0e0e0); border-radius: 10px; padding: 15px; margin-bottom: 15px;'>
            <h3>{job.get('title')}</h3>
            <p><strong>Location:</strong> {job.get('location', 'Remote')}</p>
            <p><strong>Type:</strong> {job.get('type', 'Full-time')}</p>
            <p><strong>Created:</strong> {job.get('created_at')}</p>
            <p><strong>Status:</strong> {job.get('status')}</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("View Candidates", key=f"view_candidates_{job.get('id')}", use_container_width=True):
                st.session_state.job_details = job
                navigate_to('results')
                st.rerun()
        
        with col2:
            if st.button("Edit Job", key=f"edit_job_{job.get('id')}", use_container_width=True):
                st.session_state.job_details = job
                navigate_to('job_creation')
                st.rerun()
        
        with col3:
            if job.get('status') == 'Active':
                if st.button("Close Job", key=f"close_job_{job.get('id')}", use_container_width=True):
                    # Update job status
                    for j in st.session_state.jobs:
                        if j.get('id') == job.get('id'):
                            j['status'] = 'Closed'
                    st.success(f"Job '{job.get('title')}' has been closed.")
                    st.rerun()
            elif job.get('status') == 'Closed':
                if st.button("Reopen Job", key=f"reopen_job_{job.get('id')}", use_container_width=True):
                    # Update job status
                    for j in st.session_state.jobs:
                        if j.get('id') == job.get('id'):
                            j['status'] = 'Active'
                    st.success(f"Job '{job.get('title')}' has been reopened.")
                    st.rerun()

# Helper function to generate mock results
def generate_mock_results(verified_resumes, job_details):
    # Mock candidate data
    mock_candidates = [
        {
            "name": "John Smith",
            "email": "john.smith@example.com",
            "phone": "+1 (555) 123-4567",
            "score": 92,
            "skills": ["React", "TypeScript", "Node.js", "Python", "AWS"],
            "experience": 5,
            "education": "Master's in Computer Science",
            "suspicious": False,
            "verification_message": "Resume verified successfully",
            "personality_assessment": "Strong analytical skills with excellent teamwork capabilities.",
            "ats_score": 90
        },
        {
            "name": "Emily Johnson",
            "email": "emily.johnson@example.com",
            "phone": "+1 (555) 987-6543",
            "score": 88,
            "skills": ["JavaScript", "React", "CSS", "UI/UX", "Figma"],
            "experience": 3,
            "education": "Bachelor's in Web Development",
            "suspicious": False,
            "verification_message": "Resume verified successfully",
            "personality_assessment": "Creative problem-solver with strong communication skills.",
            "ats_score": 85
        },
        {
            "name": "Michael Chen",
            "email": "michael.chen@example.com",
            "phone": "+1 (555) 456-7890",
            "score": 85,
            "skills": ["Java", "Spring", "SQL", "Docker", "Kubernetes"],
            "experience": 7,
            "education": "PhD in Computer Engineering",
            "suspicious": True,
            "verification_message": "Inconsistent employment dates detected (85% confidence)",
            "personality_assessment": "Detail-oriented with strong leadership potential.",
            "ats_score": 78
        },
        {
            "name": "Sarah Williams",
            "email": "sarah.williams@example.com",
            "phone": "+1 (555) 234-5678",
            "score": 79,
            "skills": ["Python", "Django", "Flask", "Machine Learning", "Data Analysis"],
            "experience": 4,
            "education": "Bachelor's in Data Science",
            "suspicious": False,
            "verification_message": "Resume verified successfully",
            "personality_assessment": "Analytical thinker with strong problem-solving abilities.",
            "ats_score": 82
        },
        {
            "name": "David Rodriguez",
            "email": "david.rodriguez@example.com",
            "phone": "+1 (555) 876-5432",
            "score": 76,
            "skills": ["C#", ".NET", "Azure", "SQL Server", "Angular"],
            "experience": 6,
            "education": "Master's in Software Engineering",
            "suspicious": False,
            "verification_message": "Resume verified successfully",
            "personality_assessment": "Methodical worker with excellent attention to detail.",
            "ats_score": 75
        }
    ]
    
    # Add more mock candidates based on uploaded resumes
    for i, resume in enumerate(verified_resumes):
        if i >= len(mock_candidates):  # Only add if we need more candidates
            # Generate random data
            name_parts = resume["name"].split(".")
            if len(name_parts) > 1:
                name = name_parts[0].capitalize() + " " + "".join([c for c in name_parts[1] if c.isalpha()]).capitalize()
            else:
                name = resume["name"].split(".")[0].capitalize() + " " + random.choice(["Anderson", "Brown", "Clark", "Davis", "Evans"])
            
            # Generate random skills based on job details
            all_skills = ["Python", "JavaScript", "Java", "C++", "C#", "React", "Angular", "Vue", "Node.js", 
                         "Django", "Flask", "Spring", "SQL", "NoSQL", "AWS", "Azure", "GCP", "Docker", 
                         "Kubernetes", "CI/CD", "Git", "Agile", "Scrum", "TDD", "DevOps"]
            job_skills = job_details.get('skills', [])
            
            # Include some job skills and some random skills
            candidate_skills = []
            for skill in job_skills:
                if random.random() > 0.3:  # 70% chance to include each job skill
                    candidate_skills.append(skill)
            
            # Add some random skills
            remaining_skills = [s for s in all_skills if s not in candidate_skills]
            candidate_skills.extend(random.sample(remaining_skills, min(5, len(remaining_skills))))
            
            # Calculate score based on skill match
            skill_match_score = sum(1 for skill in candidate_skills if skill in job_skills)
            skill_match_percentage = min(100, max(50, (skill_match_score / max(1, len(job_skills))) * 100))
            
            # Random experience and education
            experience = random.randint(1, 10)
            education_options = ["Bachelor's in Computer Science", "Master's in IT", "PhD in Data Science", 
                                "Bachelor's in Engineering", "Master's in Computer Engineering"]
            education = random.choice(education_options)
            
            # Create candidate
            candidate = {
                "name": name,
                "email": name.lower().replace(" ", ".") + "@example.com",
                "phone": f"+1 (555) {random.randint(100, 999)}-{random.randint(1000, 9999)}",
                "score": int(skill_match_percentage),
                "skills": candidate_skills,
                "experience": experience,
                "education": education,
                "suspicious": resume.get("suspicious", False),
                "verification_message": resume.get("verification_message", "Resume verified successfully"),
                "personality_assessment": random.choice([
                    "Strong analytical skills with excellent teamwork capabilities.",
                    "Creative problem-solver with strong communication skills.",
                    "Detail-oriented with strong leadership potential.",
                    "Analytical thinker with strong problem-solving abilities.",
                    "Methodical worker with excellent attention to detail."
                ]),
                "ats_score": random.randint(65, 95)
            }
            
            mock_candidates.append(candidate)
    
    return mock_candidates

# Run the app
if __name__ == "__main__":
    main()

