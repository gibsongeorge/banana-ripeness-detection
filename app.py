import streamlit as st
import numpy as np
from tensorflow import keras
from PIL import Image
import pandas as pd
import base64

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="🍌 Banana Ripeness Detector",
    page_icon="🍌",
    layout="centered",
)

# --- FIXED BACKGROUND BLUR ---
def add_background(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    css = f"""
    <style>

    /* Background image layer */
    .bg-layer {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        filter: blur(8px);
        z-index: -2;
    }}

    /* Semi-transparent overlay to improve readability */
    .bg-overlay {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(255,255,255,0.4); /* Light overlay for readability */
        z-index: -1;
    }}

    /* Make sure Streamlit content stays above */
    .main-content {{
        position: relative;
        z-index: 10;
    }}

    </style>

    <div class="bg-layer"></div>
    <div class="bg-overlay"></div>
    <div class="main-content">
    """

    st.markdown(css, unsafe_allow_html=True)

add_background(r"C:\Users\GIBSON\Desktop\Banana\bananapic2.jpg")

# --- LOAD MODEL ---
@st.cache_resource
def load_model():
    model_path = r"C:\Users\GIBSON\Desktop\Banana\banana_model.keras"
    model = keras.models.load_model(model_path)
    return model

model = load_model()

# --- CLASS LABELS ---
class_names = ["overripe", "ripe", "rotten", "unripe"]

# --- TITLE ---
st.title("🍌 Banana Ripeness Classifier")
st.write("Upload a banana image to check its ripeness stage!")

# --- IMAGE UPLOAD ---
uploaded_file = st.file_uploader("Upload an image of a banana", type=["jpg", "jpeg", "png"])

# --- IMAGE PREPROCESSING ---
def preprocess_image(img):
    img = img.convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# --- PREDICTION ---
if uploaded_file is not None:
    image = Image.open(uploaded_file)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(image, caption="Uploaded Image", width=230)

    with col2:
        st.write("🔍 Analyzing...")

        img_array = preprocess_image(image)
        prediction = model.predict(img_array)
        pred_index = np.argmax(prediction)
        pred_label = class_names[pred_index].capitalize()

        st.subheader(f"✅ Predicted Stage: **{pred_label}**")

        if pred_label.lower() == "unripe":
            st.info("🍏 Leave at room temp to ripen. 3–5 days to become ripe.")
        elif pred_label.lower() == "ripe":
            st.success("🍌 Perfect to eat! 2–3 days room temp or 1 week in fridge.")
        elif pred_label.lower() == "overripe":
            st.warning("🍯 Best for smoothies or banana bread.")
        else:
            st.error("🚫 Rotten — not safe to eat. Throw it away.")

    st.markdown("### 🍃 Banana Ripeness Guide")

    data = {
        "Stage": ["Unripe", "Ripe", "Overripe", "Rotten"],
        "Room Temp (25°C)": ["5–7 days before ripening", "2–3 days", "1–2 days", "Unsafe"],
        "In Fridge": ["Not recommended", "5–7 days", "3–5 days", "Unsafe"],
    }

    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)

# --- FOOTER ---
st.markdown("</div>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Developed by Gibson George | Powered by TensorFlow & Streamlit 🍌")
