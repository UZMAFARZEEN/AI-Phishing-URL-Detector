import streamlit as st
import pandas as pd
import joblib
from urllib.parse import urlparse

# Load model
model = joblib.load("model.pkl")

st.set_page_config(
    page_title="AI Phishing URL Detector",
    page_icon="🔐",
    layout="centered"
)

st.title("🔐 AI Phishing URL Detector")

st.write(
    "Paste a URL below and let AI predict whether it is phishing or legitimate."
)


# Feature Extraction Function
def extract_features(url):
    parsed = urlparse(url)

    return {
        "url_length": len(url),
        "valid_url": 1 if parsed.netloc else 0,
        "at_symbol": 1 if "@" in url else 0,
        "sensitive_words_count": sum(
            word in url.lower()
            for word in ["login", "secure", "verify", "bank", "paypal"]
        ),
        "path_length": len(parsed.path),
        "isHttps": 1 if parsed.scheme == "https" else 0,
        "nb_dots": url.count("."),
        "nb_hyphens": url.count("-"),
        "nb_and": url.count("&"),
        "nb_or": url.count("|"),
        "nb_www": url.lower().count("www"),
        "nb_com": url.lower().count("com"),
        "nb_underscore": url.count("_")
    }


# URL Input
url = st.text_input(
    "Enter URL",
    placeholder="https://example.com"
)

if st.button("Detect"):

    if url:

        features = extract_features(url)

        data = pd.DataFrame([features])

        prediction = model.predict(data)[0]

        confidence = max(
            model.predict_proba(data)[0]
        ) * 100

        st.subheader("Result")

        if prediction == 1:
            st.error(
                f"⚠️ Phishing URL Detected ({confidence:.2f}% confidence)"
            )
        else:
            st.success(
                f"✅ Legitimate URL ({confidence:.2f}% confidence)"
            )

        st.subheader("Risk Factors")

        risks = []

        if "@" in url:
            risks.append("Contains @ symbol")

        if url.count("-") > 2:
            risks.append("Contains multiple hyphens")

        if not url.startswith("https"):
            risks.append("Does not use HTTPS")

        suspicious_words = [
            "login",
            "secure",
            "verify",
            "bank",
            "paypal"
        ]

        for word in suspicious_words:
            if word in url.lower():
                risks.append(f"Contains suspicious keyword: {word}")

        if risks:
            for risk in risks:
                st.warning(risk)
        else:
            st.info("No obvious risk factors detected.")

        with st.expander("View Extracted Features"):
            st.dataframe(data)

    else:
        st.warning("Please enter a URL.")