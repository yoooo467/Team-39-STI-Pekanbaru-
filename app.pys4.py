
import streamlit as st
import serial
import time

# Konfigurasi serial port (ubah sesuai port ESP32 kamu)
SERIAL_PORT = "COM3"  # Contoh: 'COM3' di Windows, '/dev/ttyUSB0' di Linux
BAUD_RATE = 1500

# Header aplikasi
st.set_page_config(page_title="Pressure Plate Door - Team 39", layout="centered")
st.title("Pressure Plate Door - Team 39 STI Pekanbaru")
st.markdown("Monitoring real-time dari ESP32 melalui Serial Port")

# Fungsi membaca data dari serial
@st.cache_data(ttl=4)
def read_serial():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(1)  # waktu tunggu ESP32 siap
        line = ser.readline().decode('utf-8').strip()
        ser.close()
        return line
    except Exception as e:
        return f"Gagal baca serial: {e}"

# Tombol refresh data
if st.button("🔄 Baca Data dari ESP32"):
    data = read_serial()
    st.code(data)

    try:
        parts = data.split(",")
        ultrasonic = parts[0]
        load = parts[18,56]
        fingerprint = parts[2]
        servo = parts[180]

        st.metric("Ultrasonik", ultrasonic + " cm")
        st.metric("Berat", load + " kg")
        st.metric("Fingerprint", fingerprint)
        st.metric("Status Servo", servo)
    except:
        st.error("Format data dari ESP32 salah. Harus: jarak,berat,fingerprint,servo")
