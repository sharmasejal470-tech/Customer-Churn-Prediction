import streamlit as st
import pandas as pd
import joblib
from charts import show_dashboard
import time
from login import login
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

# ================= PDF REPORT ================= #

def create_pdf(
    gender,
    tenure,
    monthly,
    total,
    contract,
    internet,
    prediction,
    probability,
    confidence
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    story = []

    story.append(Paragraph("<b>Customer Churn Prediction Report</b>", styles["Title"]))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(f"<b>Gender:</b> {gender}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Tenure:</b> {tenure} Months", styles["BodyText"]))

    story.append(Paragraph(f"<b>Monthly Charges:</b> ₹ {monthly:.2f}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Total Charges:</b> ₹ {total:.2f}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Contract:</b> {contract}", styles["BodyText"]))

    story.append(Paragraph(f"<b>Internet Service:</b> {internet}", styles["BodyText"]))

    story.append(Paragraph(
        f"<b>Prediction:</b> {'Churn' if prediction==1 else 'Stay'}",
        styles["BodyText"]
    ))

    story.append(Paragraph(
        f"<b>Risk:</b> {probability*100:.2f}%",
        styles["BodyText"]
    ))

    story.append(Paragraph(
        f"<b>Confidence:</b> {confidence:.2f}%",
        styles["BodyText"]
    ))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(
        "<b>AI Recommendation:</b>",
        styles["Heading2"]
    ))

    if prediction == 1:

        story.append(Paragraph(
            "Offer discounts, loyalty rewards and contact customer immediately.",
            styles["BodyText"]
        ))

    else:

        story.append(Paragraph(
            "Maintain customer engagement and provide premium services.",
            styles["BodyText"]
        ))

    story.append(Paragraph("<br/>", styles["Normal"]))

    story.append(Paragraph(
        "<b>Developed By:</b> Sejal Sharma",
        styles["BodyText"]
    ))

    doc.build(story)

    pdf = buffer.getvalue()

    buffer.close()

    return pdf

st.set_page_config(
    page_title="Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)
# ================= PREDICTION HISTORY ================= #

if "history" not in st.session_state:
    st.session_state.history = []

# ---------- LOGIN CHECK ----------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()


# ------------------ LOAD MODEL ------------------
model = joblib.load("customer_churn_model.pkl")
scaler = joblib.load("scaler.pkl")
feature_names = joblib.load("feature_names.pkl")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #4CAF50;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: white;
}

.info-box {
            
    background-color: #1E293B;
    padding: 20px;
    border-radius: 12px;
    color: white;
    border-left: 5px solid #4CAF50;
}
section[data-testid="stSidebar"]{
    background:#111827;
}

div[data-testid="stMetric"]{
    background:#1F2937;
    padding:15px;
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# ------------------ TITLE ------------------

st.markdown("<h1 class='title'>📊 Customer Churn Prediction System</h1>", unsafe_allow_html=True)

st.markdown("<p class='subtitle'>AI Powered Customer Retention Dashboard</p>", unsafe_allow_html=True)

st.write("")

st.markdown("""
<div class="info-box">

### 👋 Welcome!

This application predicts whether a customer is likely to leave the company based on customer information.

Please enter the customer details below and click **Predict**.

</div>
""", unsafe_allow_html=True)

# ================= CUSTOMER DETAILS ================= #

st.write("")
st.markdown("## 👤 Customer Information")

col1, col2 = st.columns(2)

# ---------------- LEFT COLUMN ---------------- #

with col1:

    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    senior = st.selectbox(
        "Senior Citizen",
        ["No", "Yes"]
    )

    partner = st.selectbox(
        "Partner",
        ["No", "Yes"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["No", "Yes"]
    )

    phone_service = st.selectbox(
        "Phone Service",
        ["No", "Yes"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["No", "Yes"] if phone_service == "Yes" else ["No phone service"]
    )

    # ---------------- RIGHT COLUMN ---------------- #

with col2:

    tenure = st.number_input(
        "Tenure (Months)",
        min_value=0,
        max_value=72,
        value=12
    )

    monthly = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0,
        step=1.0
    )

    total = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=float(round(tenure * monthly, 2)),
        step=10.0,
        help="Estimated based on Tenure × Monthly Charges"
    )

    contract = st.selectbox(
        "Contract",
        ["Month-to-month", "One year", "Two year"]
    )

    paperless = st.selectbox(
        "Paperless Billing",
        ["No", "Yes"]
    )

    payment = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )
    # ================= INTERNET SERVICES ================= #

st.write("")
st.markdown("## 🌐 Internet Services")

col3, col4 = st.columns(2)

