import streamlit as st
import openai
import os

st.set_page_config(page_title="AI Modular Writer Trainer", layout="wide")
st.title("🧠 AI Writing Feedback: 8 Sequence Trainer")

# API Key from Secret
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step options
sequence_steps = {
    "Sequence 1 - Setup": [
        "Introduce the main character",
        "Show the normal world",
        "Present a small imbalance"
    ],
    "Sequence 2 - Inciting Event": [
        "Trigger change", "Escalate situation", "Push protagonist into decision"
    ],
    # Tambahkan Sequence 3 - 8 kalau perlu
}

selected_step = st.selectbox("Choose your Sequence Step:", list(sequence_steps.keys()))
guidelines = sequence_steps[selected_step]
st.markdown("### Step Guidelines:")
for item in guidelines:
    st.markdown(f"- {item}")

story_input = st.text_area("✍️ Start writing here...", height=250)

if st.button("🚀 Get AI Feedback"):
    if not story_input.strip():
        st.warning("Please write something before submitting.")
    else:
        prompt = f"Evaluate this writing for the step: {selected_step}.\n" \
                 f"Guidelines: {guidelines}\n\n" \
                 f"User writing:\n{story_input}\n\n" \
                 f"Give constructive feedback and point out if the writing deviates from the expected structure."

        with st.spinner("Analyzing with AI..."):
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are an expert writing coach for screenwriters."},
                        {"role": "user", "content": prompt}
                    ]
                )
                feedback = response['choices'][0]['message']['content']
                st.success("✅ AI Feedback:")
                st.write(feedback)
            except Exception as e:
                st.error(f"⚠️ Error: {e}")
