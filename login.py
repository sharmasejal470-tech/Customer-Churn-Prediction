import streamlit as st


def login():

    st.markdown(
        "<h1 style='text-align:center;'>🔐 Customer Analytics Portal</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<h4 style='text-align:center;color:gray;'>Secure Login</h4>",
        unsafe_allow_html=True
    )

    st.write("")

    username = st.text_input("👤 Username")

    password = st.text_input(
        "🔑 Password",
        type="password"
    )

    st.write("")

    if st.button(
        "🚀 Login",
        use_container_width=True
    ):

        if username.strip().lower() == "sejal" and password == "1234":

            st.session_state.logged_in = True

            st.success("Login Successful!")

            st.rerun()

        else:

            st.error("Invalid Username or Password")
