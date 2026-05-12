import datetime
import streamlit as st
from google import genai
from google.genai import types

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="AquaSense AI Chatbot",
    page_icon="🐟",
    layout="centered"
)

# ==========================================================
# CUSTOM CSS DARK THEME
# ==========================================================
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #e5e7eb;
}

.block-container {
    padding-top: 4rem;
    padding-bottom: 2rem;
    max-width: 900px;
}

.main-title {
    font-size: 2.5rem;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 0.4rem;
    line-height: 1.35;
}

.subtitle {
    font-size: 1.05rem;
    color: #93c5fd;
    margin-bottom: 1.5rem;
}

.info-card {
    padding: 1.2rem 1.4rem;
    border-radius: 18px;
    background-color: #111827;
    border-left: 6px solid #3b82f6;
    border: 1px solid #1f2937;
    margin-bottom: 1.2rem;
    color: #e5e7eb;
    line-height: 1.7;
}

.warning-card {
    padding: 1.2rem 1.4rem;
    border-radius: 18px;
    background-color: #1f1a12;
    border-left: 6px solid #f97316;
    border: 1px solid #3f2c16;
    margin-bottom: 1.2rem;
    color: #fef3c7;
    line-height: 1.7;
}

.success-card {
    padding: 1.2rem 1.4rem;
    border-radius: 18px;
    background-color: #052e2b;
    border-left: 6px solid #10b981;
    border: 1px solid #064e3b;
    margin-bottom: 1.2rem;
    color: #d1fae5;
    line-height: 1.7;
}

.example-box {
    padding: 1rem 1.2rem;
    border-radius: 14px;
    background-color: #172554;
    color: #bfdbfe;
    margin-bottom: 1rem;
    border: 1px solid #1d4ed8;
    line-height: 1.6;
}

.stButton > button {
    background-color: #1f2937;
    color: #ffffff;
    border: 1px solid #374151;
    border-radius: 10px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #2563eb;
    color: #ffffff;
    border: 1px solid #60a5fa;
}

.stChatMessage {
    background-color: #111827 !important;
    color: #e5e7eb !important;
    border-radius: 16px !important;
    border: 1px solid #1f2937 !important;
}

section[data-testid="stSidebar"] {
    background-color: #020617;
    color: #e5e7eb;
}

p, li, span, div {
    color: inherit;
}
</style>
""", unsafe_allow_html=True)

# ==========================================================
# HELPER FUNCTION
# ==========================================================
def build_transcript(messages):
    transcript = "# AquaSense AI Chat Transcript\n\n"
    transcript += f"Generated at: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for msg in messages:
        role = "User" if msg["role"] == "user" else "AquaSense AI"
        transcript += f"## {role}\n"
        transcript += f"{msg['content']}\n\n"

    return transcript

# ==========================================================
# HEADER
# ==========================================================
st.markdown(
    '<div class="main-title">🐟 AquaSense AI Chatbot</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">LLM-Based Assistant for Catfish Pond Water Quality Interpretation</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="info-card">
<b>AquaSense AI</b> adalah chatbot berbasis Gemini API yang membantu pengguna melakukan interpretasi awal 
terhadap kualitas air kolam lele. Pengguna dapat memasukkan data seperti suhu, pH, turbidity, dissolved oxygen, 
ammonia, atau gejala ikan untuk mendapatkan analisis dan rekomendasi awal.
</div>
""", unsafe_allow_html=True)

# ==========================================================
# SESSION STATE
# ==========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

if "api_key_checked" not in st.session_state:
    st.session_state.api_key_checked = False

if "api_key_valid" not in st.session_state:
    st.session_state.api_key_valid = False

