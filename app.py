import streamlit as st
from datetime import date
from gtts import gTTS, lang
from googletrans import Translator

st.set_page_config(page_title="Simply! Translate", page_icon="🎯")

def get_key(val):
    for key, value in lang.tts_langs().items():
        if val == value:
            return key

def main():
    trans = Translator()
    langs = lang.tts_langs()

    st.header("Translate your thoughts.")
    st.write(f"Date: {date.today()}")

    input_text = st.text_input("Enter text to translate")
    lang_choice = st.selectbox("Translate to:", list(langs.values()))

    if st.button("Translate"):
        if not input_text.strip():  # Check if input text is empty or contains only whitespace
            st.warning("Please enter text to translate.")
        else:
            try:
                detect = trans.detect(input_text)
                detect_expander = st.expander("Detected Language")
                with detect_expander:
                    st.success(f"Detected Language: {langs[detect.lang]}")

                    detect_audio = gTTS(text=input_text, lang=detect.lang, slow=False)
                    detect_audio.save("user_detect.mp3")
                    audio_file = open("user_detect.mp3", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/ogg", start_time=0)

                translation = trans.translate(input_text, dest=get_key(lang_choice))
                trans_expander = st.expander("Translated Text")
                with trans_expander:
                    st.success(f"Translated Text: {translation.text}")

                    translated_audio = gTTS(
                        text=translation.text, lang=get_key(lang_choice), slow=False
                    )
                    translated_audio.save("user_trans.mp3")
                    audio_file = open("user_trans.mp3", "rb")
                    audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/ogg", start_time=0)

                    with open("user_trans.mp3", "rb") as file:
                        st.download_button(
                            label="Download",
                            data=file,
                            file_name="trans.mp3",
                            mime="audio/ogg",
                        )

            except AttributeError:
                st.error("Error: Unable to detect language.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
