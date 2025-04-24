import streamlit as st  
import secrets  
from crypto_utils.fido import (
    generate_keypair, serialize_public_key,
    sign_challenge, verify_signature
)  
from services.user_service import (
    init_users, register_user, user_exists,
    get_user_keys, get_user_email
)
from services.email_service import send_challenge_email

st.set_page_config(page_title="MockFIDO2", page_icon="🔐")
st.title("🔐 Mock FIDO2 Authentication")

init_users()

option = st.sidebar.selectbox("Choose action", ["Register", "Login"])

# ===================== REGISTRATION ===================== #
if option == "Register":
    st.subheader("🧾 Register New User")
    username = st.text_input("Username")
    email = st.text_input("Email")

    if st.button("Register"):
        if not username or not email:
            st.warning("Username and email are required.")
        elif user_exists(username):
            st.warning("User already exists.")
        else:
            priv, pub = generate_keypair()
            register_user(username, email, priv, pub)
            st.success(f"Registered {username}!")
            st.code(serialize_public_key(pub), language='text')

# ===================== LOGIN ===================== #
elif option == "Login":
    st.subheader("🔑 Authenticate Existing User")
    username = st.text_input("Username")

    if st.button("Generate Challenge"):
        if not user_exists(username):
            st.error("User does not exist.")
        else:
            challenge = secrets.token_hex(16)
            st.session_state.challenge = challenge
            st.session_state.login_user = username

            try:
                email = get_user_email(username)
                send_challenge_email(email, challenge)
                st.success(f"✅ Challenge sent to {email}!")
            except Exception as e:
                st.error(f"Failed to send email: {e}")

    if 'challenge' in st.session_state and username == st.session_state.get('login_user'):
        sig_hex = st.text_area("Paste Signature (hex)", height=100)
        
        if st.button("Verify Signature"):
            user = get_user_keys(username)
            try:
                sig_bytes = bytes.fromhex(sig_hex.strip())
                success = verify_signature(user['public_key'], st.session_state.challenge, sig_bytes)
                if success:
                    st.success("✅ Authentication successful!")
                else:
                    st.error("❌ Signature invalid.")
            except Exception as e:
                st.error(f"Signature verification error: {e}")

