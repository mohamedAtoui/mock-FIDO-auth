import streamlit as st

def init_users():
    if 'users' not in st.session_state:
        st.session_state.users = {}

def register_user(username, private_key, public_key):
    st.session_state.users[username] = {
        'private_key': private_key,
        'public_key': public_key
    }

def user_exists(username):
    return username in st.session_state.users

def get_user_keys(username):
    return st.session_state.users.get(username)
