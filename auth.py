# auth.py
import bcrypt
import streamlit as st
from db import supabase



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
    try:
        # Get the shared password from database
        print(f"[DEBUG] Attempting to query users table...")
        result = supabase.table("users").select("*").eq("type", "shared_founder_password").execute()
        
        print(f"[DEBUG] Query result: {result}")
        print(f"[DEBUG] Data: {result.data}")
        print(f"[DEBUG] Number of records: {len(result.data) if result.data else 0}")
        
        if result.data and len(result.data) > 0:
            shared_cred = result.data[0]
            print(f"[DEBUG] Found user record: type={shared_cred.get('type')}")
            print(f"[DEBUG] Password hash exists: {bool(shared_cred.get('password'))}")
            
            if verify_password(password, shared_cred['password']):
                print(f"[DEBUG] Password verification: SUCCESS")
                return True
            else:
                print(f"[DEBUG] Password verification: FAILED")
        else:
            print(f"[DEBUG] No user record found with type='shared_founder_password'")
    except Exception as e:
        print(f"[DEBUG] Authentication error: {e}")
        import traceback
        traceback.print_exc()
    
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