# ==========================================================
# SIDEBAR CONFIGURATION
# ==========================================================
with st.sidebar:
    st.header("⚙️ Model Configuration")

    st.markdown("""
    Masukkan **Gemini API Key** Anda sendiri.  
    API Key tidak disimpan di aplikasi dan tidak ditampilkan ke pengguna lain.
    """)

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="Masukkan API key di sini..."
    )

    # ======================================================
    # TEST API KEY BUTTON
    # ======================================================
    if api_key:
        st.info("API Key sudah diisi. Klik tombol di bawah untuk mengecek koneksi.")

        if st.button("🔐 Test Gemini API Key"):
            try:
                test_client = genai.Client(api_key=api_key)

                test_response = test_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents="Reply only with OK."
                )

                if test_response.text:
                    st.session_state.api_key_checked = True
                    st.session_state.api_key_valid = True
                    st.success("✅ Gemini API Key valid dan berhasil terhubung.")
                else:
                    st.session_state.api_key_checked = True
                    st.session_state.api_key_valid = False
                    st.error("❌ API Key terbaca, tetapi Gemini tidak memberikan respons.")

            except Exception as e:
                st.session_state.api_key_checked = True
                st.session_state.api_key_valid = False
                st.error(f"❌ Gemini API Key tidak valid atau terjadi error: {e}")
    else:
        st.warning("Masukkan Gemini API Key terlebih dahulu.")

    st.divider()

    model_name = st.selectbox(
        "Model",
        ["gemini-2.5-flash", "gemini-2.0-flash"],
        index=0
    )

    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.3,
        step=0.1,
        help="Nilai rendah membuat jawaban lebih stabil. Nilai tinggi membuat jawaban lebih kreatif."
    )

    max_tokens = st.slider(
        "Max Output Tokens",
        min_value=300,
        max_value=2000,
        value=1000,
        step=100,
        help="Mengatur panjang maksimum jawaban chatbot."
    )

    tone = st.selectbox(
        "Gaya Bahasa",
        ["Edukatif", "Formal", "Santai"],
        index=0
    )

    st.divider()

    st.subheader("💡 Example Prompts")

    example_1 = "Suhu kolam saya 31°C, pH 6.2, dan air terlihat sangat keruh. Ikan lele sering naik ke permukaan. Apa yang harus saya lakukan?"
    example_2 = "Data sensor saya: temperature 29°C, pH 7.1, turbidity sedang. Apakah kualitas air kolam masih aman untuk budidaya lele?"
    example_3 = "Apa saja parameter kualitas air yang penting dipantau dalam budidaya lele berbasis IoT?"
    example_4 = "pH kolam saya 5.8 dan ikan terlihat lemas. Apa risiko awalnya dan tindakan apa yang perlu dilakukan?"

    if st.button("Gunakan Contoh 1"):
        st.session_state.pending_prompt = example_1

    if st.button("Gunakan Contoh 2"):
        st.session_state.pending_prompt = example_2

    if st.button("Gunakan Contoh 3"):
        st.session_state.pending_prompt = example_3

    if st.button("Gunakan Contoh 4"):
        st.session_state.pending_prompt = example_4

    st.divider()

    if st.button("🧹 Reset Chat"):
        st.session_state.messages = []
        st.session_state.pending_prompt = ""
        st.session_state.api_key_checked = False
        st.session_state.api_key_valid = False
        st.rerun()

# ==========================================================
# SYSTEM INSTRUCTION
# ==========================================================
system_instruction = f"""
You are AquaSense AI, an educational assistant for catfish pond water quality monitoring.

Your role is to help users interpret early water quality conditions based on parameters such as:
- temperature
- pH
- turbidity
- dissolved oxygen
- ammonia
- pond symptoms
- fish behavior

Always answer in Indonesian unless the user asks otherwise.

Use a {tone.lower()} tone.

Your response must be structured into these sections:
1. Ringkasan Kondisi
2. Analisis Parameter
3. Tingkat Risiko Awal
4. Rekomendasi Tindakan
5. Catatan Kehati-hatian

Important rules:
- Do not claim to replace aquaculture experts.
- Do not make unsupported medical or veterinary claims.
- Do not invent exact sensor values if the user does not provide them.
- If the user provides incomplete data, ask relevant follow-up questions.
- If the condition sounds risky or dangerous, advise the user to validate with direct measurement and consult an expert.
- Use clear, practical, and easy-to-understand language.
- Focus on decision-support and education, not final diagnosis.
"""

