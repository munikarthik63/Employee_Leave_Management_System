
import streamlit as st
import pandas as pd
from database import conn, cursor

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Employee Leave Management System",
    page_icon="🏢",
    layout="wide"
)

st.title("🏢 Employee Leave Management System")

# -----------------------------
# Sidebar Navigation
# -----------------------------
menu = st.sidebar.selectbox(
    "📂 Navigation",
    ["Employee", "Admin"]
)

# ======================================================
# EMPLOYEE MODULE
# ======================================================
if menu == "Employee":

    st.header("📝 Apply for Leave")

    with st.form("leave_form"):

        employee_name = st.text_input("Employee Name")

        department = st.selectbox(
            "Department",
            ["HR", "IT", "Finance", "Sales", "Marketing"]
        )

        leave_type = st.selectbox(
            "Leave Type",
            ["Casual Leave", "Sick Leave", "Earned Leave"]
        )

        start_date = st.date_input("Start Date")

        end_date = st.date_input("End Date")

        reason = st.text_area("Reason")

        submit = st.form_submit_button("Apply Leave")

    if submit:

        cursor.execute("""
        INSERT INTO leaves(
            employee_name,
            department,
            leave_type,
            start_date,
            end_date,
            reason,
            status
        )
        VALUES (?,?,?,?,?,?,?)
        """,
        (
            employee_name,
            department,
            leave_type,
            str(start_date),
            str(end_date),
            reason,
            "Pending"
        ))

        conn.commit()

        st.success("✅ Leave Applied Successfully!")

        st.balloons()

# ======================================================
# ADMIN MODULE
# ======================================================
elif menu == "Admin":

    st.header("👨‍💼 Admin Dashboard")

    df = pd.read_sql("SELECT * FROM leaves", conn)

    # -----------------------------
    # Dashboard Statistics
    # -----------------------------
    total = len(df)

    pending = len(df[df["status"] == "Pending"])

    approved = len(df[df["status"] == "Approved"])

    rejected = len(df[df["status"] == "Rejected"])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("📋 Total", total)
    col2.metric("🟡 Pending", pending)
    col3.metric("🟢 Approved", approved)
    col4.metric("🔴 Rejected", rejected)

    st.divider()

    # -----------------------------
    # Leave Requests Table
    # -----------------------------
    st.subheader("📄 Leave Requests")

    st.dataframe(df, use_container_width=True)

    st.divider()

    # -----------------------------
    # Update Leave Status
    # -----------------------------
    st.subheader("✏️ Update Leave Status")

    leave_id = st.number_input(
        "Enter Leave ID",
        min_value=1,
        step=1
    )

    action = st.selectbox(
        "Select Status",
        ["Approved", "Rejected"]
    )

    if st.button("Update Status"):

        cursor.execute(
            "UPDATE leaves SET status=? WHERE id=?",
            (action, leave_id)
        )

        conn.commit()

        st.success("✅ Status Updated Successfully!")

        st.rerun()
