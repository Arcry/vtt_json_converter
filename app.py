import streamlit as st
import json
import re
import os

def vtt_time_to_ms(time_str):
    """Преобразование времени в формате VTT (HH:MM:SS.sss) в миллисекунды."""
    hours, minutes, seconds = time_str.split(':')
    seconds, milliseconds = seconds.split('.')
    total_ms = (int(hours) * 3600 + int(minutes) * 60 + int(seconds)) * 1000 + int(milliseconds)
    return total_ms

def convert_vtt_to_json(vtt_content):
    """Конвертация VTT в JSON."""
    subtitles = []
    pattern = re.compile(r'(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})\n(.+?)\n\n', re.DOTALL)
    matches = pattern.findall(vtt_content)

    for start, end, text in matches:
        subtitles.append({
            "text": text.strip(),
            "start_time_ms": vtt_time_to_ms(start),
            "end_time_ms": vtt_time_to_ms(end),
            "gender": "male",
            "speaker_id": "0",
            "original_parts_info": None,
            "chapter_id": None
        })

    return {"subtitles": subtitles}

st.title("VTT to JSON Converter")

# Файл для загрузки
uploaded_file = st.file_uploader("Upload a VTT file", type="vtt")

if uploaded_file is not None:
    # Читаем содержимое VTT файла
    vtt_content = uploaded_file.read().decode("utf-8")
    
    # Конвертируем VTT в JSON
    json_result = convert_vtt_to_json(vtt_content)
    
    # Формируем имя выходного файла
    input_filename = uploaded_file.name
    output_filename = os.path.splitext(input_filename)[0] + ".json"
    
    # Отображаем результат пользователю
    st.write(f"File will be saved as: **{output_filename}**")
    
    # Кнопка для скачивания
    st.download_button(
        label="Download JSON",
        data=json.dumps(json_result, indent=4),
        file_name=output_filename,
        mime="application/json"
    )
