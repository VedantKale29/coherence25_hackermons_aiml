import streamlit as st
import firebase_admin
from firebase_admin import auth
import time
import re

def check_auth():
    """Check if user is authenticated"""
    return st.session_state.user is not None

def login_user(email, password):
    """Login a user with email and password"""
    if not email or not password:
        return False, "Please enter both email and password"
    
    try:
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format"
        
        # In a real implementation, this would use Firebase Authentication
        # For demo purposes, we'll simulate the authentication
        
        # Simulate API call
        time.sleep(1)
        
        # Mock successful login
        user = {
            "uid": "mock-uid-123",
            "email": email,
            "displayName": email.split('@')[0]
        }
        
        # Store user in session state
        st.session_state.user = user
        
        return True, "Login successful"
    except Exception as e:
        return False, f"Login failed: {str(e)}"

def signup_user(email, password, phone=None):
    """Register a new user"""
    if not email or not password:
        return False, "Please enter both email and password"
    
    try:
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return False, "Invalid email format"
        
        # Validate password strength
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        # In a real implementation, this would use Firebase Authentication
        # For demo purposes, we'll simulate the registration
        
        # Simulate API call
        time.sleep(1)
        
        # Mock successful registration
        user = {
            "uid": "mock-uid-123",
            "email": email,
            "displayName": email.split('@')[0],
            "phone": phone
        }
        
        # Store user in session state
        st.session_state.user = user
        
        return True, "Registration successful"
    except Exception as e:
        return False, f"Registration failed: {str(e)}"

def logout_user():
    """Logout the current user"""
    st.session_state.user = None
    st.session_state.auth_status = None
    return True, "Logout successful"

def get_current_user():
    """Get the current user from session state"""
    return st.session_state.user

