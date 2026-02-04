# auth.py
import bcrypt
import streamlit as st
from db import users_collection


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def authenticate(password: str) -> bool:
    """Authenticate using the shared founder password."""
    # Get the shared password from database
    shared_cred = users_collection.find_one({"type": "shared_founder_password"})
    
    if shared_cred and verify_password(password, shared_cred['password']):
        return True
    return False


def login(password: str) -> bool:
    """Log in with shared password and set session state."""
    if authenticate(password):
        st.session_state['authenticated'] = True
        return True
    return False


def logout():
    """Log out the current user."""
    st.session_state['authenticated'] = False


def is_authenticated() -> bool:
    """Check if a user is authenticated."""
    return st.session_state.get('authenticated', False)
