# Kentiq AI Banking Chatbot (DGSL Bank)

A conversational banking assistant simulating real-world banking operations using **dummy data**. Handles **balance inquiry, money transfer, cheque upload, and dummy video KYC**.

---

## Key Features

* **Account Balance Inquiry:** Returns dummy balance.
* **Money Transfer:** Step-by-step flow with confirmation.
* **Cheque Upload & Validation:** Accepts only cheque-like images, rejects invalid ones.
* **Video KYC:** Records short video locally and confirms completion.
* **Typo Handling & Error Guidance:** Recognizes common spelling mistakes and provides polite instructions.

---

## Technical Architecture

* **Backend:** Python functions with Streamlit `session_state` for conversation flow.
* **Image Validation:** OpenCV + NumPy heuristics (aspect ratio + text density).
* **Video KYC:** Streamlit `camera_input` saving videos locally.
* **Frontend:** Streamlit chat interface with real-time messaging.

---

## Setup & Run

```bash
# Clone the repository
git clone <repo-link>
cd project1_chatbot

# Install dependencies
pip install -r requirements.txt

# Run the chatbot
streamlit run app.py
```

---

## Project Structure

```Chatbot/ 
│
├── __pycache__/ 
│
├
│
├── backend/ 
│   ├── __init__.py 
│   ├── chat_handler.py 
│   ├── file_handlers.py 
│   ├── session_manager.py 
│   └── utils.py 
│
├── venv/ 
│
├── app.py 
│
├── config.py 
│
├── README.md 
│
└── requirements.txt 

## Usage Examples

* **Balance Inquiry:** `"What's my savings account balance?"`
* **Transfer Funds:** `"Transfer ₹5000 to Aman Singh"`
* **Cheque Upload:** Upload `.jpg/.png` image
* **Video KYC:** `"Start video KYC"`

---

## Technologies Used

Python, Streamlit, OpenCV, Pillow,session state

---

## Demo

Screenshots:

* `welcome.png`, `balance.png`, `transfer.png`, `cheque_valid.png`, `video_kyc.png`
