import asyncio
import io
import os
import tempfile
from pathlib import Path

import edge_tts
import PyPDF2
import streamlit as st


DEFAULT_VOICE = 'en-US-AriaNeural'
DEFAULT_RATE = '-30%'


def parse_feature_request(feature_request: str):
    request = (feature_request or "").lower()

    if "female" in request:
        voice = "en-US-AriaNeural"
    elif "male" in request:
        voice = "en-US-GuyNeural"
    else:
        voice = DEFAULT_VOICE

    if "slow" in request:
        rate = "-30%"
    elif "fast" in request:
        rate = "+30%"
    else:
        rate = DEFAULT_RATE

    return voice, rate


async def _create_audio_file(text: str, voice: str, rate: str) -> bytes:
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
    )

    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as temp:
            temp_path = temp.name

        await communicate.save(temp_path)
        return Path(temp_path).read_bytes()
    finally:
        if temp_path:
            try:
                os.unlink(temp_path)
            except OSError:
                pass


def generate_audiobook(pdf_bytes: bytes, feature_request: str) -> bytes:
    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    text_parts = []

    for page in reader.pages:
        try:
            extracted = page.extract_text()
            if extracted:
                text_parts.append(extracted)
        except Exception:
            continue

    text = "\n".join(text_parts)

    if not text.strip():
        raise ValueError(
            "No readable text was found in this PDF. "
            "Please upload a text-based PDF."
        )

    voice, rate = parse_feature_request(feature_request)
    return asyncio.run(_create_audio_file(text, voice, rate))


if __name__ == "__main__":
    st.set_page_config(page_title="PDF to Audiobook")
    st.title("PDF to Audiobook")

    uploaded_pdf = st.file_uploader(
        "Upload a PDF",
        type=["pdf"],
    )

    feature_request = st.text_input(
        "Feature request",
        placeholder="Example: female voice slow",
    )

    if uploaded_pdf is not None:
        if st.button("Generate Audiobook"):
            try:
                audio_bytes = generate_audiobook(
                    uploaded_pdf.getvalue(),
                    feature_request,
                )
                st.audio(audio_bytes, format="audio/mp3")
                st.download_button(
                    "Download Audiobook",
                    data=audio_bytes,
                    file_name="audiobook.mp3",
                    mime="audio/mpeg",
                )
            except Exception as exc:
                st.error(str(exc))