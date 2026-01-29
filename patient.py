import streamlit as st
from database import get_conn

def patient_dashboard(user):
    conn = get_conn()
    username = user[1]
    role = user[3]

    st.subheader("📊 Dashboard")

    if role == "Patient":
        appts = conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE patient=?",
            (username,)
        ).fetchone()[0]

        reports = conn.execute(
            "SELECT COUNT(*) FROM lab_reports WHERE patient=?",
            (username,)
        ).fetchone()[0]

        bills = conn.execute(
            "SELECT COUNT(*) FROM bills WHERE patient=?",
            (username,)
        ).fetchone()[0]

        col1, col2, col3 = st.columns(3)
        col1.metric("Appointments", appts)
        col2.metric("Lab Reports", reports)
        col3.metric("Bills", bills)

    elif role == "Doctor":
        appts = conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE doctor=?",
            (username,)
        ).fetchone()[0]
        st.metric("Your Appointments", appts)

    elif role == "Receptionist":
        bills = conn.execute("SELECT COUNT(*) FROM bills").fetchone()[0]
        st.metric("Total Bills", bills)

    elif role == "Lab Technician":
        reports = conn.execute("SELECT COUNT(*) FROM lab_reports").fetchone()[0]
        st.metric("Total Lab Reports", reports)
