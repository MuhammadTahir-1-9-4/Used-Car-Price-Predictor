import streamlit as st
import pandas as pd
import pickle
from datetime import date
import time
import os 


st.set_page_config(
    page_title="Used Car Price Predictor",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed" # Collapse sidebar by default
)

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        with open('xgb_model.pkl', 'rb') as file:
            model = pickle.load(file)
        return model
    except FileNotFoundError:
        st.error("Model file not found. Ensure 'xgb_model.pkl' is in the root directory.")
        return None

model = load_model()

st.markdown("""
    <style>
    # /* General Styling */
    # .stApp {
    #     background-color: #1a1a1a; /* Dark background */
    #     color: #e0e0e0;
    # }
    
    /* Title and Header Styling */
    .stTitle {
        text-align: center;
        font-family: 'Arial Black', sans-serif;
    }
    .stHeader {
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 10px;
    }

    /* Prediction Box Styling */
    .prediction-box {
        border: 2px solid #4CAF50;
        border-radius: 10px;
        padding: 25px;
        text-align: center;
        background-color: #2e2e2e; /* Slightly lighter dark shade */
        margin-top: 30px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
    }
    .prediction-title {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50; /* Green accent */
    }
    .prediction-value {
        font-size: 42px;
        font-weight: bold;
        color: #ffffff; /* White text */
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)


# construct the absolute path to the image file
# this makes the app work regardless of the current working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.join(script_dir, "assets", "car.png")

# use columns to center the title and image
_, mid_col, _ = st.columns([1, 2, 1])
with mid_col:
    # check if the image file exists before trying to display it
    if os.path.exists(image_path):
        st.image(image_path, use_container_width=True)
    else:
        # display a warning if the image is not found at the path
        st.warning("Car image not found. Please ensure 'assets/car.png' exists.")
        
    st.title('            Used Car Price Predictor')

st.markdown("<p style='text-align: center;'>This machine learning tool provides an estimated resale value for used cars. Fill in the car's details below to get a prediction.</p>", unsafe_allow_html=True)
st.divider()


st.header("Enter Car Details 📝")

# Using st.form to group inputs and have a single submission button
with st.form(key='car_input_form'):
    col1, col2, col3 = st.columns(3)

    with col1:
        present_price = st.number_input('Current Showroom Price (in Lakhs)', min_value=0.5, max_value=50.0, value=5.5, step=0.1)
        year = st.number_input('Year of Purchase', min_value=2000, max_value=date.today().year, value=2015)

    with col3:
        kms_driven = st.number_input('Kilometers Driven', min_value=500, max_value=500000, value=30000, step=500)
        owner = st.selectbox('Number of Previous Owners', [0, 1, 3], index=0)

    with col2:
        fuel_type = st.selectbox('Fuel Type', ['Petrol', 'Diesel', 'CNG'])
        seller_type = st.selectbox('Seller Type', ['Dealer', 'Individual'])
        transmission = st.selectbox('Transmission Type', ['Manual', 'Automatic'])

    # the submission button must be inside the form
    submit_button = st.form_submit_button(label='Predict Resale Value', use_container_width=True)


if submit_button:
    if model is not None:
        with st.spinner('Calculating...'):
            time.sleep(1) # simulate processing
            
            car_age = date.today().year - year
            fuel_diesel = 1 if fuel_type == 'Diesel' else 0
            fuel_petrol = 1 if fuel_type == 'Petrol' else 0
            seller_individual = 1 if seller_type == 'Individual' else 0
            transmission_manual = 1 if transmission == 'Manual' else 0

            # create input data frame
            # IMPORTANT: The column order MUST match the training data order
            input_data = pd.DataFrame({
                'Present_Price': [present_price], 'Kms_Driven': [kms_driven], 'Owner': [owner],
                'Car_Age': [car_age], 'Fuel_Type_Diesel': [fuel_diesel], 'Fuel_Type_Petrol': [fuel_petrol],
                'Seller_Type_Individual': [seller_individual], 'Transmission_Manual': [transmission_manual]
            })

            # make prediction
            prediction = model.predict(input_data)
            predicted_price = prediction[0]

            # display the result
            st.markdown(f"""
                <div class="prediction-box">
                    <p class="prediction-title">Estimated Resale Value</p>
                    <p class="prediction-value">₹ {predicted_price:.2f} Lakhs</p>
                </div>
                """, unsafe_allow_html=True)
            st.balloons()
    else:
        st.warning("Model is not loaded. Cannot make a prediction.")


# about section
st.divider()
with st.expander("ℹ️ About This Project", expanded=False):
    st.info("""
        This application is a demonstration of a complete machine learning project pipeline.
        - **Model:** XGBoost Regressor
        - **Dataset:** Used Car Sales data from Kaggle
        - **Tools:** Python, Pandas, Scikit-learn, Streamlit
    """)
    st.markdown("For more details, check out the [GitHub repository](https://github.com/MuhammadTahir-1-9-4/Used-Car-Price-Predictor).")