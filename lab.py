import streamlit as st
from database import get_conn
from pdf_utils import generate_lab_report_pdf

def lab_ui(user):
    conn = get_conn()
    role = user[3]
    username = user[1]

    st.subheader("🧪 Lab Reports")

    # 🔬 LAB TECHNICIAN → CREATE REPORT
    if role == "Lab Technician":
        patient = st.text_input("Patient Username", key="lab_patient")
        test = st.text_input("Test Name", key="lab_test")
        result = st.text_area("Result", key="lab_result")

        if st.button("Save Lab Report", key="lab_btn"):
            conn.execute(
                "INSERT INTO lab_reports VALUES (NULL,?,?,?)",
                (patient, test, result)
            )
            conn.commit()
            st.success("Lab report added")

    # 👀 PATIENT → VIEW ONLY OWN REPORTS
    if role == "Patient":
        reports = conn.execute(
            "SELECT test, result FROM lab_reports WHERE patient=?",
            (username,)
        ).fetchall()

        if reports:
            for test, result in reports:
                st.write(f"Test: {test}")
                st.write(f"Result: {result}")

                if st.button("Download Lab Report PDF", key=f"lab_pdf_{test}"):
                    pdf_path = generate_lab_report_pdf(username, test, result)

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download",
                            data=f,
                            file_name="lab_report.pdf",
                            mime="application/pdf"
                        )
        else:
            st.info("No lab reports found")


    elif role == "Doctor":
        # Doctor sees lab reports only for their patients
        reports = conn.execute("""
            SELECT l.patient, l.test, l.result
            FROM lab_reports l
            JOIN appointments a ON l.patient = a.patient
            WHERE a.doctor = ?
        """, (username,)).fetchall()

        st.table(reports) if reports else st.info("No lab reports for your patients")