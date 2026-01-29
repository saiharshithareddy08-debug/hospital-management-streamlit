import streamlit as st
from database import get_conn

def prescription_ui(user):
    if user[3] != "Doctor":
        return

    st.subheader("Prescriptions")

    p = st.text_input("Patient", key="pres_patient")
    d = st.text_area("Diagnosis", key="pres_diag")
    m = st.text_area("Medicines", key="pres_meds")

    if st.button("Save Prescription", key="pres_btn"):
        conn = get_conn()
        conn.execute(
            "INSERT INTO prescriptions VALUES (NULL,?,?,?,?)",
            (p, user[1], d, m)
        )
        conn.commit()
        st.success("Prescription saved")
