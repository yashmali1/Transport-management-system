import streamlit as st
import pandas as pd
from datetime import datetime

st.title("🚚 Transport Bhada & Profit Tracker")

# Set Hemmal's simple password (don't use in real prod apps!)
HEMMAL_PASSWORD = "1234"  # change this to something secure

# Session state to store data
if 'data' not in st.session_state:
    st.session_state.data = []

# Form to add new entry
with st.form("bhada_form"):
    shop_name = st.text_input("🛍️ Shop Name", placeholder="Enter the shop name")
    date = st.date_input("📅 Date", datetime.today())
    bhada = st.number_input("💰 Bhada (₹)", min_value=0.01, format="%.2f", placeholder="Enter Bhada")  # Added placeholder
    profit_percent = st.number_input("📈 Your Profit (%)", min_value=0.01, max_value=100.0, format="%.2f", placeholder="Enter Profit %")  # Added placeholder

    submitted = st.form_submit_button("Add Entry")
    if submitted and shop_name and bhada > 0:
        profit = (bhada * profit_percent) / 100
        entry = {
            "Date": date.strftime("%Y-%m-%d"),
            "Shop": shop_name,
            "Bhada (₹)": bhada,
            "Profit %": profit_percent,
            "Your Profit (₹)": round(profit, 2),
            "Status": "⏳ Pending"
        }
        st.session_state.data.append(entry)
        st.success("✅ Entry added!")

# Show password input for Hemmal
st.subheader("🔐 Hemmal Login to Update")
hem_pass = st.text_input("Enter password to update entries", type="password")
is_hemmal = hem_pass == HEMMAL_PASSWORD

# Show table with Update & Delete options
if st.session_state.data:
    st.subheader("📊 All Entries")

    for i, row in enumerate(st.session_state.data):
        cols = st.columns([2, 2, 1.5, 1.5, 1.5, 1.5, 2])

        cols[0].write(row["Date"])
        cols[1].write(row["Shop"])
        cols[2].write(f"₹{row['Bhada (₹)']}")
        cols[3].write(f"{row['Profit %']}%")
        cols[4].write(f"₹{row['Your Profit (₹)']}")
        cols[5].write(row["Status"])

        # Update button (only if logged in as Hemmal)
        if is_hemmal:
            if cols[6].button("✅ Mark Delivered", key=f"delivered_{i}"):
                st.session_state.data[i]["Status"] = "✅ Delivered"
                st.rerun()

        # Delete button (only if Hemmal)
        if is_hemmal:
            if cols[6].button("🗑️ Delete", key=f"delete_{i}"):
                st.session_state.data.pop(i)
                st.rerun()

    # Option to download CSV
    df = pd.DataFrame(st.session_state.data)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download CSV", csv, "transport_data.csv", "text/csv")
