import streamlit as st
from PIL import Image
from streamlit_chat import message
import cv2
import time
from datetime import datetime
import re

# ====== Config Imports ======
from config import BOT_NAME, BANK_NAME, WELCOME_MESSAGE

# ====== Session State Initialization ======
def init_session_state():
    """Initialize session state variables for chat, transfers, and KYC."""
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("transfer_step", 0)
    st.session_state.setdefault("transfer_data", {})
    st.session_state.setdefault("welcomed", False)
    st.session_state.setdefault("kyc_recorded", False)
    st.session_state.setdefault("processed_files", set())

# ====== Chat Helpers ======
def add_message(sender, text=None, image=None):
    """Add a message (text or image) to chat history."""
    msg = {"sender": sender}
    if text: msg["text"] = text
    if image: msg["image"] = image
    st.session_state.messages.append(msg)

# ====== Transfer Helpers ======
def reset_transfer():
    """Reset money transfer workflow."""
    st.session_state.transfer_step = 0
    st.session_state.transfer_data = {}

def mask_account_number(account_number):
    """Mask all digits except the last 4 for privacy."""
    return "*" * (len(account_number) - 4) + account_number[-4:] if len(account_number) >= 4 else account_number

# ====== Cheque Helpers ======
def validate_cheque(image):
    """Check if uploaded image meets minimum size for a cheque."""
    width, height = image.size
    return width > 300 and height > 150

# ====== Banking Query Helpers ======
def is_balance_query(text):
    """Detect if user is asking for account balance."""
    keywords = ["balance", "account balance", "money left", "how much"]
    return any(k in text.lower() for k in keywords)

def handle_balance_query():
    """Return dummy account balance."""
    return "💰 Your account balance is ₹50,000"

# ====== Streamlit App Setup ======
st.set_page_config(page_title=f"{BOT_NAME} - {BANK_NAME}", page_icon="🏦", layout="wide")
init_session_state()

# ====== Header ======
st.markdown(f"<h1 style='text-align:center'>🏦 {BOT_NAME}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center'><i>{BANK_NAME}</i></p>", unsafe_allow_html=True)

# ====== Welcome Message ======
if not st.session_state.welcomed:
    add_message("bot", WELCOME_MESSAGE)
    st.session_state.welcomed = True

# ====== Sidebar: Cheque Upload & Video KYC ======
with st.sidebar:
    st.header("📄 Cheque Processing")
    uploaded_cheque = st.file_uploader("Upload Cheque Image", type=["jpg","jpeg","png"], key="cheque_uploader")

    if uploaded_cheque:
        cheque_image = Image.open(uploaded_cheque)
        file_hash = hash(uploaded_cheque.getvalue())

        if file_hash not in st.session_state.processed_files:
            add_message("user", image=cheque_image)

            if validate_cheque(cheque_image):
                add_message("bot", "✅ Valid cheque detected and processed.")
            else:
                add_message("bot", "❌ Invalid cheque! Please upload a proper cheque image.")

            st.session_state.processed_files.add(file_hash)

        st.image(cheque_image, caption="Uploaded Cheque", width=250)

    st.header("🎥 Video KYC")
    if not st.session_state.kyc_recorded and st.button("Start 5-Second Video KYC"):
        status_text = st.empty()
        status_text.info("🔴 Recording 5 seconds...")

        cap = cv2.VideoCapture(0)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = f"kyc_video_{timestamp}.mp4"
        out = cv2.VideoWriter(video_filename, cv2.VideoWriter_fourcc(*'mp4v'), 20.0, (640,480))

        start_time = time.time()
        while time.time() - start_time < 5:
            ret, frame = cap.read()
            if ret: out.write(frame)

        cap.release()
        out.release()
        status_text.success("✅ Recording Complete!")

        add_message("user", "Completed video KYC")
        add_message("bot", "✅ Video KYC completed and saved!")
        st.session_state.kyc_recorded = True
        st.video(video_filename)