# ==========================================================
# PROJECT DESCRIPTION
# ==========================================================
with st.expander("📌 Tentang Project Ini"):
    st.markdown("""
    **AquaSense AI Chatbot** dibuat untuk final project pelatihan 
    **LLM-Based Tools and Gemini API Integration for Data Scientists**.

    **Use Case:** Education bot dan decision-support assistant untuk monitoring kualitas air kolam lele.

    **Input:** Pertanyaan pengguna atau data parameter air seperti temperature, pH, turbidity, dissolved oxygen, ammonia, dan gejala ikan.

    **Output:** Ringkasan kondisi, analisis parameter, tingkat risiko awal, rekomendasi tindakan, dan catatan kehati-hatian.

    **Parameter Kreatif:** Chatbot menyediakan pengaturan model, temperature, max output tokens, dan gaya bahasa.
    """)

# ==========================================================
# DISCLAIMER
# ==========================================================
st.markdown("""
<div class="warning-card">
⚠️ <b>Disclaimer:</b> Jawaban AquaSense AI bersifat bantuan awal dan edukatif. 
Keputusan akhir tetap perlu divalidasi dengan pengukuran langsung, pengalaman lapangan, dan konsultasi dengan ahli budidaya.
</div>
""", unsafe_allow_html=True)

# ==========================================================
# DISPLAY CHAT HISTORY
# ==========================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ==========================================================
# PROMPT HANDLER
# ==========================================================
prompt_to_process = None

if st.session_state.pending_prompt:
    st.markdown("""
    <div class="success-card">
    Contoh prompt sudah dipilih. Klik tombol di bawah untuk mengirim prompt tersebut ke chatbot.
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="example-box">{st.session_state.pending_prompt}</div>',
        unsafe_allow_html=True
    )

    if st.button("🚀 Kirim Contoh Prompt"):
        prompt_to_process = st.session_state.pending_prompt
        st.session_state.pending_prompt = ""

user_prompt = st.chat_input("Tanyakan kondisi kualitas air kolam lele...")

if user_prompt:
    prompt_to_process = user_prompt

# ==========================================================
# GENERATE RESPONSE
# ==========================================================
if prompt_to_process:
    if not api_key:
        st.error("Masukkan Gemini API Key terlebih dahulu di sidebar.")
        st.stop()

    st.session_state.messages.append({
        "role": "user",
        "content": prompt_to_process
    })

    with st.chat_message("user"):
        st.markdown(prompt_to_process)

    with st.chat_message("assistant"):
        with st.spinner("AquaSense AI sedang menganalisis..."):
            try:
                client = genai.Client(api_key=api_key)

                conversation_context = ""
                for msg in st.session_state.messages[-8:]:
                    role = "User" if msg["role"] == "user" else "Assistant"
                    conversation_context += f"{role}: {msg['content']}\\n"

                response = client.models.generate_content(
                    model=model_name,
                    contents=conversation_context,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=temperature,
                        max_output_tokens=max_tokens
                    )
                )

                answer = response.text if response.text else "Maaf, saya belum dapat menghasilkan jawaban."

            except Exception as e:
                answer = f"Terjadi error saat memanggil Gemini API: {e}"

        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })

# ==========================================================
# DOWNLOAD TRANSCRIPT
# ==========================================================
if st.session_state.messages:
    transcript = build_transcript(st.session_state.messages)

    st.download_button(
        label="⬇️ Download Chat Transcript",
        data=transcript,
        file_name="aquasense_chat_transcript.md",
        mime="text/markdown"
    )
