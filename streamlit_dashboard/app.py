import streamlit as st
import pandas as pd
import requests
import plotly.express as px


# =================================
# PAGE CONFIGURATION
# =================================

st.set_page_config(
    page_title="EMS Dashboard",
    page_icon="👨‍💼",
    layout="wide"
)


# =================================
# DASHBOARD HEADER
# =================================

st.title("👨‍💼 Employee Management System")
st.caption("Employee Overview & Analytics Dashboard")

st.divider()


# =================================
# FETCH DATA FROM FASTAPI
# =================================

API_URL = "http://127.0.0.1:8000/employees"


@st.cache_data(ttl=30)
def fetch_employees():

    response = requests.get(API_URL, timeout=10)
    response.raise_for_status()

    return response.json()


# =================================
# SIDEBAR
# =================================

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    ["Dashboard", "Employee Details"]
)


# =================================
# LOAD EMPLOYEE DATA
# =================================

try:

    employees = fetch_employees()

    df = pd.DataFrame(employees)

    if df.empty:
        st.info("No employee records found.")
        st.stop()  #stop the execution of entire script

    # =================================
    # DASHBOARD PAGE
    # =================================

    if page == "Dashboard":

        st.subheader("Dashboard Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                label="Total Employees",
                value=len(df)
            )

        with col2:
            st.metric(
                label="Total Designations",
                value=df["designation"].nunique()
            )

        st.divider()

        st.subheader("Employee Distribution by Designation")

        designation_counts = (
            df["designation"]
            .value_counts()
            .reset_index()
        )

        designation_counts.columns = [
            "Designation",
            "Employee Count"
        ]

        fig = px.bar(
            designation_counts,
            x="Designation",
            y="Employee Count",
            color="Designation",
            title="Employees per Designation"
        )

        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Recent Employee Records")

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

    # =================================
    # EMPLOYEE DETAILS PAGE
    # =================================

    elif page == "Employee Details":

        st.subheader("Employee Directory")

        search = st.text_input("Search employee by name")

        if search:
            filtered_df = df[
                df["ename"].str.contains(
                    search,
                    case=False,
                    na=False
                )
            ]
        else:
            filtered_df = df

        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True
        )


except requests.exceptions.RequestException as e:

    st.error(
        "Unable to connect to FastAPI. "
        "Please make sure the backend is running."
    )

    st.caption(f"Connection details: {e}")
