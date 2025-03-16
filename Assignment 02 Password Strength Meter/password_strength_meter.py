# Project #2: Password Strength Meter

# A password strength meter is a tool that assesses the strength of a password based on a set of criteria.

import re
import streamlit as st

#Styling
st.set_page_config(page_title="Password Strength Meter by Hasan Rafay", page_icon="🔒", layout="centered")

#Custom CSS
st.markdown("""
<style>
    .main {text-align: center;}
    .stTextInput {width: 60% | important; margin: auto;}
    .stButton button {width: 50%; background-color: blue; color: white; font-size: 18px}
    .stButton button:hover {background-color: green;}
    .footer{
        text-align: center;
        margin-top: 50px;
        font-size: 16px;
        font-weight: 500;
        color: black;
    }
</style>
""", unsafe_allow_html=True)

#Title and Description
st.title("Password Strength Meter")
st.write("Check the strength of your password and make it more secure Level.🔐")

#function to check password strength
def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1 #increased score by 1 
    else:
        feedback.append("❌ Password should be **at least 8 characters long**.")

    if re.search(r'[A-Z]', password) and re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("❌ Password should contain **both uppercase and lowercase letters**.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Password should contain **at least one number (0-9)**.")

    if re.search(r'[!@#$%^&*":{}|<>]', password):
        score += 1
    else:
        feedback.append("❌ Password should contain **at least one special character (!@#$%^&*)**.")

    #Display Password Strength results 
    if score == 4:
        st.success("✅ Your password is **strong**! Secure password!🔑")
    elif score == 3:
        st.info("🔐 Your password is **good**! But try to make it stronger!🔑")
    else:
        st.error("❌ Your password is **weak**! Please make it stronger!🔑")

    #feedback
    if feedback:
        with st.expander("Improved Your Password"):
            for item in feedback:
                st.write(item)

password = st.text_input("Enter your password", type="password", help="Ensure your password is strong and secure!")

#Button to check password strength
if st.button("Check Password Strength"):
    if password:
        check_password_strength(password)
    else:
        st.warning(" ⚠ Please enter a password first!") #show warning if no password is entered


st.markdown("<div class='footer'>Developed by Syed Hasan Rafay</div>", unsafe_allow_html=True)