import streamlit as st
import pandas as pd
import joblib

st.title("🚌 Transport Delay Prediction App")
st.write("Predict public transport delay in minutes")

# =========================
# تحميل الموديل بأمان
# =========================
try:
    model = joblib.load("delay_model.pkl")
    features = joblib.load("model_features.pkl")
    st.success("✅ Model loaded successfully")
except Exception as e:
    st.error("❌ Model could not be loaded due to environment incompatibility.")
    st.info("This is a known deployment issue caused by different scikit-learn versions.")
    st.stop()

# =========================
# مدخلات المستخدم
# =========================
passenger_count = st.number_input("Passenger Count", min_value=0)
hour = st.slider("Hour of Trip", 0, 23)
latitude = st.number_input("Latitude")
longitude = st.number_input("Longitude")
is_weekend = st.selectbox("Is Weekend?", [0, 1])

# =========================
# تجهيز الداتا
# =========================
input_data = pd.DataFrame({
    'passenger_count': [passenger_count],
    'hour': [hour],
    'latitude': [latitude],
    'longitude': [longitude],
    'is_weekend': [is_weekend]
})

# إضافة الأعمدة الناقصة
for col in features:
    if col not in input_data.columns:
        input_data[col] = 0

input_data = input_data[features]

# =========================
# التوقع
# =========================
if st.button("Predict Delay"):
    prediction = model.predict(input_data)
    st.success(f"🕒 Predicted Delay: {prediction[0]:.2f} minutes")