# ====== Chat Display ======
st.divider()
for i, msg in enumerate(st.session_state.messages):
    if "text" in msg:
        message(msg["text"], is_user=(msg["sender"]=="user"),
                key=f"msg_{i}_{hash(msg['text'])}",
                avatar_style="bottts" if msg["sender"]=="bot" else "miniavs")
    elif "image" in msg:
        st.image(msg["image"], width=250, caption="Uploaded Image")

# ====== Chat Input ======
user_input = st.chat_input("Type your message here...", key="chat_input")

if user_input:
    add_message("user", user_input)
    step = st.session_state.transfer_step

    # ====== Money Transfer Workflow ======
    if step > 0:
        if step == 1:
            st.session_state.transfer_data["beneficiary_name"] = user_input
            st.session_state.transfer_step = 2
            add_message("bot", "Enter Bank Name:")
        elif step == 2:
            st.session_state.transfer_data["bank_name"] = user_input
            st.session_state.transfer_step = 3
            add_message("bot", "Enter Account Number:")
        elif step == 3:
            if not user_input.isdigit() or len(user_input)<6:
                add_message("bot", "Please enter a valid account number (min 6 digits).")
            else:
                st.session_state.transfer_data["account_number"] = mask_account_number(user_input)
                st.session_state.transfer_step = 4
                add_message("bot", "Enter Amount to Transfer:")
        elif step == 4:
            if not re.match(r"^\d+(\.\d{1,2})?$", user_input):
                add_message("bot", "Enter a valid amount (e.g., 1000 or 1000.50).")
            else:
                st.session_state.transfer_data["amount"] = user_input
                st.session_state.transfer_step = 5
                d = st.session_state.transfer_data
                add_message("bot", f"Confirm transfer of ₹{d['amount']} to {d['beneficiary_name']} ({d['bank_name']} / {d['account_number']})? (yes/no)")
        elif step == 5:
            reply = user_input.strip().lower()
            if reply == "yes":
                add_message("bot", "✅ Transfer Successful!")
            elif reply == "no":
                add_message("bot", "❌ Transfer Cancelled.")
            else:
                add_message("bot", "Please reply with yes or no.")
                st.stop()
            reset_transfer()
            st.stop()

    # ====== Balance Inquiry ======
    elif is_balance_query(user_input):
        add_message("bot", handle_balance_query())

    # ====== Transfer Initiation ======
    elif "transfer" in user_input.lower():
        st.session_state.transfer_step = 1
        add_message("bot", "Enter Beneficiary Name:")

    # ====== General Banking Queries ======
    else:
        keywords = {
            "interest": "Our current interest rate is 4.5% per annum.",
            "loan": "We offer personal, home, and car loans. Visit our website for details.",
            "card": "You can apply for a credit or debit card through our mobile app.",
            "support": "Contact customer support at 1800-123-4567.",
            "hours": "Our bank hours are 9 AM to 6 PM, Monday to Saturday.",
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! How can I assist you?"
        }
        response = next((reply for k, reply in keywords.items() if k in user_input.lower()),
                        "I can help you with balance inquiries, money transfers, cheque processing, and KYC. Please be more specific.")
        add_message("bot", response)

# ====== Quick Action Buttons ======
st.divider()
st.subheader("Quick Actions")

col1, col2, col3, col4 = st.columns(4)

def handle_balance_click():
    add_message("user", "What's my balance?")
    add_message("bot", handle_balance_query())

def handle_transfer_click():
    add_message("user", "I want to transfer money")
    st.session_state.transfer_step = 1
    add_message("bot", "Enter Beneficiary Name:")

def handle_cheque_click():
    add_message("user", "Check my cheque status")
    add_message("bot", "Please upload a cheque image using the sidebar.")

def handle_help_click():
    add_message("user", "Help")
    add_message("bot", "I can help you with:\n• Balance inquiries\n• Money transfers\n• Cheque processing\n• Video KYC\n\nUse the sidebar for cheque uploads and KYC.")

buttons = [handle_balance_click, handle_transfer_click, handle_cheque_click, handle_help_click]
for col, func, label in zip([col1,col2,col3,col4], buttons, ["Check Balance","Transfer Money","Cheque Status","Help"]):
    col.button(label, use_container_width=True, on_click=func)

# ====== Clear Chat ======
with st.sidebar:
    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.clear()
        st.rerun()
