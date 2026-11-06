import os
import pandas as pd
import streamlit as st

# የገጽ አቀማመጥ እና ስም ማስተካከል
st.set_page_config(
    page_title="የዕለታዊ የስምሪት እና ፍሊት ማኔጅመንት",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# የዳታ ፋይል ስም (መረጃዎችን በ CSV መልክ ያስቀምጣል)
DATA_FILE = "dispatch_data.csv"

# ፋይሉ ከሌለ አዲስ መነሻ ዳታ ማዘጋጀት
if not os.path.exists(DATA_FILE):
    initial_data = pd.DataFrame(
        columns=[
            "ወር",
            "የአሽከርካሪው ስም",
            "የመኪና ሰሌዳ",
            "የተነሳበትና መድረሻ",
            "የካርጎ አይነት",
            "የተሰጠ ነዳጅ (ሊትር)",
            "የተጓዘው ኪ.ሜ",
            "የጫነው ኩንታል",
            "የስምሪት ሁኔታ",
        ]
    )
    initial_data.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ዋና ርዕስ
st.title("🚚 የዕለታዊ የስምሪት መከታተያ ዳሽቦርድ")
st.write("የመኪናዎችን ጉዞ፣ ጭነት፣ ነዳጅ እና ወርሃዊ ሪፖርት መከታተያ ሲስተም")

# ዳታውን መጫን
df = load_data()

# --- 1. አጠቃላይ ማጠቃለያ (Metrics Dashboard) ---
st.subheader("📊 አጠቃላይ ማጠቃለያ (Dashboard)")
if not df.empty:
    total_km = df["የተጓዘው ኪ.ሜ"].sum() if "የተጓዘው ኪ.ሜ" in df.columns else 0
    total_quintal = df["የጫነው ኩንታል"].sum() if "የጫነው ኩንታል" in df.columns else 0
    total_fuel = df["የተሰጠ ነዳጅ (ሊትር)"].sum() if "የተሰጠ ነዳጅ (ሊትር)" in df.columns else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("ጠቅላላ የተጓዘው ኪ.ሜ", f"{total_km:,.1f} ኪ.ሜ")
    col2.metric("ጠቅላላ የጫነው ኩንታል", f"{total_quintal:,.1f} ኩንታል")
    col3.metric("ጠቅላላ የተሰጠ ነዳጅ", f"{total_fuel:,.1f} ሊትር")

# --- 2. አዲስ መረጃ ማስገቢያ ፎርም (Sidebar Form) ---
st.sidebar.header("➕ አዲስ ስምሪት መዝግብ")

# የኢትዮጵያ ወራት ዝርዝር
ethiopian_months = [
    "መስከረም", "ጥቅምት", "ህዳር", "ታህሳስ", 
    "ጥር", "የካቲት", "መጋቢት", "ሚያዝያ", 
    "ግንቦት", "ሰኔ", "ሐምሌ", "ነሐሴ", "ጳጉሜ"
]

with st.sidebar.form("vehicle_log_form"):
    selected_month = st.selectbox("ወር ይምረጡ", ethiopian_months)
    driver_name = st.text_input("የአሽከርካሪው ስም")
    plate_number = st.text_input("የመኪና ሰሌዳ (e.g. AA 3-12345)")
    route = st.text_input("የተነሳበትና መድረሻ (e.g. አዲስ አበባ ⟼ ጅማ)")
    cargo_type = st.text_input("የካርጎ አይነት (e.g. ሲሚንቶ)")
    
    fuel_liters = st.number_input("የተሰጠ ነዳጅ (ሊትር)", min_value=0.0, value=0.0)
    distance_km = st.number_input("የተጓዘው ኪሎሜትር (KM)", min_value=0.0, value=0.0)
    quintals = st.number_input("የጫነው ኩንታል", min_value=0.0, value=0.0)
    
    status = st.selectbox("የስምሪት ሁኔታ", ["ጉዞ ላይ (In Transit)", "ደረሰ (Delivered)", "ጋራጅ (In Garage)"])
    
    submit_button = st.form_submit_button("መረጃውን መዝግብ")
    
    if submit_button:
        if plate_number and driver_name:
            new_row = pd.DataFrame({
                "ወር": [selected_month],
                "የአሽከርካሪው ስም": [driver_name],
                "የመኪና ሰሌዳ": [plate_number],
                "የተነሳበትና መድረሻ": [route],
                "የካርጎ አይነት": [cargo_type],
                "የተሰጠ ነዳጅ (ሊትር)": [fuel_liters],
                "የተጓዘው ኪ.ሜ": [distance_km],
                "የጫነው ኩንታል": [quintals],
                "የስምሪት ሁኔታ": [status]
            })
            df = pd.concat([df, new_row], ignore_index=True)
            save_data(df)
            st.sidebar.success("መረጃው በተሳካ ሁኔታ ተመዝግቧል!")
            st.rerun()
        else:
            st.sidebar.error("እባክዎ የአሽከርካሪውን ስም እና የመኪና ሰሌዳ ያስገቡ!")

# --- 3. የተመዘገቡ መረጃዎች ሰንጠረዥ ---
st.subheader("📋 የተመዘገቡ ስምሪቶች ዝርዝር")
if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("እስካሁን የተመዘገበ መረጃ የለም። ከጎን ካለው ፎርም መረጃ ያስገቡ።")

# --- 4. ለእያንዳንዱ መኪና እና ወር የሪፖርት ማጠቃለያ ---
st.subheader("📑 ለእያንዳንዱ መኪና ወርሃዊ ሪፖርት ማጠቃለያ")
if not df.empty and "የመኪና ሰሌዳ" in df.columns:
    # በወር እና በመኪና ሰሌዳ ከፋፍሎ ማጠቃለያ ማሳየት
    summary_df = df.groupby(["ወር", "የመኪና ሰሌዳ"])[["የተጓዘው ኪ.ሜ", "የጫነው ኩንታል", "የተሰጠ ነዳጅ (ሊትር)"]].sum().reset_index()
    st.dataframe(summary_df, use_container_width=True)
