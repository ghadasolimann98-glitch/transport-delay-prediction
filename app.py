import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Transport Delay Prediction", layout="centered")

st.title("🚌 Transport Delay Prediction App")
st.write("Predict public transport delay based on trip information")

# محاولة تحميل الموديل بأمان
model_loaded = True
try:
    model = joblib.load("delay_model.pkl")
    features = joblib.load("model_features.pkl")
except Exception as e:
    model_loaded = False
    st.error("⚠️ Model could not be loaded due to environment compatibility issues.")
    st.info("The application interface is deployed successfully. Model loading issue is documented in the report.")

# واجهة الإدخال (تظهر في كل الأحوال)
passenger_count = st.number_input("Passenger Count", min_value=0, value=20)
hour = st.slider("Hour of Trip", 0, 23, 8)
latitude = st.number_input("Latitude", value=30.0)
longitude = st.number_input("Longitude", value=31.0)
is_weekend = st.selectbox("Is Weekend?", [0, 1])

# زر التوقع
if st.button("Predict Delay"):
    if not model_loaded:
        st.warning("Model is not available in this deployment environment.")
    else:
        input_data = pd.DataFrame({
            'passenger_count': [passenger_count],
            'hour': [hour],
            'latitude': [latitude],
            'longitude': [longitude],
            'is_weekend': [is_weekend]
        })

        for col in features:
            if col not in input_data.columns:
                input_data[col] = 0

        input_data = input_data[features]

        prediction = model.predict(input_data)
        st.success(f"Predicted Delay: {prediction[0]:.2f} minutes")
