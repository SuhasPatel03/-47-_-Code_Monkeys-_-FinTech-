import streamlit as st
import pandas as pd
import easyocr
import re
import numpy as np
from preprocess import preprocess_image
import matplotlib.pyplot as plt

# Initialize EasyOCR reader (language set to English)
reader = easyocr.Reader(['en'])

# Initialize session state data structure if it doesn't exist
if "data" not in st.session_state:
    st.session_state.data = {"expense": 0.0, "income": 0.0, "savings": 0.0, "emi": 0.0}

if "conversation" not in st.session_state:
    st.session_state.conversation = []

# Helper function to extract total from the OCR text
def extract_total(text):
    total_pattern = r'\btotal[:\s]*[\$₹]?\d+(\.\d{2})?'  # Regex to match total amount
    total_match = re.search(total_pattern, text, re.IGNORECASE)
    if total_match:
        total_str = re.sub(r'[^\d.]', '', total_match.group())
        return float(total_str) if total_str else None
    return None

# Streamlit App
st.title("Expense Tracker - Image Upload and Manual Entry")

# Sidebar for stats
with st.sidebar:
    st.header("Expense Tracker Summary")
    st.metric("Total Income", f"₹{st.session_state.data['income']}")
    st.metric("Total Expenses", f"₹{st.session_state.data['expense']}")
    st.metric("Savings", f"₹{st.session_state.data['savings']}")
    st.metric("Remaining Amount", f"₹{st.session_state.data['income'] - st.session_state.data['expense']}")

    # Save to Excel
    if st.button("Download Data as Excel"):
        df = pd.DataFrame([st.session_state.data])
        df.to_excel("expense_tracker_data.xlsx", index=False)
        st.success("Data saved as 'expense_tracker_data.xlsx'")

# Tabs for Chatbot, Data Entry, and Visualization
tab1, tab2, tab3 = st.tabs(["Chatbot", "Data Entry", "Visualization"])

# Chatbot Tab
with tab1:
    st.title("Expense Tracker Assistant")

    # Display conversation history
    st.write("### Conversation History")
    for message in st.session_state.conversation:
        if message.startswith("You:"):
            st.markdown(f'<div class="chat-container user-message">{message}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-container bot-message">{message}</div>', unsafe_allow_html=True)

    # Dropdown to select user input
    options = ["Hi", "Add Expense", "Add Income", "Show Summary", "Help"]
    user_input = st.selectbox("Select an option:", options)

    # Respond to user selection
    if user_input:
        st.session_state.conversation.append(f"You: {user_input}")
        if user_input == "Hi":
            response = "Hello! How can I assist you today?"
        elif user_input == "Add Expense":
            response = "Please upload your receipt or enter expense details manually in the 'Data Entry' tab."
        elif user_input == "Add Income":
            response = "You can enter your income details manually in the 'Data Entry' tab."
        elif user_input == "Show Summary":
            response = "You can view a detailed summary in the sidebar."
        elif user_input == "Help":
            response = "You can use this chatbot to track expenses, income, and EMI payments. Navigate through the tabs for details."
        else:
            response = "Sorry, I didn't understand. Please choose one of the options."
        st.session_state.conversation.append(f"Bot: {response}")

# Data Entry Tab
with tab2:
    st.subheader("Data Entry Options")

    # Dropdown to choose data entry method
    data_entry_method = st.selectbox("How would you like to enter data?", ["Upload Receipt Image", "Manual Entry"])

    if data_entry_method == "Upload Receipt Image":
        st.subheader("Upload Receipt Image")

        with st.form("receipt_form"):
            uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            submit_button = st.form_submit_button("Submit Image")

            if uploaded_image is not None:
                # Preprocess the uploaded image
                preprocessed_image = preprocess_image(uploaded_image)

                # Convert PIL image to a NumPy array for EasyOCR
                np_image = np.array(preprocessed_image)

                # Perform OCR on the NumPy array
                result = reader.readtext(np_image)

                # Extract text from OCR results
                text = " ".join([t[1] for t in result]) if result else "No text detected"

                # Extract the total amount
                total_amount = extract_total(text)

                # Update the expense value directly with extracted total
                if total_amount is not None:
                    st.session_state.data["expense"] = total_amount
                    st.success(f"Expense updated to ₹{total_amount} from receipt.")

            if submit_button:
                st.success("Receipt has been processed successfully.")

    elif data_entry_method == "Manual Entry":
        st.subheader("Enter Financial Details Manually")

        # Add Income
        st.number_input(
            "Enter Income (₹):",
            value=st.session_state.data["income"],
            step=100.0,
            key="input_income",
            on_change=lambda: st.session_state.data.update({"income": st.session_state.input_income}),
        )

        # Add Savings
        st.number_input(
            "Enter Savings (₹):",
            value=st.session_state.data["savings"],
            step=100.0,
            key="input_savings",
            on_change=lambda: st.session_state.data.update({"savings": st.session_state.input_savings}),
        )

        # Add Expenses
        st.number_input(
            "Enter Expenses Manually (₹):",
            value=st.session_state.data["expense"],
            step=100.0,
            key="input_expense",
            on_change=lambda: st.session_state.data.update({"expense": st.session_state.input_expense}),
        )

# Visualization Tab
with tab3:
    st.title("Visualization")

    # Plotting Bar Graph
    categories = ["Expenses", "Income", "Savings"]
    values = [
        st.session_state.data["expense"],
        st.session_state.data["income"],
        st.session_state.data["savings"],
    ]
    fig, ax = plt.subplots()
    ax.bar(categories, values, color=["red", "green", "blue"])
    ax.set_title("Expense Tracker Overview")
    ax.set_ylabel("Amount (₹)")
    st.pyplot(fig)