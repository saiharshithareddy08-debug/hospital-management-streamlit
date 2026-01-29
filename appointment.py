import streamlit as st
from database import get_conn
from email_service import send_email

def appointment_ui(user):
    conn = get_conn()
    role = user[3]
    username = user[1]

    st.subheader("📅 Appointments")

    # ---------------- PATIENT ----------------
    if role == "Patient":
        doctors = conn.execute(
            "SELECT username FROM users WHERE role='Doctor'"
        ).fetchall()

        doctor_list = [d[0] for d in doctors]

        selected_doctor = st.selectbox(
            "Select Doctor",
            doctor_list,
            key="appt_doctor"
        )

        date = st.date_input("Appointment Date", key="appt_date")
        email = st.text_input("Your Email", value=user[4], key="appt_email")

        if st.button("Book Appointment", key="appt_btn"):
            conn.execute(
                "INSERT INTO appointments VALUES (NULL,?,?,?,?,?)",
                (username, selected_doctor, str(date), "Pending", email)
            )
            conn.commit()

            send_email(
                email,
                "Hospital Appointment Booked",
                f"""
Hello {username},

Your appointment has been booked successfully.

Doctor: {selected_doctor}
Date: {date}
Status: Pending

Thank you,
Hospital Management System
"""
            )

            st.success("Appointment booked & email sent")

    # ---------------- DOCTOR ----------------
    # ---------------- DOCTOR ----------------
    if role == "Doctor":
        st.subheader("Your Appointments")

        appts = conn.execute(
            "SELECT id, patient, date, status, email FROM appointments WHERE doctor=?",
            (username,)
        ).fetchall()

        for appt in appts:
            appt_id, patient, date, status, patient_email = appt

            with st.expander(f"{patient} | {date} | {status}"):
                col1, col2 = st.columns(2)

                # ✅ APPROVE
                if col1.button("Approve", key=f"approve_{appt_id}"):
                    conn.execute(
                        "UPDATE appointments SET status='Approved' WHERE id=?",
                        (appt_id,)
                    )
                    conn.commit()

                    send_email(
                        patient_email,
                        "Appointment Approved",
                        f"""
    Hello {patient},

    Your appointment with Dr. {username} has been APPROVED.

    📅 Date: {date}

    Thank you,
    Hospital Management System
    """
                    )

                    st.success("Approved & email sent")
                    st.rerun()

                # ❌ REJECT
                if col2.button("Reject", key=f"reject_{appt_id}"):
                    conn.execute(
                        "UPDATE appointments SET status='Rejected' WHERE id=?",
                        (appt_id,)
                    )
                    conn.commit()

                    send_email(
                        patient_email,
                        "Appointment Rejected",
                        f"""
    Hello {patient},

    Your appointment with Dr. {username} has been REJECTED.

    Please book another appointment.

    Thank you,
    Hospital Management System
    """
                    )

                    st.error("Rejected & email sent")
                    st.rerun()


    if role == "Receptionist":
        st.subheader("All Appointments (View Only)")

        appts = conn.execute(
            "SELECT patient, doctor, date, status FROM appointments"
        ).fetchall()

        if appts:
            st.table(appts)
        else:
            st.info("No appointments found")