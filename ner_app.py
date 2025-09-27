import spacy
import pandas as pd
import streamlit as st
from spacy import displacy
from gtts import gTTS   # ✅ correct import
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import os

# -----------------------------
# Page Config (must be first)
# -----------------------------
st.set_page_config(page_title="Universal NER App", layout="wide")

# -----------------------------
# Initialize session state
# -----------------------------
if "query" not in st.session_state:
    st.session_state["query"] = ""
if "entities" not in st.session_state:
    st.session_state["entities"] = []

# -----------------------------
# Load SpaCy model
# -----------------------------
try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    from spacy.cli import download
    download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

# -----------------------------
# Functions
# -----------------------------
def extract_entities(text):
    doc = nlp(text)
    return [(ent.text, ent.label_) for ent in doc.ents], doc

def speak_text(text, filename="output.mp3"):
    tts = gTTS(text=text, lang="en")
    tts.save(filename)
    return filename

def save_pdf(entities, query, filename="entities.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    flowables = []

    flowables.append(Paragraph("Named Entity Recognition Report", styles["Heading1"]))
    flowables.append(Spacer(1, 12))
    flowables.append(Paragraph(f"Input Query: {query}", styles["Normal"]))
    flowables.append(Spacer(1, 12))

    if entities:
        data = [["Entity", "Label"]] + entities
        table = Table(data)
        flowables.append(table)
    else:
        flowables.append(Paragraph("No entities found.", styles["Normal"]))

    doc.build(flowables)
    return filename

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🔎 Universal Named Entity Recognition (NER) with Text-to-Speech")

query = st.text_area("✍️ Enter your text:", st.session_state["query"])

if st.button("Extract Entities"):
    if query.strip():
        entities, doc = extract_entities(query)
        st.session_state["query"] = query
        st.session_state["entities"] = entities

        if entities:
            st.subheader("📌 Extracted Entities")
            df = pd.DataFrame(entities, columns=["Entity", "Label"])
            st.table(df)

            html = displacy.render(doc, style="ent")
            st.markdown(html, unsafe_allow_html=True)

            # TTS
            entity_texts = [f"{ent} ({label})" for ent, label in entities]
            speech_text = "I found the following entities: " + ", ".join(entity_texts)
            audio_file = speak_text(speech_text)
            st.audio(audio_file, format="audio/mp3")

            # PDF
            pdf_file = save_pdf(entities, query)
            with open(pdf_file, "rb") as f:
                st.download_button("📥 Download Report as PDF", f, file_name="entities.pdf")
        else:
            st.warning("⚠️ No entities found.")
    else:
        st.error("Please enter some text.")

# -----------------------------
# Buttons to clear query/results/all
# -----------------------------

    if st.button("🗑️ Remove All"):
        st.session_state["query"] = ""
        st.session_state["entities"] = []
        st.reru












