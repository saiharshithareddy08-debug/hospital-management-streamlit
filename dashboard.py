import streamlit as st
from database import get_conn


def patient_dashboard(user):
    role = user[3]
    username = user[1]
    conn = get_conn()

    # ---------------- DOCTOR DASHBOARD ----------------
    if role == "Doctor":
        st.subheader("🧑‍⚕️ Doctor Dashboard")

        total_appts = conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE doctor=?",
            (username,)
        ).fetchone()[0]

        pending_appts = conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE doctor=? AND status='Pending'",
            (username,)
        ).fetchone()[0]

        approved_appts = conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE doctor=? AND status='Approved'",
            (username,)
        ).fetchone()[0]

        lab_reports = conn.execute("""
            SELECT COUNT(*)
            FROM lab_reports l
            JOIN appointments a ON l.patient = a.patient
            WHERE a.doctor=?
        """, (username,)).fetchone()[0]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("📅 Total Appointments", total_appts)
        col2.metric("⏳ Pending", pending_appts)
        col3.metric("✅ Approved", approved_appts)
        col4.metric("🧪 Lab Reports", lab_reports)

        st.markdown("---")
        st.info("Use the sidebar to manage appointments and lab reports.")

    # ---------------- PATIENT DASHBOARD ----------------
    elif role == "Patient":
        st.subheader("👤 Patient Dashboard")
        st.write("Welcome to the Hospital Management System")
        st.write("You can:")
        st.write("• Book appointments")
        st.write("• View lab reports")
        st.write("• View billing details")

    # ---------------- LAB TECHNICIAN DASHBOARD ----------------
    elif role == "Lab Technician":
        st.subheader("🧪 Lab Technician Dashboard")
        st.write("You can:")
        st.write("• Add lab reports")
        st.write("• View existing lab reports")

    # ---------------- RECEPTIONIST DASHBOARD ----------------
    elif role == "Receptionist":
        st.subheader("🧾 Receptionist Dashboard")
        st.write("You can:")
        st.write("• View appointments")
        st.write("• Generate billing")