with col3:

    internet = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    has_internet = (internet != "No")

    online_security = st.selectbox(
        "Online Security",
        ["No", "Yes"] if has_internet else ["No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["No", "Yes"] if has_internet else ["No internet service"]
    )

    device_protection = st.selectbox(
        "Device Protection",
        ["No", "Yes"] if has_internet else ["No internet service"]
    )

with col4:

    tech_support = st.selectbox(
        "Tech Support",
        ["No", "Yes"] if has_internet else ["No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["No", "Yes"] if has_internet else ["No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["No", "Yes"] if has_internet else ["No internet service"]
    )
    # ================= PREDICT BUTTON ================= #

st.write("")
st.markdown("---")

predict = st.button(
    "🔮 Predict Customer Churn",
    use_container_width=True
)
if predict:
    # Loading Animation
    with st.spinner("🤖 AI is analyzing customer data..."):
        time.sleep(2)


    # Create input dictionary
    input_data = {

        "Tenure Months": tenure,
        "Monthly Charges": monthly,
        "Total Charges": total,

        "Gender_Male": 1 if gender == "Male" else 0,

        "Senior Citizen_Yes": 1 if senior == "Yes" else 0,

        "Partner_Yes": 1 if partner == "Yes" else 0,

        "Dependents_Yes": 1 if dependents == "Yes" else 0,

        "Phone Service_Yes": 1 if phone_service == "Yes" else 0,

        "Multiple Lines_No phone service":
            1 if multiple_lines == "No phone service" else 0,

        "Multiple Lines_Yes":
            1 if multiple_lines == "Yes" else 0,

        "Internet Service_Fiber optic":
            1 if internet == "Fiber optic" else 0,

        "Internet Service_No":
            1 if internet == "No" else 0,

        "Online Security_No internet service":
            1 if online_security == "No internet service" else 0,

        "Online Security_Yes":
            1 if online_security == "Yes" else 0,

        "Online Backup_No internet service":
            1 if online_backup == "No internet service" else 0,

        "Online Backup_Yes":
            1 if online_backup == "Yes" else 0,

        "Device Protection_No internet service":
            1 if device_protection == "No internet service" else 0,

        "Device Protection_Yes":
            1 if device_protection == "Yes" else 0,

        "Tech Support_No internet service":
            1 if tech_support == "No internet service" else 0,

        "Tech Support_Yes":
            1 if tech_support == "Yes" else 0,

        "Streaming TV_No internet service":
            1 if streaming_tv == "No internet service" else 0,

        "Streaming TV_Yes":
            1 if streaming_tv == "Yes" else 0,

        "Streaming Movies_No internet service":
            1 if streaming_movies == "No internet service" else 0,

        "Streaming Movies_Yes":
            1 if streaming_movies == "Yes" else 0,

        "Contract_One year":
            1 if contract == "One year" else 0,

        "Contract_Two year":
            1 if contract == "Two year" else 0,

        "Paperless Billing_Yes":
            1 if paperless == "Yes" else 0,

        "Payment Method_Credit card (automatic)":
            1 if payment == "Credit card (automatic)" else 0,

        "Payment Method_Electronic check":
            1 if payment == "Electronic check" else 0,

        "Payment Method_Mailed check":
            1 if payment == "Mailed check" else 0,
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_data])

    # Arrange columns
    input_df = input_df[feature_names]

    # Scale input
    input_scaled = scaler.transform(input_df)

    # Prediction
    prediction = model.predict(input_scaled)[0]

    # Probability
    probability = model.predict_proba(input_scaled)[0][1]

    confidence = max(model.predict_proba(input_scaled)[0]) * 100

   
    # ---------------- RESULT ---------------- #

    st.write("")
    st.markdown("---")
    st.markdown("## 📊 Prediction Result")
    # ================= KPI CARDS =================

    st.write("")

    k1, k2, k3, k4 = st.columns(4)

    with k1:
       st.metric(
        label="👥 Customers",
        value="7043",
        delta="+152"
    )

    with k2:
      st.metric(
        label="📈 Retention",
        value=f"{(1-probability)*100:.1f}%"
    )

    with k3:
      st.metric(
        label="⚠ Risk",
        value=f"{probability*100:.1f}%"
    )

    with k4:
      st.metric(
        label="🤖 Model",
        value="Logistic Regression"
    )
  
    st.write("")

    if prediction == 1:

        st.error("## ⚠️ High Risk Customer")

        st.markdown(f"""
### 🔴 Churn Probability : **{probability*100:.2f}%**

**Confidence : {confidence:.2f}%**

 This customer is **likely to leave the company.**
    """)

        st.progress(float(probability))

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Risk Level",
                "HIGH 🔴"
            )

        with col2:
            st.metric(
                "Probability",
                f"{probability*100:.2f}%"
            )

        st.warning("""
### 💡 AI Recommendation

✅ Offer Discount

✅ Provide Loyalty Rewards

✅ Contact Customer Personally

✅ Upgrade Customer Support

✅ Offer Long-Term Contract
    """)

    else:

        st.success("## 🎉 Customer Will Stay")

        st.markdown(f"""
### 🟢 Churn Probability : **{probability*100:.2f}%**

**Confidence : {confidence:.2f}%**

Customer is **likely to continue with the company.**
""")

        st.progress(float(1-probability))

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Risk Level",
                "LOW 🟢"
            )

        with col2:
            st.metric(
                "Probability",
                f"{probability*100:.2f}%"
            )

        st.info("""
### 💡 AI Recommendation

✅ Maintain Good Customer Service

✅ Offer Premium Plans

✅ Loyalty Rewards

✅ Personalized Offers

✅ Continue Customer Engagement
""")
        # ================= CUSTOMER SUMMARY CARD ================= #

    st.markdown("---")

    prediction_text = "🟢 Stay" if prediction == 0 else "🔴 Churn"

    risk_color = "#00C853" if prediction == 0 else "#FF4B4B"

    st.markdown(f"""
<div style="
background:#1E293B;
padding:25px;
border-radius:18px;
border-left:8px solid {risk_color};
box-shadow:0 6px 15px rgba(0,0,0,0.35);
">

<h2 style="color:white;">📋 Customer Summary</h2>

<table style="width:100%; color:white; font-size:17px; border-collapse:collapse;">

<tr>
<td><b>👤 Gender</b></td>
<td>{gender}</td>
</tr>

<tr>
<td><b>📅 Tenure</b></td>
<td>{tenure} Months</td>
</tr>

<tr>
<td><b>💰 Monthly Charges</b></td>
<td>₹ {monthly:.2f}</td>
</tr>

<tr>
<td><b>💳 Total Charges</b></td>
<td>₹ {total:.2f}</td>
</tr>

<tr>
<td><b>📄 Contract</b></td>
<td>{contract}</td>
</tr>

<tr>
<td><b>🌐 Internet Service</b></td>
<td>{internet}</td>
</tr>

<tr>
<td><b>🎯 Prediction</b></td>
<td><b>{prediction_text}</b></td>
</tr>

<tr>
<td><b>⚠️ Churn Risk</b></td>
<td><b>{probability*100:.2f}%</b></td>
</tr>

<tr>
<td><b>🤖 Model</b></td>
<td>Logistic Regression</td>
</tr>

</table>

</div>
""", unsafe_allow_html=True)

    st.write("")
    # ================= DOWNLOAD PDF ================= #

    pdf = create_pdf(
    gender,
    tenure,
    monthly,
    total,
    contract,
    internet,
    prediction,
    probability,
    confidence
)

    st.download_button(
    label="📄 Download Prediction Report",
    data=pdf,
    file_name="Customer_Churn_Report.pdf",
    mime="application/pdf",
    use_container_width=True
)
    # ================= SAVE PREDICTION ================= #

    st.session_state.history.append({

    "Gender": gender,

    "Tenure": tenure,

    "Contract": contract,

    "Prediction": "🟢 Stay" if prediction == 0 else "🔴 Churn",

    "Risk %": round(probability * 100, 2),

    "Confidence %": round(confidence, 2)

})
    
        
        
    show_dashboard(probability,
    model,
    feature_names)

