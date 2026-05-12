# AquaSense AI Chatbot

AquaSense AI Chatbot adalah chatbot berbasis Large Language Model (LLM) yang membantu pengguna melakukan interpretasi awal terhadap kondisi kualitas air kolam lele berdasarkan parameter seperti temperature, pH, turbidity, dissolved oxygen, ammonia, dan gejala ikan.

Project ini dibuat untuk final project pelatihan **LLM-Based Tools and Gemini API Integration for Data Scientists**.

## Use Case

Use case dari project ini adalah education bot dan decision-support assistant untuk monitoring kualitas air kolam lele.

Chatbot ini membantu pengguna memahami kondisi awal kualitas air secara lebih cepat dan terstruktur. Namun, hasil analisis tetap perlu divalidasi dengan pengukuran langsung dan konsultasi dengan ahli budidaya.

## Main Features

- Chatbot berbasis Gemini API
- User interface menggunakan Streamlit
- Input Gemini API Key langsung dari halaman web
- Tombol validasi Gemini API Key
- Konfigurasi model
- Pengaturan temperature
- Pengaturan max output tokens
- Pilihan gaya bahasa: Edukatif, Formal, dan Santai
- Example prompts
- Riwayat percakapan menggunakan session state
- Download chat transcript
- Disclaimer human-in-the-loop

## Input

User dapat memasukkan informasi seperti:

- Temperature
- pH
- Turbidity
- Dissolved Oxygen
- Ammonia
- Gejala ikan
- Pertanyaan umum tentang kualitas air kolam

## Output

Chatbot menghasilkan jawaban dengan struktur:

1. Ringkasan Kondisi
2. Analisis Parameter
3. Tingkat Risiko Awal
4. Rekomendasi Tindakan
5. Catatan Kehati-hatian

## Model Configuration

Contoh konfigurasi yang digunakan:

- Model: Gemini 2.5 Flash
- Temperature: 0.3
- Max Output Tokens: 1000
- Interface: Streamlit
- Deployment Testing: ngrok via Google Colab

## How to Run Locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run Streamlit:

```bash
streamlit run AquaSense_AI_Chatbot.py
```

After the app opens, enter your own Gemini API Key in the sidebar.

## How to Run in Google Colab

1. Install required libraries.
2. Run the Streamlit app file.
3. Use ngrok to generate a public URL.
4. Open the URL in browser.
5. Enter your Gemini API Key in the sidebar.
6. Test the API key.
7. Start chatting with AquaSense AI.

## Screenshots

Screenshots of the application are available in the `screenshots/` folder.

## Security Note

Do not upload Gemini API Key or ngrok token to GitHub.  
Gemini API Key is entered directly by the user through the Streamlit sidebar.  
Ngrok token is only used in Google Colab through Colab Secrets.

## Disclaimer

AquaSense AI hanya digunakan sebagai bantuan awal dan edukatif. Keputusan akhir tetap perlu divalidasi dengan pengukuran langsung, pengalaman lapangan, dan konsultasi dengan ahli budidaya.
```
