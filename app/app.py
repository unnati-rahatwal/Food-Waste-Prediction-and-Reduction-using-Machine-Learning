import streamlit as st
import pandas as pd
import pickle

# -------------------------------
# Load trained model
# -------------------------------
with open("/Users/unnatir/Desktop/ML/Food_Wastage_Prediction/model/food_waste_model.pkl", "rb") as f:
    model = pickle.load(f)

st.title("🍽️ Food Waste Prediction & Reduction System")

st.markdown("Predict food waste for events and get smart recommendations.")

# -------------------------------
# User Inputs
# -------------------------------
num_guests = st.number_input("Number of Guests", min_value=10, max_value=1000, value=300)
quantity_prepared = st.number_input("Quantity Prepared (kg)", min_value=50, max_value=1000, value=400)

food_type = st.selectbox("Food Type", ["Vegetables", "Meat", "Fruits", "Dairy Products"])
event_type = st.selectbox("Event Type", ["Wedding", "Corporate", "Birthday", "Social Gathering"])
pricing = st.selectbox("Pricing", ["Low", "Moderate", "High"])
prep_method = st.selectbox("Preparation Method", ["Buffet", "Finger Food"])
storage = st.selectbox("Storage Condition", ["Refrigerated", "Room Temperature"])
season = st.selectbox("Season", ["Winter", "Summer", "All Seasons"])
location = st.selectbox("Location", ["Urban", "Suburban", "Rural"])

# -------------------------------
# Create input dataframe
# -------------------------------
input_dict = {
    "num_guests": num_guests,
    "quantity_prepared": quantity_prepared,
    "waste_ratio": 0,          # placeholder
    "waste_per_guest": 0       # placeholder
}

df_input = pd.DataFrame([input_dict])

# Add categorical values
cat_data = {
    "food_type": food_type,
    "event_type": event_type,
    "Pricing": pricing,
    "Preparation Method": prep_method,
    "Storage Conditions": storage,
    "Seasonality": season,
    "Geographical Location": location
}

for k, v in cat_data.items():
    df_input[k] = v

# One-hot encode
df_input = pd.get_dummies(df_input)

# Align columns with model
model_features = model.feature_names_in_
df_input = df_input.reindex(columns=model_features, fill_value=0)

# -------------------------------
# Prediction
# -------------------------------
if st.button("Predict Food Waste"):
    prediction = model.predict(df_input)[0]

    st.subheader("📊 Prediction Result")
    st.success(f"Estimated Food Waste: **{prediction:.2f} kg**")

    # Risk level
    if prediction < 20:
        st.info("🟢 Low Waste Risk")
    elif prediction < 40:
        st.warning("🟡 Medium Waste Risk")
    else:
        st.error("🔴 High Waste Risk")

    # -------------------------------
    # Recommendations (NOVELTY)
    # -------------------------------
    st.subheader("💡 Waste Reduction Recommendations")

    if quantity_prepared > num_guests * 1.2:
        st.write("• Reduce quantity prepared to match guest count")

    if prep_method == "Buffet":
        st.write("• Switch from buffet to portion-controlled serving")

    if num_guests > 400:
        st.write("• Improve guest forecasting for large events")

    if food_type == "Fruits":
        st.write("• Prepare fruits closer to serving time")

    st.write("• Donate surplus food to nearby NGOs if safe")
