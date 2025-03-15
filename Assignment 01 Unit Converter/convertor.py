# Project 01:- Unit Converter
# A Google Unit Converter built with Python and Streamlit that allows users to easily convert between various units of measurement like distance, temperature, weight, time and distance.

import streamlit as st
st.markdown(
    """
    <style>
    body {
        background-color: #lele2f;
        color: white;
    }
    .stApp {
        background: linear-gradient(135deg,rgb(76, 255, 181),rgb(226, 253, 210));
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
    }
    .h1 {
        text-align: center;
        font-size: 36px;
        color: white;
    }
    .stButton>button {
            background: linear-gradient(45deg, #ff9a9e, #fad0c4);
            color: black;
            font-size: 20px;
            padding: 12px 24px;
            border-radius: 12px;
            transition: 0.3s;
            box-shadow: 0px 5px 15px rgba(255, 154, 158, 0.4);
            cursor: pointer;
    }
    .stButton>button:hover {
            transform: scale(1.08);
            background: linear-gradient(45deg, #84fab0, #8fd3f4);
            color: black;
    }
    .stselectbox {
        cursor: pointer;
    }
    .result {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        background: rgba(162, 255, 149, 0.1);
        padding: 25px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0px 5px 15px rgba(0, 201, 255, 0.4);
    }
    .footer{
        text-align: center;
        margin-top: 50px;
        font-size: 16px;
        font-weight: 500;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#title and description:
st.markdown("<h1 class='h1'>Unit Converter🔁</h1>", unsafe_allow_html=True)
st.markdown("""
    <h3 style="text-align:center; font-size:22px; font-weight:500; color:#333;">
        Easily convert between 
        <span style="color:#004d00; font-weight:600;">Length</span>, 
        <span style="color:#8B0000; font-weight:600;">Temperature</span>, and 
        <span style="color:#003366; font-weight:600;">Weight</span> units in just a click!
    </h3>
    <hr style="border:none; height:2px; background:linear-gradient(90deg, #ff9a9e, #84fab0, #8fd3f4); margin:10px 0 20px;">
""", unsafe_allow_html=True)
#sidebar menu
conversion_type = st.sidebar.selectbox("Choose Conversion Type", ["Lenght", "Weight", "Temperature", "Time", "Distance"])
value = st.sidebar.number_input("Enter the value to convert", value=0.0, min_value=0.0, step=0.1)
col1, col2 = st.columns(2)

if conversion_type == "Lenght":
    with col1:
        from_unit = st.selectbox("From", ["Meters", "Kilometers", "Miles", "Feet", "Yards", "Inches"])
    with col2:
        to_unit = st.selectbox("To", ["Meters", "Kilometers", "Miles", "Feet", "Yards", "Inches"])

elif conversion_type == "Weight":
    with col1:
        from_unit = st.selectbox("From", ["Kilograms", "Grams", "Pounds", "Ounces", "Milligrams", "Micrograms"])
    with col2:
        to_unit = st.selectbox("To", ["Kilograms", "Grams", "Pounds", "Ounces", "Milligrams", "Micrograms"])

elif conversion_type == "Temperature":
    with col1:
        from_unit = st.selectbox("From", ["Celsius", "Fahrenheit", "Kelvin"])
    with col2:
        to_unit = st.selectbox("To", ["Celsius", "Fahrenheit", "Kelvin"])

elif conversion_type == "Time":
    with col1:
        from_unit = st.selectbox("From", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"])
    with col2:
        to_unit = st.selectbox("To", ["Seconds", "Minutes", "Hours", "Days", "Weeks", "Months", "Years"])

elif conversion_type == "Distance":
    with col1:
        from_unit = st.selectbox("From", ["Meters", "Kilometers", "Miles", "Feet", "Yards", "Inches"])
    with col2:
        to_unit = st.selectbox("To", ["Meters", "Kilometers", "Miles", "Feet", "Yards", "Inches"])

#converted Function
def length_convertor(value, from_unit, to_unit):
    lenght_units = {
        "Meters": 1, 'Kilometers': 0.001, 'centimeters' : 100, 'Millimeters': 1000, 'Miles': 0.000621371, 'Yards': 1.09361, 'Feet': 3.28, 'Inches': 39.37
    }
    return value * lenght_units[from_unit] / lenght_units[to_unit]

def weight_convertor(value, from_unit, to_unit):
    weight_units = {
        "Kilograms": 1, "Grams": 1000, "Pounds": 2.20462, "Ounces": 35.274, "Milligrams": 1000000, "Micrograms": 1000000000
    }
    return value * weight_units[from_unit] / weight_units[to_unit]

def temperature_convertor(value, from_unit, to_unit):
    if from_unit == "Celsius":
        return (value * 9/5 + 32) if to_unit == "Fahrenheit" else (value + 273.15) if to_unit == "Kelvin" else value
    elif from_unit == "Fahrenheit":
        return (value - 32) * 5/9 if to_unit == "Celsius" else (value - 32) * 5/9 + 273.15 if to_unit == "Kelvin" else value
    elif from_unit == "Kelvin":
        return (value - 273.15) if to_unit == "Celsius" else (value - 273.15) * 9/5 + 32 if to_unit == "Fahrenheit" else value

def time_convertor(value, from_unit, to_unit):
    time_units = {
        "Seconds": 1, "Minutes": 60, "Hours": 3600, "Days": 86400, "Weeks": 604800, "Months": 2629746, "Years": 31556952
    }
    return value * time_units[from_unit] / time_units[to_unit]

def distance_convertor(value, from_unit, to_unit):
    distance_units = {
        "Meters": 1, "Kilometers": 0.001, "Miles": 0.000621371, "Feet": 3.28, "Yards": 1.09361, "Inches": 39.37
    }
    return value * distance_units[from_unit] / distance_units[to_unit]

#Button for conversion
if st.button("🤖Convert"):
    if conversion_type == "Lenght":
        result = length_convertor(value, from_unit, to_unit)
    elif conversion_type == "Weight":
        result = weight_convertor(value, from_unit, to_unit)
    elif conversion_type == "Temperature":
        result = temperature_convertor(value, from_unit, to_unit)
    elif conversion_type == "Time":
        result = time_convertor(value, from_unit, to_unit)
    elif conversion_type == "Distance":
        result = distance_convertor(value, from_unit, to_unit)
    st.markdown(f"<div class='result'>{value} {from_unit} is equal to {result} {to_unit}</div>", unsafe_allow_html=True)
    
st.markdown("<div class='footer'>Developed by Syed Hasan Rafay</div>", unsafe_allow_html=True)
        




