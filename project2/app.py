import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

# -----------------------------------------------------------
# LOAD NLTK RESOURCES
# -----------------------------------------------------------
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()

# -----------------------------------------------------------
# TEXT PREPROCESSING FUNCTION
# -----------------------------------------------------------
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    # Remove special characters
    text = [i for i in text if i.isalnum()]

    # Remove stopwords
    text = [i for i in text if i not in stopwords.words('english')]

    # Stemming
    text = [ps.stem(i) for i in text]

    return " ".join(text)

# -----------------------------------------------------------
# LOAD MODEL + TF-IDF
# -----------------------------------------------------------
@st.cache_resource
def load_model():
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    model = pickle.load(open('model.pkl','rb'))
    return tfidf, model

tfidf, model = load_model()

# -----------------------------------------------------------
# STREAMLIT UI CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Spam Classifier", page_icon="📩")

st.markdown("""
    <h1 style="text-align:center; color:#4CAF50; font-size:40px;">📩 SMS / Email Spam Classifier</h1>
    <p style="text-align:center; font-size:18px; color:#AAAAAA;">
        Detect whether a message is <b>Spam</b> or <b>Not Spam</b> instantly!
    </p>
""", unsafe_allow_html=True)

st.write("---")

# -----------------------------------------------------------
# LARGE BUTTON CSS
# -----------------------------------------------------------
st.markdown("""
<style>
.big-button button {
    background-color: #4CAF50 !important;
    color: white !important;
    padding: 18px 30px !important;
    font-size: 22px !important;
    border-radius: 12px !important;
    width: 100% !important;
    height: 70px !important;
}
.big-button button:hover {
    background-color: #45a049 !important;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# INPUT AREA
# -----------------------------------------------------------
input_sms = st.text_area("✉️ Enter your message:", height=150)

# -----------------------------------------------------------
# BIG BUTTON
# -----------------------------------------------------------
predict_btn = st.container()
with predict_btn:
    clicked = st.button("🔍 Predict", key="big_button")

# -----------------------------------------------------------
# PREDICTION LOGIC
# -----------------------------------------------------------
if clicked:

    if len(input_sms.strip()) == 0:
        st.warning("⚠️ Please enter a message before predicting!")
    
    else:
        # 1. Preprocess
        transformed_sms = transform_text(input_sms)

        # 2. Vectorize
        vector_input = tfidf.transform([transformed_sms])

        # 3. Predict
        result = model.predict(vector_input)[0]
        proba = model.predict_proba(vector_input)[0]

        st.write("---")

        # 4. Display Result
        if result == 1:
            st.markdown(
                "<h2 style='color:red; text-align:center;'>🚨 SPAM MESSAGE 🚨</h2>",
                unsafe_allow_html=True
            )
            st.subheader(f"Confidence: {proba[1]*100:.2f}%")

            st.progress(int(proba[1]*100))  # confidence meter

        else:
            st.markdown(
                "<h2 style='color:green; text-align:center;'>✅ NOT SPAM</h2>",
                unsafe_allow_html=True
            )
            st.subheader(f"Confidence: {proba[0]*100:.2f}%")

            st.progress(int(proba[0]*100))

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.write("---")
st.markdown(
    "<p style='text-align:center; color:#999;'>Made with ❤️ using Streamlit</p>",
    unsafe_allow_html=True
)
