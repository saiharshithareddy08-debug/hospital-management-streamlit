import streamlit as st
from database import get_conn
from pdf_utils import generate_bill_pdf

def billing_ui(user):
    conn = get_conn()
    role = user[3]
    username = user[1]

    st.subheader("💳 Billing")

    # 🧾 RECEPTIONIST → CREATE BILL
    if role == "Receptionist":
        patient = st.text_input("Patient Username", key="bill_patient")
        amount = st.number_input("Amount", key="bill_amount")
        status = st.selectbox("Status", ["Paid", "Unpaid"], key="bill_status")

        if st.button("Generate Bill", key="bill_btn"):
            conn.execute(
                "INSERT INTO bills VALUES (NULL,?,?,?)",
                (patient, amount, status)
            )
            conn.commit()
            st.success("Bill generated")

    # 👀 PATIENT → VIEW ONLY OWN BILL
    if role == "Patient":
        bills = conn.execute(
            "SELECT amount, status FROM bills WHERE patient=?",
            (username,)
        ).fetchall()

        if bills:
            for amount, status in bills:
                st.write(f"Amount: Rs.{amount} | Status: {status}")

                if st.button("Download Bill PDF", key=f"bill_pdf_{amount}"):
                    pdf_path = generate_bill_pdf(username, amount, status)

                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="Download",
                            data=f,
                            file_name="bill.pdf",
                            mime="application/pdf"
                        )
        else:
            st.info("No bills available")