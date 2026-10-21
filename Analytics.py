import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Customer Prediction Analytics")

if "history" not in st.session_state or len(st.session_state.history) == 0:
    st.info("ℹ️ No predictions recorded in this active session yet.")
    st.markdown("""
    ### How to view real-time analytics:
    1. Navigate to the **Customer Churn Prediction** home page.
    2. Input customer demographic, contract, and service details.
    3. Click **Predict Customer Churn**.
    4. Return here to inspect cumulative session analytics, risk distribution, and contract comparisons.
    """)
else:
    df = pd.DataFrame(st.session_state.history)
    st.markdown("### 📈 Session Prediction Summary")
    
    total = len(df)
    churn_count = sum(df["Prediction"].str.contains("Churn", na=False))
    churn_pct = (churn_count / total) * 100 if total > 0 else 0
    avg_risk = df["Risk %"].mean() if "Risk %" in df.columns else 0.0

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Total Customers Analyzed", f"{total}")
    with m2:
        st.metric("Session Churn Rate", f"{churn_pct:.1f}%")
    with m3:
        st.metric("Average Churn Risk", f"{avg_risk:.1f}%")

    st.write("")
    c1, c2 = st.columns(2)
    with c1:
        pie_fig = px.pie(
            df,
            names="Prediction",
            title="Session Outcome Distribution",
            color="Prediction",
            color_discrete_map={
                "🔴 Churn": "#FF4B4B",
                "🟢 Stay": "#00E676"
            }
        )
        st.plotly_chart(pie_fig, use_container_width=True)
    with c2:
        if "Contract" in df.columns:
            bar_fig = px.histogram(
                df,
                x="Contract",
                color="Prediction",
                barmode="group",
                title="Predictions by Contract Type",
                color_discrete_map={
                    "🔴 Churn": "#FF4B4B",
                    "🟢 Stay": "#00E676"
                }
            )
            st.plotly_chart(bar_fig, use_container_width=True)

    st.markdown("### 📜 Prediction Log")
    st.dataframe(df, use_container_width=True, hide_index=True)
