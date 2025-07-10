import streamlit as st
import requests

st.set_page_config(page_title="HR Query Chatbot", page_icon="💼")
st.title("💼 HR Resource Query Chatbot")

# 🔍 Chat section
st.subheader("Ask a Question")
query = st.text_input("E.g., Find Python developers with 3+ years experience")

if st.button("Submit Query") and query:
    with st.spinner("Searching..."):
        res = requests.post("http://localhost:8000/chat", json={"question": query})
        if res.status_code == 200:
            st.success(res.json()["response"])
        else:
            st.error("Backend Error")

# ➕ Add employee
st.markdown("---")
st.subheader("Add New Employee")

with st.form("add_form"):
    name = st.text_input("Name")
    skills = st.text_input("Skills (comma separated)")
    experience = st.number_input("Experience (years)", 0, 50)
    projects = st.text_input("Projects (comma separated)")
    availability = st.selectbox("Availability", ["available", "unavailable"])
    submit = st.form_submit_button("Add Employee")

    if submit:
        data = {
            "name": name,
            "skills": [s.strip() for s in skills.split(",")],
            "experience_years": experience,
            "projects": [p.strip() for p in projects.split(",")],
            "availability": availability
        }
        res = requests.post("http://localhost:8000/employees/add", json=data)
        if res.status_code == 200:
            st.success(res.json()["message"])
        else:
            st.error("Error adding employee")
