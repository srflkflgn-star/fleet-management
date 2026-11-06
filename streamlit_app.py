
import os
import pandas as pd
import streamlit as st

# ገጹ በስልክም ሆነ በኮምፒውተር እንዲመች ማድረግ
st.set_page_config(
    page_title="የስምሪት እና የፍሊት ማኔጅመንት",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# የዳታቤዝ ፋይል ስም (መረጃዎችን በኤክሰል/CSV መልክ ያስቀምጣል)
DATA_FILE = "dispatch_data.csv"

# ፋይሉ ከሌለ አዲስ መፍጠሪያ
if not os.path.exists(DATA_FILE):
    initial_data = pd.DataFrame(
        columns=[
            "የመኪና ሰሌዳ",
            "የአሽከርካሪ ስም",
            "የተነሳበትና መድረሻ",
            "ካርጎ",
            "ነዳጅ (ሊትር)",
            "ሁኔታ",
        ]
    )
    initial_data.to_csv(DATA_FILE, index=False)


def load_data():
    return pd.read_csv(DATA_FILE)


def save_data(df):
    df.to_csv(DATA_FILE, index=False)


# ዋና ርዕስ
st.title("🚛 የዕለታዊ የስምሪት መከታተያ ዳሽቦርድ")
st.write("በስልክ እና በኮምፒውተር በቀላሉ የሚሰራ የፍሊት ማኔጅመንት አፕሊኬሽን")

# Sidebar - አዲስ ስምሪት መመዝገቢያ
st.sidebar.header("📝 አዲስ ስምሪት መዝግብ")
with st.sidebar.form("dispatch_form", clear_on_submit=True):
    plate_no = st.text_input("የመኪና ሰሌዳ ቁጥር (e.g. AA 3-12345)")
    driver_name = st.text_input("የአሽከርካሪ ስም")
    route = st.text_input("የተነሳበትና መድረሻ (e.g. አዲስ አበባ ➔ ጂቡቲ)")
    cargo = st.text_input("የካርጎ ዓይነት (e.g. ቡቲ 25 ቶን)")
    fuel = st.number_input("የተሰጠ ነዳጅ (በሊትር)", min_value=0, value=100)
    status = st.selectbox(
        "የስምሪት ሁኔታ",
        [
            "መንገድ ላይ (In Transit)",
            "ዝግጁ (Available)",
            "ጥገና ላይ (Maintenance)",
        ],
    )

    submitted = st.form_submit_button("💾 ስምሪት መዝግብ")

    if submitted and plate_no and driver_name:
        df = load_data()
        new_row = {
            "የመኪና ሰሌዳ": plate_no,
            "የአሽከርካሪ ስም": driver_name,
            "የተነሳበትና መድረሻ": route,
            "ካርጎ": cargo,
            "ነዳጅ (ሊትር)": fuel,
            "ሁኔታ": status,
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("መረጃው በስኬት ተመዝግቧል!")

# መረጃዎችን ማሳያ
df_data = load_data()

# የቁጥር ማጠቃለያ (Metrics)
col1, col2, col3, col4 = st.columns(4)
in_transit = len(
    df_data[df_data["ሁኔታ"] == "መንገድ ላይ (In Transit)"]
)
available = len(df_data[df_data["ሁኔታ"] == "ዝግጁ (Available)"])
maintenance = len(df_data[df_data["ሁኔታ"] == "ጥገና ላይ (Maintenance)"])
total_fuel = df_data["ነዳጅ (ሊትር)"].sum() if not df_data.empty else 0

col1.metric("መንገድ ላይ ያሉ", f"{in_transit} መኪኖች")
col2.metric("ዝግጁ የሆኑ", f"{available} መኪኖች")
col3.metric("ጥገና ላይ ያሉ", f"{maintenance} መኪኖች")
col4.metric("ጠቅላላ የተሰጠ ነዳጅ", f"{total_fuel} ሊትር")

st.divider()

# የዳታ ሰንጠረዥ ማሳያ
st.subheader("📋 የተመዘገቡ የስምሪት መረጃዎች")
st.dataframe(df_data, use_container_width=True)

# በኤክሰል ማውረጃ (Export to Excel/CSV)
if not df_data.empty:
    csv = df_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 መረጃዎችን በ Excel (CSV) አውርድ",
        data=csv,
        file_name="dispatch_report.csv",
        mime="text/csv",
    )
class FleetManager:
    def __init__(self):
        # የመኪና መረጃዎችን ለመያዝ የሚረዳ ዝርዝር (List)
        self.vehicle_logs = []

    def add_log(self, plate_number, distance, quintal, fuel, month):
        """አዲስ የጉዞ እና የጭነት መረጃ የሚመዘግብበት ፍንክሽን"""
        log = {
            "plate_number": plate_number,
            "distance": float(distance),
            "quintal": float(quintal),
            "fuel": float(fuel),
            "month": month
        }
        self.vehicle_logs.append(log)
        print(f"✅ የመኪና ቁጥር {plate_number} መረጃ በተሳካ ሁኔታ ተመዝግቧል!")

    def show_total_summary(self):
        """አጠቃላይ የተጓዘውን ኪሎሜትር እና የጫነውን ኩንታል ያሳያል"""
        total_km = sum(log["distance"] for log in self.vehicle_logs)
        total_quintal = sum(log["quintal"] for log in self.vehicle_logs)
        total_fuel = sum(log["fuel"] for log in self.vehicle_logs)

        print("\n--- 📊 አጠቃላይ የፍሊት ማጠቃለያ ---")
        print(f"ጠቅላላ የተጓዘው ኪሎሜትር: {total_km} ኪ.ሜ")
        print(f"ጠቅላላ የተጫነው ጭነት: {total_quintal} ኩንታል")
        print(f"ጠቅላላ የተጠቀመው ነዳጅ: {total_fuel} ሊትር")

    def generate_monthly_report(self):
        """እያንዳንዱ መኪና በወር ውስጥ የጠቀመውን ነዳጅ እና የጫነውን ኩንታል በሪፖርት መልክ ያሳያል"""
        report = {}

        for log in self.vehicle_logs:
            plate = log["plate_number"]
            if plate not in report:
                report[plate] = {"distance": 0.0, "quintal": 0.0, "fuel": 0.0}
            
            report[plate]["distance"] += log["distance"]
            report[plate]["quintal"] += log["quintal"]
            report[plate]["fuel"] += log["fuel"]

        print("\n--- 📑 ለእያንዳንዱ መኪና ወርሃዊ ሪፖርት ---")
        print(f"{'የመኪና ሰሌዳ':<15} | {'ጠቅላላ ኪ.ሜ':<12} | {'ጠቅላላ ኩንታል':<15} | {'ጠቅላላ ነዳጅ (ሊትር)':<18}")
        print("-" * 65)
        for plate, data in report.items():
            print(f"{plate:<15} | {data['distance']:<12} | {data['quintal']:<15} | {data['fuel']:<18}")

# --- የኮዱ አጠቃቀም ማሳያ (Test) ---
if __name__ == "__main__":
    manager = FleetManager()

    # 1. መረጃዎችን ማስገባት (ምሳሌ)
    manager.add_log(plate_number="ET-3-12345", distance=450, quintal=120, fuel=60, month="ህዳር")
    manager.add_log(plate_number="ET-3-12345", distance=300, quintal=90, fuel=40, month="ህዳር")
    manager.add_log(plate_number="ET-4-98765", distance=600, quintal=150, fuel=85, month="ህዳር")

    # 2. አጠቃላይ ድምር ማሳያ
    manager.show_total_summary()

    # 3. ወርሃዊ ሪፖርት ማሳያ
    manager.generate_monthly_report()
