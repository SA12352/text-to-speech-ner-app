# ner_app.py
# 🔹 Named Entity Recognition (NER) + Text-to-Speech
# Thank you Nexus company for giving this opportunity. Task 2 completed.

import spacy
from spacy import displacy
import pandas as pd
import streamlit as st
from gtts import gTTS
import os
import subprocess

# -----------------------------
# Load SpaCy model (small, deploy-friendly)
# -----------------------------
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")

# -----------------------------
# Custom Entity Ruler for products (iPhone 15, etc.)
# -----------------------------
from spacy.pipeline import EntityRuler

ruler = nlp.add_pipe("entity_ruler", before="ner")
patterns = [
    {"label": "PRODUCT", "pattern": "iPhone 15"},
    {"label": "PRODUCT", "pattern": "iPhone 14"},
    {"label": "PRODUCT", "pattern": "MacBook Pro"},
    {"label": "PRODUCT", "pattern": "Samsung Galaxy S23"},
]
ruler.add_patterns(patterns)

# -----------------------------
# Function to extract entities
# -----------------------------
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents], doc

# -----------------------------
# Function for text-to-speech
# -----------------------------
def speak_text(text, filename="output.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

# -----------------------------
# Streamlit App
# -----------------------------
def main():
    st.set_page_config(page_title="NER + TTS App", layout="wide")
    st.title("🔎 Named Entity Recognition (NER) + Text-to-Speech")
    st.write("Extract key entities from customer queries and hear them spoken out.")

    # Input box
    query = st.text_area("Enter a customer query:", "Do you have the iPhone 15 in stock?")

    # Button to extract entities
    if st.button("Extract Entities"):
        if query.strip():
            entities, doc = extract_entities(query)

            if entities:
                st.subheader("📌 Extracted Entities")
                df = pd.DataFrame(entities, columns=["Entity", "Label"])
                st.table(df)

                # Visualization with displacy
                html = displacy.render(doc, style="ent")
                st.markdown(html, unsafe_allow_html=True)

                # Prepare text for speech
                entity_texts = [f"{ent} ({label})" for ent, label in entities]
                speech_text = "I found the following entities: " + ", ".join(entity_texts)

                # Generate speech
                audio_file = speak_text(speech_text)
                st.audio(audio_file, format="audio/mp3")

            else:
                st.warning("⚠️ No entities found.")
                audio_file = speak_text("No entities found in your query.")
                st.audio(audio_file, format="audio/mp3")
        else:
            st.error("Please enter a query first.")

if __name__ == "__main__":
    main()










































