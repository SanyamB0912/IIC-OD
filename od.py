import streamlit as st
from supabase import create_client, Client
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL="https://qyukrrodgynfbjvxknsw.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InF5dWtycm9kZ3luZmJqdnhrbnN3Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzkzNDcwNTcsImV4cCI6MjA1NDkyMzA1N30.mia7QJ7uRrZMoOEohgw7cTNLLYz_D1fFGQURZhpbuE0"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

st.title("OD Form")

# Form for user input
with st.form("attendance_form"):
    name = st.text_input("Name")
    department = st.text_input("Department")
    roll_number = st.text_input("Roll Number")
    date = st.date_input("Date", datetime.date.today())
    lecture_numbers = st.text_area("Lecture Numbers (comma separated)")
    submit_button = st.form_submit_button("Submit")

# Handling form submission
if submit_button:
    if not name or not department or not roll_number or not lecture_numbers:
        st.error("Please fill all fields before submitting.")
    else:
        # Check if an entry already exists for the same roll number and date
        existing_entry = (
            supabase.table("attendance")
            .select("*")
            .eq("roll_number", roll_number)
            .eq("date", str(date))
            .execute()
        )
        
        if existing_entry.data:
            st.warning("An entry for this roll number already exists on this date.")
        else:
            data = {
                "name": name,
                "department": department,
                "roll_number": roll_number,
                "date": str(date),
                "lecture_numbers": lecture_numbers
            }
            response = supabase.table("attendance").insert([data]).execute()
            
            if response.data:
                st.success("Data submitted successfully!")
            else:
                st.error("Error submitting data. Please try again.")
