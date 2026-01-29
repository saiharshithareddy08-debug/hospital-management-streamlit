import streamlit as st
import bcrypt
from database import get_conn

def register():
    st.subheader("Register")

    u = st.text_input("Username")
    e = st.text_input("Email")
    r = st.selectbox("Role", ["Patient", "Doctor", "Receptionist", "Lab Technician"],
    key="reg_role")
    p = st.text_input("Password", type="password")

    if st.button("Register"):
        hashed = bcrypt.hashpw(p.encode(), bcrypt.gensalt())
        conn = get_conn()
        try:
            conn.execute(
                "INSERT INTO users VALUES (NULL,?,?,?,?)",
                (u, hashed, r, e)
            )
            conn.commit()
            st.success("Registration successful")
        except:
            st.error("Username already exists")

def login():
    st.subheader("Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_conn()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?", (u,)
        ).fetchone()

        if user and bcrypt.checkpw(p.encode(), user[2]):
            st.session_state["user"] = user
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid credentials")
