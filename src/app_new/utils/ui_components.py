import streamlit as st
import time
import random
from datetime import datetime
import requests
import json
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def render_navbar(toggle_dark_mode_callback=None):
    """Render the navigation bar"""
    # Create columns for the navbar
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("<h2 style='text-align: left;'>HireSense.AI</h2>", unsafe_allow_html=True)
    
    with col2:
        # Center navigation links
        nav_cols = st.columns(5)
        with nav_cols[0]:
            if st.button("Home", use_container_width=True):
                st.session_state.page = 'home'
                st.rerun()
        with nav_cols[1]:
            if st.button("About", use_container_width=True):
                st.session_state.page = 'about'
                st.rerun()
        with nav_cols[2]:
            if st.button("Pricing", use_container_width=True):
                st.session_state.page = 'pricing'
                st.rerun()
        with nav_cols[3]:
            if st.button("Contact", use_container_width=True):
                st.session_state.page = 'contact'
                st.rerun()
        with nav_cols[4]:
            if st.session_state.user:
                if st.button("Dashboard", use_container_width=True):
                    st.session_state.page = 'dashboard'
                    st.rerun()
    
    with col3:
        # Right-aligned auth buttons and dark mode toggle
        if st.session_state.user:
            cols = st.columns([3, 1])
            with cols[0]:
                if st.button("Logout", key="navbar_logout"):
                    from utils.auth import logout_user
                    logout_user()
                    st.session_state.page = 'home'
                    st.rerun()
            with cols[1]:
                if toggle_dark_mode_callback and st.button("🌙" if not st.session_state.dark_mode else "☀️", key="dark_mode_toggle"):
                    toggle_dark_mode_callback()
        else:
            cols = st.columns([3, 1])
            with cols[0]:
                if st.button("Sign In", key="navbar_signin"):
                    st.session_state.page = 'auth'
                    st.rerun()
            with cols[1]:
                if toggle_dark_mode_callback and st.button("🌙" if not st.session_state.dark_mode else "☀️", key="dark_mode_toggle"):
                    toggle_dark_mode_callback()
    
    st.markdown("---")

