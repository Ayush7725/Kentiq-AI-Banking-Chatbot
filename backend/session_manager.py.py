import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "transfer_step" not in st.session_state:
        st.session_state.transfer_step = 0
    
    if "transfer_data" not in st.session_state:
        st.session_state.transfer_data = {}
    
    if "welcomed" not in st.session_state:
        st.session_state.welcomed = False
    
    if "kyc_recorded" not in st.session_state:
        st.session_state.kyc_recorded = False

def add_message(sender, text=None, image=None):
    """Add a message to chat history"""
    message = {"sender": sender}
    
    if text:
        message["text"] = text
    if image:
        message["image"] = image
    
    st.session_state.messages.append(message)

def reset_transfer():
    """Reset transfer workflow"""
    st.session_state.transfer_step = 0
    st.session_state.transfer_data = {}