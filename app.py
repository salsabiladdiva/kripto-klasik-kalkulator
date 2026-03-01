import streamlit as st
from ciphers import (
    vigenere_encrypt, vigenere_decrypt,
    affine_encrypt, affine_decrypt,
    playfair_encrypt, playfair_decrypt,
    hill_encrypt, hill_decrypt,
    enigma_encrypt_decrypt,
)

st.set_page_config(page_title="Kriptografi Klasik Calculator", page_icon="🍭", layout="centered", initial_sidebar_state="collapsed")

# Custom CSS untuk tema hijau muda yang cerah
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700;800&family=Poppins:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary-green: #81C784;
            --light-green-bg: #E8F5E9;
            --dark-green: #2E7D32;
            --soft-white: #F1F8F6;
            --font-elegant: 'Poppins', sans-serif;
            --font-heading: 'Playfair Display', serif;
        }
        
        * {
            font-family: var(--font-elegant) !important;
        }
        
        [data-testid="stMainBlockContainer"] {
            background-color: #F1F8F6;
            padding-top: 2rem;
        }
        
        [data-testid="stAppViewContainer"] {
            background: linear-gradient(135deg, #E8F5E9 0%, #F1F8F6 100%);
        }
        
        [data-testid="stToolbar"] {
            display: none !important;
        }
        
        header {
            display: none !important;
        }
        
        .stToolbar {
            display: none !important;
        }
        
        h1 {
            color: #000000 !important;
            font-family: var(--font-heading) !important;
            font-weight: 700 !important;
            letter-spacing: 0.5px !important;
        }
        
        h2, h3 {
            color: #000000 !important;
            font-family: var(--font-heading) !important;
            font-weight: 600 !important;
            letter-spacing: 0.3px !important;
        }
        
        .stMarkdown {
            color: #000000 !important;
            font-weight: 400 !important;
        }
        
        p {
            color: #000000 !important;
            font-weight: 400 !important;
        }
        
        label {
            color: #000000 !important;
            font-weight: 500 !important;
        }
        
        input, textarea, select {
            color: #000000 !important;
            border-color: #A5D6A7 !important;
            background-color: #F1F8F6 !important;
        }
        
        input[type="number"] {
            background-color: #F1F8F6 !important;
            color: #000000 !important;
            border: 2px solid #A5D6A7 !important;
        }
        
        input[type="number"]:hover {
            background-color: #FFFFFF !important;
            border-color: #81C784 !important;
        }
        
        input[type="number"]:focus {
            background-color: #FFFFFF !important;
            border-color: #2E7D32 !important;
            outline-color: #81C784 !important;
        }
        
        input:focus, textarea:focus, select:focus {
            border-color: #2E7D32 !important;
            outline-color: #81C784 !important;
        }
        
        [data-testid="stButton"] > button {
            background-color: #81C784 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            font-weight: bold !important;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stButton"] > button:hover {
            background-color: #66BB6A !important;
            box-shadow: 0 4px 12px rgba(129, 199, 132, 0.4) !important;
            transform: translateY(-2px) !important;
        }
        
        [data-testid="stTextInput"] > div > div,
        [data-testid="stTextArea"] > div > div,
        [data-testid="stNumberInput"] > div > div {
            background-color: #F1F8F6 !important;
            border: 2px solid #A5D6A7 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 6px rgba(129, 199, 132, 0.1) !important;
        }
        
        [data-testid="stTextInput"] > div > div:hover,
        [data-testid="stTextArea"] > div > div:hover,
        [data-testid="stNumberInput"] > div > div:hover {
            border-color: #81C784 !important;
            box-shadow: 0 4px 12px rgba(129, 199, 132, 0.25) !important;
            background-color: #FFFFFF !important;
            transform: translateY(-2px) !important;
        }
        
        [data-testid="stTextInput"] > div > div:focus-within,
        [data-testid="stTextArea"] > div > div:focus-within,
        [data-testid="stNumberInput"] > div > div:focus-within {
            border-color: #2E7D32 !important;
            box-shadow: 0 0 0 3px rgba(129, 199, 132, 0.2), 0 4px 16px rgba(46, 125, 50, 0.25) !important;
            background-color: #FFFFFF !important;
            transform: translateY(-2px) !important;
        }
        
        [data-testid="stSelectbox"] > div > div {
            background-color: #F1F8F6 !important;
            border: 2px solid #A5D6A7 !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 2px 6px rgba(129, 199, 132, 0.1) !important;
        }
        
        [data-testid="stSelectbox"] div[role="combobox"] {
            color: #000000 !important;
        }
        
        [data-testid="stSelectbox"] > div > div > div {
            color: #000000 !important;
        }
        
        [data-testid="stSelectbox"] option {
            color: #000000 !important;
            background-color: #F1F8F6 !important;
        }
        
        [data-testid="stSelectbox"] > div > div:hover {
            border-color: #81C784 !important;
            box-shadow: 0 4px 12px rgba(129, 199, 132, 0.25) !important;
            background-color: #FFFFFF !important;
            transform: translateY(-2px) !important;
        }
        
        [data-testid="stSelectbox"] > div > div:focus-within {
            border-color: #2E7D32 !important;
            box-shadow: 0 0 0 3px rgba(129, 199, 132, 0.2), 0 4px 16px rgba(46, 125, 50, 0.25) !important;
            background-color: #FFFFFF !important;
            transform: translateY(-2px) !important;
        }
        
        [data-testid="stRadio"] > div {
            background-color: transparent !important;
        }
        
        .st-success {
            background-color: #C8E6C9 !important;
            border-left: 5px solid #81C784 !important;
        }
        
        .st-error {
            background-color: #FFEBEE !important;
            border-left: 5px solid #EF5350 !important;
        }
        
        .stCode {
            background-color: #E0F2F1 !important;
            border: 2px solid #80CBC4 !important;
            border-radius: 6px !important;
        }
        
        hr {
            border-color: #81C784 !important;
            border-width: 2px !important;
            margin: 2rem 0 !important;
        }
        
        .candy-sticker {
            position: fixed;
            font-size: 3rem;
            opacity: 0.4;
            pointer-events: none;
            z-index: 1;
        }
        
        .candy-left-1 {
            left: 10px;
            top: 15%;
            animation: float 4s ease-in-out infinite;
        }
        
        .candy-left-2 {
            left: 5px;
            top: 45%;
            animation: float 5s ease-in-out infinite 0.5s;
        }
        
        .candy-left-3 {
            left: 15px;
            top: 75%;
            animation: float 4.5s ease-in-out infinite 1s;
        }
        
        .candy-right-1 {
            right: 10px;
            top: 20%;
            animation: float 4.2s ease-in-out infinite;
        }
        
        .candy-right-2 {
            right: 8px;
            top: 50%;
            animation: float 5.2s ease-in-out infinite 0.8s;
        }
        
        .candy-right-3 {
            right: 12px;
            top: 80%;
            animation: float 4.8s ease-in-out infinite 1.2s;
        }
        
        @keyframes float {
            0%, 100% {
                transform: translateY(0px) rotate(0deg);
            }
            50% {
                transform: translateY(20px) rotate(5deg);
            }
        }
    </style>
""", unsafe_allow_html=True)

# Tambahkan stiker permen di sisi kiri-kanan
st.markdown("""
    <div class="candy-sticker candy-left-1">🍭</div>
    <div class="candy-sticker candy-left-2">🍬</div>
    <div class="candy-sticker candy-left-3">🍭</div>
    <div class="candy-sticker candy-right-1">🍬</div>
    <div class="candy-sticker candy-right-2">🍭</div>
    <div class="candy-sticker candy-right-3">🍬</div>
""", unsafe_allow_html=True)

st.title("Kalkulator encrypt dan decrypt Kriptografi Klasik")
st.markdown("<p style='color: #558B2F; font-size: 1.1rem;'>Pilih salah satu algoritma klasik dan masukkan teks serta kunci untuk encrypt atau decrypt.</p>", unsafe_allow_html=True)

cipher = st.selectbox("Algoritma", ["Vigenere", "Affine", "Playfair", "Hill", "Enigma"])
mode = st.radio("Mode", ["Encrypt", "Decrypt"])

input_text = st.text_area("Teks input", height=150)

result = ""
error = None

if cipher == "Vigenere":
    key = st.text_input("Kunci (kata)")
    if st.button("Proses"):
        if key == "":
            error = "Masukkan kunci"
        else:
            try:
                if mode == "Encrypt":
                    result = vigenere_encrypt(input_text, key)
                else:
                    result = vigenere_decrypt(input_text, key)
            except Exception as e:
                error = str(e)

elif cipher == "Affine":
    a = st.number_input("a (coprime dengan 26)", value=5, step=1)
    b = st.number_input("b (angka)", value=8, step=1)
    if st.button("Proses"):
        try:
            if mode == "Encrypt":
                result = affine_encrypt(input_text, int(a), int(b))
            else:
                result = affine_decrypt(input_text, int(a), int(b))
        except Exception as e:
            error = str(e)

elif cipher == "Playfair":
    key = st.text_input("Kunci (kata)")
    if st.button("Proses"):
        if key == "":
            error = "Masukkan kunci"
        else:
            try:
                if mode == "Encrypt":
                    result = playfair_encrypt(input_text, key)
                else:
                    result = playfair_decrypt(input_text, key)
            except Exception as e:
                error = str(e)

elif cipher == "Hill":
    st.markdown("Masukkan matriks kunci 2x2, dipisahkan koma. Contoh: 3,3,2,5 untuk [[3,3],[2,5]]")
    key_raw = st.text_input("Matriks kunci 2x2")
    if st.button("Proses"):
        try:
            numbers = [int(x.strip()) for x in key_raw.split(",") if x.strip() != ""]
            if len(numbers) != 4:
                raise ValueError("Matriks kunci harus 4 angka")
            matrix = [[numbers[0], numbers[1]], [numbers[2], numbers[3]]]
            if mode == "Encrypt":
                result = hill_encrypt(input_text, matrix)
            else:
                result = hill_decrypt(input_text, matrix)
        except Exception as e:
            error = str(e)

elif cipher == "Enigma":
    st.markdown("Konfigurasi rotor dan posisi awal (huruf) serta ring setting (angka 1-26). Rotor diambil dari I, II, III.")
    rotor_choices = ["I", "II", "III"]
    rotor1 = st.selectbox("Rotor kanan", rotor_choices, index=0)
    rotor2 = st.selectbox("Rotor tengah", rotor_choices, index=1)
    rotor3 = st.selectbox("Rotor kiri", rotor_choices, index=2)
    pos1 = st.text_input("Posisi awal rotor kanan (A-Z)", value="A")
    pos2 = st.text_input("Posisi awal rotor tengah (A-Z)", value="A")
    pos3 = st.text_input("Posisi awal rotor kiri (A-Z)", value="A")
    ring1 = st.number_input("Ring setting kanan (1-26)", min_value=1, max_value=26, value=1)
    ring2 = st.number_input("Ring setting tengah (1-26)", min_value=1, max_value=26, value=1)
    ring3 = st.number_input("Ring setting kiri (1-26)", min_value=1, max_value=26, value=1)
    if st.button("Proses"):
        try:
            rotors = [rotor1, rotor2, rotor3]
            positions = [ord(pos1.upper()[0]) - 65, ord(pos2.upper()[0]) - 65, ord(pos3.upper()[0]) - 65]
            rings = [ring1 - 1, ring2 - 1, ring3 - 1]
            # for Enigma encrypt/decrypt are same
            result = enigma_encrypt_decrypt(input_text, rotors, positions, rings)
        except Exception as e:
            error = str(e)

if error:
    st.error(error)
elif result:
    st.success("Hasil:")
    st.code(result)

st.markdown("---")
st.markdown("*Aplikasi sederhana untuk tugas Kriptografi Klasik semester genap 2025/2026.*")
