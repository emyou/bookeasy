import streamlit as st
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

# Google Sheets Setup
SCOPE = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(CREDS)
SHEET_NAME = "BookEasy"  # Update if your sheet has a different name

# Open Sheet
try:
    sheet = client.open(SHEET_NAME).sheet1
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"Sheet '{SHEET_NAME}' not found. Please create it or check the name.")
    st.stop()

# --- Ensure Headers Exist ---
expected_headers = ['Customer Name', 'Phone Number', 'Job Address', 'Job Datetime', 'Job Notes']
existing_headers = sheet.row_values(1)

if existing_headers != expected_headers:
    sheet.insert_row(expected_headers, 1)

# --- Streamlit UI ---
st.set_page_config(page_title="BookEasy Scheduler", layout="centered")
st.title("📅 BookEasy Job Scheduler")
st.markdown("Schedule appointments and save them to Google Sheets.")

# --- Input Form ---
with st.form("schedule_form"):
    name = st.text_input("Customer Name")
    phone = st.text_input("Phone Number")
    address = st.text_area("Job Address")
    date = st.date_input("Preferred Date", min_value=datetime.today())
    time = st.time_input("Preferred Time")
    notes = st.text_area("Job Notes")
    submitted = st.form_submit_button("Schedule Job")

if submitted:
    scheduled_datetime = datetime.combine(date, time)
    row = [name, phone, address, scheduled_datetime.strftime("%Y-%m-%d %H:%M"), notes]
    sheet.append_row(row)
    st.success(f"✅ Job scheduled for {name} on {scheduled_datetime.strftime('%A, %B %d at %I:%M %p')}")
    st.info(f"📤 SMS reminder would be sent to {phone} (simulated)")

# --- View Scheduled Jobs ---
st.subheader("📋 Upcoming Appointments")
records = sheet.get_all_records()

if records:
    df = pd.DataFrame(records)
    st.dataframe(df)
else:
    st.info("No appointments found.")