# ================= PREDICTION HISTORY TABLE ================= #

st.markdown("---")

st.subheader("📜 Prediction History")

history_df = pd.DataFrame(st.session_state.history)

st.dataframe(
    history_df,
    use_container_width=True,
    hide_index=True
)

# ================= DOWNLOAD HISTORY ================= #

history_csv = history_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Prediction History (CSV)",
    data=history_csv,
    file_name="prediction_history.csv",
    mime="text/csv",
    use_container_width=True
)



  
        
# ================= SIDEBAR ================= #

with st.sidebar:

    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=120)

    st.markdown("## 📊 Customer Churn Prediction")

    st.markdown("---")

    st.success("✅ Machine Learning Model Loaded")

    st.info("""
### Project Information

✔ Logistic Regression Model

✔ 30 Customer Features

✔ AI Prediction

✔ Real-Time Analysis

✔ Streamlit Dashboard
""")

    st.markdown("---")

    st.markdown("### 👩‍💻 Developed By")

    st.write("**Sejal Sharma**")

    st.caption("B.Tech CSE (AI & Data Science)")

    st.markdown("---")

    st.markdown(
        "<center>🚀 Built using Python + Streamlit + Machine Learning</center>",
        unsafe_allow_html=True,
    )
    # ================= FOOTER ================= #

st.markdown("---")

st.markdown("""
<div style="
text-align:center;
padding:20px;
color:#9CA3AF;
font-size:16px;
">

<h4>🚀 Customer Churn Prediction System</h4>

<p>
Developed by <b>Sejal Sharma</b><br>
B.Tech CSE (AI & Data Science)
</p>

<p>
🐍 Python &nbsp; | &nbsp;
🤖 Scikit-Learn &nbsp; | &nbsp;
📊 Streamlit &nbsp; | &nbsp;
📈 Plotly
</p>

<p style="font-size:14px;">
© 2026 All Rights Reserved
</p>

</div>
""", unsafe_allow_html=True)