def render_footer():
    """Render the footer"""
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.markdown("© 2023 HireSense.AI")
    
    with col2:
        st.markdown("<div style='text-align: center;'>Privacy Policy | Terms of Service | Contact Us</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("<div style='text-align: right;'>Made with ❤️ by HireSense Team</div>", unsafe_allow_html=True)

def render_hero_section():
    """Render the hero section of the landing page"""
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("<h1 style='font-size: 2.5rem;'>AI-Powered Resume Screening for Modern Recruiters</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem;'>HireSense AI helps you find the perfect candidates faster by automatically analyzing resumes and matching them to your job requirements.</p>", unsafe_allow_html=True)
        
        button_cols = st.columns(2)
        with button_cols[0]:
            if st.session_state.user:
                if st.button("Upload Resumes", key="hero_upload", use_container_width=True):
                    st.session_state.page = 'upload'
                    st.rerun()
            else:
                if st.button("Get Started", key="hero_get_started", use_container_width=True):
                    st.session_state.page = 'auth'
                    st.rerun()
        
        with button_cols[1]:
            if st.button("Learn More", key="hero_learn_more", use_container_width=True):
                st.session_state.page = 'about'
                st.rerun()
    
    with col2:
        # Display a dashboard visualization instead of static image
        render_dashboard_visualization(is_hero=True)

def render_features_section():
    """Render the features section of the landing page"""
    st.header("How HireSense AI Works")
    st.write("Our AI-powered platform streamlines your recruitment process from resume collection to candidate selection.")
    
    # Create three columns for features
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_card(
            title="Upload Resumes",
            content=lambda: st.write("Upload multiple resumes and provide your job description to start the screening process."),
            icon="📄"
        )
    
    with col2:
        render_card(
            title="AI Analysis",
            content=lambda: st.write("Our AI analyzes each resume against your job requirements and ranks candidates by match score."),
            icon="🤖"
        )
    
    with col3:
        render_card(
            title="Review Top Candidates",
            content=lambda: st.write("Review ranked candidates, see detailed profiles, and access contact information."),
            icon="👥"
        )
    
    # Second row of features
    col4, col5, col6 = st.columns(3)
    
    with col4:
        render_card(
            title="Schedule Interviews",
            content=lambda: st.write("Schedule interviews with top candidates directly through our Google Meet integration."),
            icon="📅"
        )
    
    with col5:
        render_card(
            title="Contact Candidates",
            content=lambda: st.write("Send SMS messages to candidates to inform them about next steps in the hiring process."),
            icon="💬"
        )
    
    with col6:
        render_card(
            title="Make Better Hires",
            content=lambda: st.write("Make data-driven hiring decisions and build stronger teams with qualified candidates."),
            icon="✅"
        )

def render_animated_pattern():
    """Render an animated pattern showcasing ranking parameters"""
    st.subheader("Our AI Evaluates Resumes Based On:")
    
    # Create columns for parameters
    cols = st.columns(5)
    
    parameters = [
        {"name": "Skills Match", "weight": "40%", "description": "How well the candidate's skills match the job requirements"},
        {"name": "Experience", "weight": "25%", "description": "Relevant work experience and years in the industry"},
        {"name": "Education", "weight": "15%", "description": "Educational background and qualifications"},
        {"name": "Achievements", "weight": "10%", "description": "Notable accomplishments and certifications"},
        {"name": "Cultural Fit", "weight": "10%", "description": "Potential fit with company culture and values"}
    ]
    
    for i, param in enumerate(parameters):
        with cols[i]:
            st.metric(label=param["name"], value=param["weight"])
            st.caption(param["description"])
    
    # Add a progress bar to simulate animation
    if "animation_progress" not in st.session_state:
        st.session_state.animation_progress = 0
        st.session_state.animation_direction = 1
    
    # Update progress for animation effect
    progress = st.progress(st.session_state.animation_progress)
    
    # This will create a subtle animation effect when the page loads
    if st.session_state.animation_progress >= 1.0:
        st.session_state.animation_direction = -0.01
    elif st.session_state.animation_progress <= 0:
        st.session_state.animation_direction = 0.01
    
    st.session_state.animation_progress += st.session_state.animation_direction

def render_card(title, content, icon=None):
    """Render a card with title, content, and optional icon"""
    with st.container():
        st.markdown(f"""
        <div style='border: 1px solid var(--border-color, #e0e0e0); 
                    border-radius: 10px; 
                    padding: 20px; 
                    margin-bottom: 20px;
                    background-color: var(--card-bg-color, white);'>
            <h3>{icon + " " if icon else ""}{title}</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Call the content function to render the content
        content()

def render_skill_badge(skill):
    """Render a skill badge"""
    st.markdown(f"""
    <div style='display: inline-block; 
                background-color: var(--primary-color, #0A21C0); 
                color: white; 
                padding: 5px 10px; 
                border-radius: 15px; 
                margin-right: 5px;
                margin-bottom: 5px;
                font-size: 0.8rem;'>
        {skill}
    </div>
    """, unsafe_allow_html=True)

def render_avatar(name, title, image_url):
    """Render an avatar with name and title"""
    st.markdown(f"""
    <div style='text-align: center;'>
        <img src='{image_url}' style='width: 100px; height: 100px; border-radius: 50%; object-fit: cover;'>
        <h3 style='margin-top: 10px; margin-bottom: 0;'>{name}</h3>
        <p style='margin-top: 5px; color: #666;'>{title}</p>
    </div>
    """, unsafe_allow_html=True)

def render_progress_bar(value, key, max_value=100):
    """Render a custom progress bar"""
    # Calculate percentage
    percentage = min(100, max(0, value)) / max_value * 100
    
    # Determine color based on percentage
    if percentage >= 80:
        color = "#4CAF50"  # Green
    elif percentage >= 60:
        color = "#2196F3"  # Blue
    elif percentage >= 40:
        color = "#FF9800"  # Orange
    else:
        color = "#F44336"  # Red
    
    st.markdown(f"""
    <div style='width: 100%; background-color: #f0f0f0; border-radius: 5px; margin-bottom: 10px;'>
        <div style='width: {percentage}%; height: 20px; background-color: {color}; border-radius: 5px; text-align: center; color: white;'>
            {value}%
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_testimonials():
    """Render customer testimonials"""
    st.header("What Our Customers Say")
    
    # Testimonial data
    testimonials = [
        {
            "name": "Jessica Thompson",
            "position": "HR Director, TechCorp",
            "image": "https://randomuser.me/api/portraits/women/65.jpg",
            "text": "HireSense AI has revolutionized our hiring process. We've reduced our time-to-hire by 40% and found better candidates."
        },
        {
            "name": "Robert Chen",
            "position": "Talent Acquisition Manager, StartupX",
            "image": "https://randomuser.me/api/portraits/men/22.jpg",
            "text": "The AI-powered resume screening is incredibly accurate. It's like having an expert recruiter working 24/7."
        },
        {
            "name": "Amanda Johnson",
            "position": "Recruiting Lead, Enterprise Solutions",
            "image": "https://randomuser.me/api/portraits/women/33.jpg",
            "text": "We've seen a 35% improvement in the quality of candidates reaching the interview stage since implementing HireSense AI."
        }
    ]
    
    # Display testimonials in columns
    cols = st.columns(len(testimonials))
    
    for i, testimonial in enumerate(testimonials):
        with cols[i]:
            st.markdown(f"""
            <div style='border: 1px solid var(--border-color, #e0e0e0); 
                        border-radius: 10px; 
                        padding: 20px; 
                        height: 100%;
                        background-color: var(--card-bg-color, white);'>
                <div style='text-align: center; margin-bottom: 15px;'>
                    <img src='{testimonial["image"]}' style='width: 80px; height: 80px; border-radius: 50%; object-fit: cover;'>
                    <h4 style='margin-top: 10px; margin-bottom: 0;'>{testimonial["name"]}</h4>
                    <p style='margin-top: 5px; color: #666; font-size: 0.8rem;'>{testimonial["position"]}</p>
                </div>
                <p style='font-style: italic;'>"{testimonial["text"]}"</p>
            </div>
            """, unsafe_allow_html=True)

def render_stats_counter():
    """Render statistics counter"""
    st.markdown("<div style='padding: 20px 0; background-color: var(--primary-color, #0A21C0); color: white; border-radius: 10px; margin: 20px 0;'>", unsafe_allow_html=True)
    
    cols = st.columns(4)
    
    stats = [
        {"value": "500+", "label": "Companies"},
        {"value": "10,000+", "label": "Resumes Analyzed"},
        {"value": "40%", "label": "Time Saved"},
        {"value": "95%", "label": "Accuracy"}
    ]
    
    for i, stat in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
            <div style='text-align: center;'>
                <h2 style='font-size: 2.5rem; margin-bottom: 5px;'>{stat["value"]}</h2>
                <p style='font-size: 1rem;'>{stat["label"]}</p>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_pricing_section():
    """Render pricing plans"""
    st.header("Pricing Plans")
    
    # Pricing data
    pricing_plans = [
        {
            "name": "Starter",
            "price": "$49",
            "period": "per month",
            "description": "Perfect for small businesses and startups",
            "features": [
                "Up to 50 resume analyses per month",
                "Basic candidate ranking",
                "Email support",
                "1 user account"
            ],
            "cta": "Get Started",
            "highlight": False
        },
        {
            "name": "Pro",
            "price": "$99",
            "period": "per month",
            "description": "Ideal for growing teams and businesses",
            "features": [
                "Up to 200 resume analyses per month",
                "Advanced candidate ranking",
                "Skill gap analysis",
                "Priority email support",
                "5 user accounts",
                "API access"
            ],
            "cta": "Try Pro",
            "highlight": True
        },
        {
            "name": "Enterprise",
            "price": "Custom",
            "period": "pricing",
            "description": "For large organizations with custom needs",
            "features": [
                "Unlimited resume analyses",
                "Custom AI model training",
                "Advanced analytics and reporting",
                "Dedicated account manager",
                "24/7 priority support",
                "Unlimited user accounts",
                "Full API access",
                "Custom integrations"
            ],
            "cta": "Contact Sales",
            "highlight": False
        }
    ]
    
    # Display pricing plans in columns
    cols = st.columns(len(pricing_plans))
    
    for i, plan in enumerate(pricing_plans):
        with cols[i]:
            border_color = "var(--primary-color, #0A21C0)" if plan["highlight"] else "var(--border-color, #e0e0e0)"
            bg_color = "rgba(10, 33, 192, 0.05)" if plan["highlight"] else "var(--card-bg-color, white)"
            
            st.markdown(f"""
            <div style='border: 2px solid {border_color}; 
                        border-radius: 10px; 
                        padding: 20px; 
                        height: 100%;
                        background-color: {bg_color};'>
                <h3 style='text-align: center;'>{plan["name"]}</h3>
                <div style='text-align: center; margin: 20px 0;'>
                    <span style='font-size: 2.5rem; font-weight: bold;'>{plan["price"]}</span>
                    <span style='font-size: 1rem; color: #666;'> {plan["period"]}</span>
                </div>
                <p style='text-align: center; margin-bottom: 20px;'>{plan["description"]}</p>
                <ul style='padding-left: 20px; margin-bottom: 30px;'>
            """, unsafe_allow_html=True)
            
            for feature in plan["features"]:
                st.markdown(f"<li>{feature}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul>", unsafe_allow_html=True)
            
            if st.button(plan["cta"], key=f"pricing_{plan['name'].lower()}", use_container_width=True):
                if plan["name"] == "Enterprise":
                    st.session_state.page = 'contact'
                else:
                    st.session_state.page = 'auth'
                st.rerun()

def load_lottie_url(url):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def load_lottie_file(filepath):
    """Load Lottie animation from file"""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except:
        return None

def render_dashboard_visualization(is_hero=False):
    """Render a dashboard visualization with recruitment metrics"""
    if is_hero:
        # Simplified version for hero section
        # Create a sample dataset for the visualization
        months = st.session_state.monthly_stats['months']
        applications = st.session_state.monthly_stats['applications']
        interviews = st.session_state.monthly_stats['interviews']
        hires = st.session_state.monthly_stats['hires']
        
        # Create a figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Add traces
        fig.add_trace(
            go.Bar(
                x=months,
                y=applications,
                name="Applications",
                marker_color='#0A21C0'
            ),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(
                x=months,
                y=interviews,
                name="Interviews",
                marker_color='#FF9800',
                mode='lines+markers'
            ),
            secondary_y=True,
        )
        
        # Add figure title
        fig.update_layout(
            title_text="Recruitment Metrics",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(
                color='#333333'
            )
        )
        
        # Set x-axis title
        fig.update_xaxes(title_text="Month")
        
        # Set y-axes titles
        fig.update_yaxes(title_text="Applications", secondary_y=False)
        fig.update_yaxes(title_text="Interviews", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Full dashboard visualization
        # Create tabs for different visualizations
        tab1, tab2, tab3 = st.tabs(["Recruitment Funnel", "Monthly Metrics", "Candidate Sources"])
        
        with tab1:
            # Recruitment funnel
            funnel_data = {
                'Stage': ['Applications', 'Resume Screening', 'Phone Interview', 'Technical Assessment', 'Final Interview', 'Offer', 'Hire'],
                'Count': [250, 180, 120, 80, 40, 25, 20]
            }
            
            funnel_df = pd.DataFrame(funnel_data)
            
            fig = go.Figure(go.Funnel(
                y=funnel_df['Stage'],
                x=funnel_df['Count'],
                textposition="inside",
                textinfo="value+percent initial",
                opacity=0.8,
                marker=dict(
                    color=[
                        '#0A21C0', '#1E3FD8', '#325CF0', '#4679FF', 
                        '#5A96FF', '#6EB3FF', '#82D0FF'
                    ],
                    line=dict(width=1, color='#333333')
                ),
                connector=dict(line=dict(color="#333333", width=1))
            ))
            
            fig.update_layout(
                title="Recruitment Funnel",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # Monthly metrics
            months = st.session_state.monthly_stats['months']
            applications = st.session_state.monthly_stats['applications']
            interviews = st.session_state.monthly_stats['interviews']
            hires = st.session_state.monthly_stats['hires']
            
            # Create a figure with secondary y-axis
            fig = make_subplots(specs=[[{"secondary_y": True}]])
            
            # Add traces
            fig.add_trace(
                go.Bar(
                    x=months,
                    y=applications,
                    name="Applications",
                    marker_color='#0A21C0'
                ),
                secondary_y=False,
            )
            
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=interviews,
                    name="Interviews",
                    marker_color='#FF9800',
                    mode='lines+markers'
                ),
                secondary_y=True,
            )
            
            fig.add_trace(
                go.Scatter(
                    x=months,
                    y=hires,
                    name="Hires",
                    marker_color='#4CAF50',
                    mode='lines+markers'
                ),
                secondary_y=True,
            )
            
            # Add figure title
            fig.update_layout(
                title_text="Monthly Recruitment Metrics",
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            # Set x-axis title
            fig.update_xaxes(title_text="Month")
            
            # Set y-axes titles
            fig.update_yaxes(title_text="Applications", secondary_y=False)
            fig.update_yaxes(title_text="Interviews & Hires", secondary_y=True)
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Calculate metrics
            avg_time_to_hire = random.randint(20, 40)
            cost_per_hire = random.randint(3000, 5000)
            offer_acceptance_rate = random.randint(75, 95)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Avg. Time to Hire", f"{avg_time_to_hire} days")
            
            with col2:
                st.metric("Cost per Hire", f"${cost_per_hire}")
            
            with col3:
                st.metric("Offer Acceptance Rate", f"{offer_acceptance_rate}%")
        
        with tab3:
            # Candidate sources
            source_data = {
                'Source': ['Job Boards', 'Referrals', 'Company Website', 'LinkedIn', 'Recruiters', 'Other'],
                'Percentage': [35, 25, 15, 15, 7, 3]
            }
            
            source_df = pd.DataFrame(source_data)
            
            fig = px.pie(
                source_df, 
                values='Percentage', 
                names='Source',
                color_discrete_sequence=px.colors.sequential.Blues_r,
                hole=0.4
            )
            
            fig.update_layout(
                title="Candidate Sources",
                height=500
            )
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hoverinfo='label+percent'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display source quality metrics
            st.subheader("Source Quality Metrics")
            
            source_quality = {
                'Source': ['Job Boards', 'Referrals', 'Company Website', 'LinkedIn', 'Recruiters', 'Other'],
                'Quality Score': [75, 90, 80, 85, 70, 60]
            }
            
            quality_df = pd.DataFrame(source_quality)
            
            fig = px.bar(
                quality_df,
                x='Source',
                y='Quality Score',
                color='Quality Score',
                color_continuous_scale='blues',
                labels={'Quality Score': 'Candidate Quality Score (%)'}
            )
            
            fig.update_layout(
                title="Candidate Quality by Source",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

def render_tech_visualization():
    """Render a visualization of the AI technology behind HireSense"""
    # Create a flowchart-like visualization of the AI technology
    nodes = [
        {"id": "resume", "label": "Resume Upload", "x": 0, "y": 0, "color": "#0A21C0"},
        {"id": "parse", "label": "Resume Parsing", "x": 1, "y": 0, "color": "#1E3FD8"},
        {"id": "verify", "label": "Resume Verification", "x": 2, "y": 0, "color": "#325CF0"},
        {"id": "extract", "label": "Data Extraction", "x": 2, "y": 1, "color": "#4679FF"},
        {"id": "nlp", "label": "NLP Processing", "x": 3, "y": 0.5, "color": "#5A96FF"},
        {"id": "match", "label": "Skill Matching", "x": 4, "y": 0, "color": "#6EB3FF"},
        {"id": "rank", "label": "Candidate Ranking", "x": 5, "y": 0, "color": "#82D0FF"},
        {"id": "job", "label": "Job Requirements", "x": 4, "y": 1, "color": "#0A21C0"}
    ]
    
    edges = [
        {"from": "resume", "to": "parse"},
        {"from": "parse", "to": "verify"},
        {"from": "verify", "to": "extract"},
        {"from": "extract", "to": "nlp"},
        {"from": "nlp", "to": "match"},
        {"from": "match", "to": "rank"},
        {"from": "job", "to": "match"}
    ]
    
    # Create node positions
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    
    for node in nodes:
        node_x.append(node["x"])
        node_y.append(node["y"])
        node_text.append(node["label"])
        node_color.append(node["color"])
    
    # Create edge traces
    edge_x = []
    edge_y = []
    
    for edge in edges:
        from_node = next(node for node in nodes if node["id"] == edge["from"])
        to_node = next(node for node in nodes if node["id"] == edge["to"])
        
        edge_x.extend([from_node["x"], to_node["x"], None])
        edge_y.extend([from_node["y"], to_node["y"], None])
    
    # Create the figure
    fig = go.Figure()
    
    # Add edges
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines',
        showlegend=False
    ))
    
    # Add nodes
    fig.add_trace(go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        marker=dict(
            size=30,
            color=node_color,
            line=dict(width=2, color='#333')
        ),
        text=node_text,
        textposition="middle center",
        hoverinfo='text',
        showlegend=False
    ))
    
    # Update layout
    fig.update_layout(
        title="HireSense AI Technology Flow",
        showlegend=False,
        hovermode='closest',
        margin=dict(b=20, l=5, r=5, t=40),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=400,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Add explanation text
    st.markdown("""
    ### How Our AI Technology Works
    
    1. **Resume Upload**: Candidates or recruiters upload resumes in various formats
    2. **Resume Parsing**: Our AI extracts structured data from unstructured resume documents
    3. **Resume Verification**: Advanced algorithms detect potential inconsistencies or suspicious patterns
    4. **Data Extraction**: Key information like skills, experience, and education is extracted
    5. **NLP Processing**: Natural Language Processing understands context and semantics
    6. **Skill Matching**: AI matches candidate skills with job requirements
    7. **Candidate Ranking**: Candidates are scored and ranked based on multiple factors
    
    Our technology goes beyond simple keyword matching to understand the true meaning and context of skills and experiences, resulting in more accurate candidate matching.
    """)

