import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


# ================= RISK GAUGE ================= #

def risk_gauge(probability):

    fig = go.Figure(go.Indicator(

        mode="gauge+number",

        value=probability * 100,

        number={"suffix": "%"},

        title={"text": "<b>Customer Churn Risk</b>"},

        gauge={

            "axis": {"range": [0, 100]},

            "bar": {"color": "#00E676"},

            "steps": [

                {"range": [0, 35], "color": "#00C853"},

                {"range": [35, 70], "color": "#FFD600"},

                {"range": [70, 100], "color": "#FF1744"}

            ],

            "threshold": {

                "line": {"color": "white", "width": 4},

                "thickness": 0.8,

                "value": probability * 100

            }

        }

    ))

    fig.update_layout(

        height=350,

        paper_bgcolor="#0E1117",

        font=dict(color="white", size=16)

    )

    return fig


# ================= DASHBOARD ================= #

def show_dashboard(probability, model, feature_names):

    st.markdown("---")
    st.header("📊 Customer Analytics Dashboard")

    # ---------------- KPI SUMMARY ---------------- #

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "📈 Retention",
            f"{(1-probability)*100:.1f}%"
        )

    with c2:
        st.metric(
            "⚠ Risk",
            f"{probability*100:.1f}%"
        )

    with c3:
        st.metric(
            "🤖 AI Status",
            "Active"
        )

    st.write("")

    # ---------------- DONUT + GAUGE ---------------- #

    col1, col2 = st.columns(2)

    with col1:

        fig = px.pie(

            values=[
                probability * 100,
                (1 - probability) * 100
            ],

            names=[
                "Churn",
                "Stay"
            ],

            hole=0.70,

            color=[
                "Churn",
                "Stay"
            ],

            color_discrete_map={
                "Churn": "#FF4B4B",
                "Stay": "#00E676"
            }

        )

        fig.update_layout(

            title="Customer Status",

            paper_bgcolor="#0E1117",

            plot_bgcolor="#0E1117",

            font_color="white",

            height=420

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        gauge = risk_gauge(probability)

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    st.markdown("---")

    # ---------------- FEATURE IMPORTANCE ---------------- #

    st.subheader("🔥 Top Factors Affecting Churn")

    # Logistic Regression coefficients & impact direction
    coefs = model.coef_[0]

    feature_df = pd.DataFrame({
        "Feature": feature_names,
        "Coefficient": coefs,
        "Importance": [abs(c) for c in coefs],
        "Impact": [
            "Increases Churn (Risk)" if c > 0 else "Decreases Churn (Retention)"
            for c in coefs
        ]
    })

    # Clean feature names BEFORE creating the plot
    feature_df["Feature"] = (
        feature_df["Feature"]
        .str.replace("_", " ", regex=False)
        .str.replace("Yes", "", regex=False)
        .str.replace("No internet service", "No Internet", regex=False)
        .str.replace("No phone service", "No Phone", regex=False)
        .str.strip()
    )

    # Top 10 features by absolute importance
    top_features = feature_df.sort_values(
        by="Importance",
        ascending=False
    ).head(10)

    fig = px.bar(
        top_features,
        x="Importance",
        y="Feature",
        orientation="h",
        color="Impact",
        color_discrete_map={
            "Increases Churn (Risk)": "#FF4B4B",
            "Decreases Churn (Retention)": "#00E676"
        },
        text="Importance",
        title="Top 10 Feature Drivers (Red = Churn Risk, Green = Retention Driver)"
    )

    fig.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font_color="white",
        height=500,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        yaxis=dict(categoryorder="total ascending", title="")
    )

    fig.update_traces(
        texttemplate="%{text:.3f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown("---")

    # ---------------- AI INSIGHTS ---------------- #

    st.subheader("🤖 AI Insights")

    if probability >= 0.70:

        st.error("""
### High Churn Risk

• Customer has a very high probability of leaving.

• Recommend immediate retention campaign.

• Offer discounts or loyalty rewards.

• Personal customer support is advised.
""")

    elif probability >= 0.35:

        st.warning("""
### Medium Churn Risk

• Customer should be monitored.

• Offer personalized plans.

• Increase engagement through promotions.
""")

    else:

        st.success("""
### Low Churn Risk

• Customer is loyal.

• Continue current service quality.

• Offer premium services and rewards.
""")
