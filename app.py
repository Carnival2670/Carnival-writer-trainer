import streamlit as st
from openai import OpenAI
import os

# Pastikan kamu sudah mengatur variabel lingkungan OPENAI_API_KEY di Streamlit Cloud
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Struktur urutan latihan
sequence_steps = {
    "1. Premis": [
        "Tuliskan 1 kalimat ringkas tentang tokoh utama dan konflik utama.",
        "Buat pembaca tahu kenapa cerita ini penting atau layak diikuti."
    ],
    "2. Karakterisasi": [
        "Kenalkan sifat dan motivasi tokoh utama.",
        "Berikan satu tindakan/tanggapan yang menunjukkan karakternya."
    ],
    "3. Setting Awal": [
        "Deskripsikan tempat dan waktu cerita secara singkat.",
        "Tunjukkan suasana yang relevan dengan konflik atau tema."
    ],
    "4. Pemicu Konflik": [
        "Tuliskan kejadian yang menjadi titik tolak perubahan.",
        "Konflik bisa dari dalam diri, orang lain, atau lingkungan."
    ],
    "5. Reaksi Tokoh": [
        "Tunjukkan bagaimana tokoh utama bereaksi pertama kali.",
        "Reaksinya harus sesuai dengan karakterisasi sebelumnya."
    ],
    "6. Komplikasi": [
        "Masukkan rintangan atau konsekuensi dari reaksi awal.",
        "Pertahankan logika dan konsistensi dengan konflik utama."
    ],
    "7. Klimaks": [
        "Tunjukkan titik balik cerita: puncak emosi atau keputusan penting.",
        "Pastikan pembaca merasa tegang atau penasaran."
    ],
    "8. Resolusi": [
        "Berikan penutup yang memuaskan atau menggugah pikiran.",
        "Tunjukkan perubahan tokoh atau konsekuensi akhir konflik."
    ]
}

st.set_page_config(page_title="AI Modular Writer Trainer", layout="wide")
st.title("🧠 AI Modular Writer Trainer")

selected_step = st.selectbox("📍 Pilih urutan latihan menulis:", list(sequence_steps.keys()))
guidelines = sequence_steps[selected_step]

st.markdown("### ✍️ Step Guidelines:")
for item in guidelines:
    st.markdown(f"- {item}")

story_input = st.text_area("⚡ Start writing here...", height=250)

if st.button("🧠 Get AI Feedback"):
    if not story_input.strip():
        st.warning("Please write something before submitting.")
    else:
        prompt = f"""Evaluate this writing for the step: {selected_step}.\n
Guidelines: {guidelines}\n
User writing:\n{story_input}\n
Give constructive feedback and point out if the writing deviates from the expected structure."""

        with st.spinner("Analyzing with AI..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert writing coach for screenwriters."},
                        {"role": "user", "content": prompt}
                    ]
                )
                feedback = response.choices[0].message.content
                st.success("✅ AI Feedback:")
                st.write(feedback)

            except Exception as e:
                st.error(f"⚠️ Error: {e}")

