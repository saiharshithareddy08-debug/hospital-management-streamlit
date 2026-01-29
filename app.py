import streamlit as st
# ---- IMPORT MODULES ----
from database import create_tables
from auth import login, register
from appointment import appointment_ui
from lab import lab_ui
from billing import billing_ui
from patient import patient_dashboard
from dashboard import patient_dashboard

# ---- INITIAL SETUP ----
st.set_page_config(
    page_title="Hospital Management System",
    page_icon="🏥",
    layout="wide"
)

create_tables()

st.title("🏥 Hospital Management System")

# ---- NOT LOGGED IN ----
if "user" not in st.session_state:

    menu = st.sidebar.selectbox(
        "Menu",
        ["Login", "Register"],
        key="auth_menu"
    )

    if menu == "Login":
        login()
    else:
        register()

# ---- LOGGED IN ----
else:
    user = st.session_state["user"]
    username = user[1]
    role = user[3]

    # -------- SIDEBAR --------
    with st.sidebar:
        st.title("🏥 HMS")

        st.subheader("👤 User Info")
        st.write(username)
        st.write(f"Role: {role}")

        st.markdown("---")
        st.subheader("Navigation")

        if role == "Doctor":
            menu = st.radio(
                "",
                ["Dashboard", "Appointments", "Lab Reports"],
                key="menu_doctor"
            )

        elif role == "Lab Technician":
            menu = st.radio(
                "",
                ["Dashboard", "Lab Reports"],
                key="menu_lab"
            )

        elif role == "Receptionist":
            menu = st.radio(
                "",
                ["Dashboard", "Appointments", "Billing"],
                key="menu_reception"
            )

        else:  # Patient
            menu = st.radio(
                "",
                ["Dashboard", "Appointments", "Lab Reports", "Billing"],
                key="menu_patient"
            )

        st.markdown("---")

        if st.button("Logout", key="logout_btn"):
            del st.session_state["user"]
            st.rerun()


# ---------------- MAIN PAGE CONTENT (OUTSIDE SIDEBAR) ----------------
# st.title("🏥 Hospital Management System")

if menu == "Dashboard":
    patient_dashboard(user)

elif menu == "Appointments":
    appointment_ui(user)

elif menu == "Lab Reports":
    lab_ui(user)

elif menu == "Billing":
    billing_ui(user)
