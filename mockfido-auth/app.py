
import streamlit as st  
import secrets  
from crypto_utils.fido import (
    generate_keypair, serialize_public_key,
    sign_challenge, verify_signature
)  
from services.user_service import init_users, register_user, user_exists, get_user_keys  # User management functions


st.set_page_config(page_title="MockFIDO2", page_icon="🔐")
st.title("🔐 Mock FIDO2 Authentication")

# Initialize the user database (creates empty storage if none exists)
init_users()

# Create sidebar navigation menu
option = st.sidebar.selectbox("Choose action", ["Register", "Login"])

# REGISTRATION FLOW
if option == "Register":
    st.subheader("🧾 Register New User")
    username = st.text_input("Username")  # Input field for new username

    if st.button("Register"):
        # Validate input
        if not username:
            st.warning("Username required.")
        elif user_exists(username):
            st.warning("User already exists.")
        else:
            # Generate new cryptographic key pair for the user
            priv, pub = generate_keypair()
            
            # Store user credentials in the database
            register_user(username, priv, pub)
            
            # Display success message and show the public key
            st.success(f"Registered {username}!")
            st.code(serialize_public_key(pub), language='text')  # Display PEM-formatted public key

# AUTHENTICATION FLOW
elif option == "Login":
    st.subheader("🔑 Authenticate Existing User")
    username = st.text_input("Username")  # Input field for existing username
    
    # Challenge Generation Phase
    if st.button("Generate Challenge"):
        if not user_exists(username):
            st.error("User does not exist.")
        else:
            # Create a secure random challenge (32 hex chars = 16 bytes)
            challenge = secrets.token_hex(16)
            
            # Store challenge and username in session state
            st.session_state.challenge = challenge
            st.session_state.login_user = username
            
            # Display the challenge to be signed by client
            st.info(f"Challenge: {challenge}")

    # Signature Verification Phase (only shows if challenge exists and username matches)
    if 'challenge' in st.session_state and username == st.session_state.get('login_user'):
        # Text area for pasting the hex-encoded signature
        sig_hex = st.text_area("Paste Signature (hex)", height=100)
        
        if st.button("Verify Signature"):
            # Retrieve user's public key from database
            user = get_user_keys(username)
            try:
                # Convert hex signature to bytes and verify
                sig_bytes = bytes.fromhex(sig_hex.strip())
                success = verify_signature(
                    user['public_key'], 
                    st.session_state.challenge, 
                    sig_bytes
                )
                if success:
                    st.success("✅ Authentication successful!")
                else:
                    st.error("❌ Signature invalid.")
            except Exception as e:
                st.error(f"Signature verification error: {e}")

    # Development helper: Shows what a valid signature would look like
    if st.button("Simulate Client Sign"):
        # Get the user's private key (for simulation only - in real FIDO2 this would be on client device)
        priv_key = get_user_keys(username)["private_key"]
        challenge = st.session_state.get("challenge")
        
        # Generate a valid signature for the current challenge
        sig = sign_challenge(priv_key, challenge)
        
        # Display the hex-encoded signature (simulates what a real client would send)
        st.text_area("Simulated Signature (hex)", value=sig.hex(), height=100)