import re
import streamlit as st

class ChatHandler:
    """Handle chat interactions and workflows"""
    
    @staticmethod
    def is_balance_query(text):
        """Check if user is asking for balance"""
        keywords = ["balance", "account balance", "money left", "how much"]
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in keywords)
    
    @staticmethod
    def handle_balance_query():
        """Handle balance inquiry"""
        DUMMY_BALANCE = "₹50,000"
        return f"💰 Your account balance is {DUMMY_BALANCE}"
    
    @staticmethod
    def handle_transfer_workflow(user_input):
        """Handle money transfer step-by-step"""
        from .file_handlers import mask_account_number
        
        step = st.session_state.transfer_step
        
        if step == 1:
            st.session_state.transfer_data["beneficiary_name"] = user_input
            st.session_state.transfer_step = 2
            return "Enter Bank Name:"
        
        elif step == 2:
            st.session_state.transfer_data["bank_name"] = user_input
            st.session_state.transfer_step = 3
            return "Enter Account Number:"
        
        elif step == 3:
            if not user_input.isdigit() or len(user_input) < 6:
                return "Please enter a valid account number (minimum 6 digits)."
            
            masked_account = mask_account_number(user_input)
            st.session_state.transfer_data["account_number"] = masked_account
            st.session_state.transfer_step = 4
            return "Enter Amount to Transfer:"
        
        elif step == 4:
            if not re.match(r"^\d+(\.\d{1,2})?$", user_input):
                return "Please enter a valid amount (e.g., 1000 or 1000.50)."
            
            st.session_state.transfer_data["amount"] = user_input
            st.session_state.transfer_step = 5
            
            d = st.session_state.transfer_data
            return (
                f"Confirm transfer of ₹{d['amount']} to {d['beneficiary_name']} "
                f"({d['bank_name']} / {d['account_number']})? (yes/no)"
            )
        
        elif step == 5:
            if user_input.lower() == "yes":
                response = "✅ Transfer Successful!"
            else:
                response = "❌ Transfer Cancelled."
            
            # Reset transfer
            st.session_state.transfer_step = 0
            st.session_state.transfer_data = {}
            return response
        
        return None
    
    @staticmethod
    def handle_cheque_upload(image):
        """Handle cheque image upload"""
        from .file_handlers import validate_cheque
        
        if validate_cheque(image):
            return "✅ Valid cheque detected and processed."
        else:
            return "❌ Invalid cheque uploaded! Please upload a proper cheque image."
    
    @staticmethod
    def handle_kyc_completion():
        """Handle KYC completion"""
        return "✅ Video KYC completed and saved locally!"