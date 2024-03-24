from flask import Flask, render_template, request, jsonify
import os
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS

app = Flask(__name__)
output_folder = 'output_videos'

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_video', methods=['POST'])
def translate_video():
    target_language = request.form['targetLanguage']
    video_file = request.files['videoFile']
    
    video_filename = os.path.join(output_folder, video_file.filename)
    video_file.save(video_filename)

    extracted_text_file, translated_text_file, translated_audio_file, output_video = translate_and_merge(video_filename, target_language)

    return jsonify({'extracted_text_file': extracted_text_file, 'translated_text_file': translated_text_file, 'translated_audio_file': translated_audio_file, 'output_video': output_video, 'original_video': video_filename})

def translate_and_merge(video_path, target_language='es'):
    # Extract audio from video
    audio_path = extract_audio(video_path)
    
    # Transcribe audio to text
    extracted_text = transcribe_audio(audio_path)
    extracted_text_file = os.path.splitext(video_path)[0] + "_extracted_text.txt"
    with open(extracted_text_file, 'w', encoding='utf-8') as f:
        f.write(extracted_text)
    
    # Translate extracted text to target language
    translated_text = translate_text(extracted_text, target_language)
    translated_text_file = os.path.splitext(video_path)[0] + "_translated_text.txt"
    with open(translated_text_file, 'w', encoding='utf-8') as f:
        f.write(translated_text)
    
    # Translate extracted audio to target language
    translated_audio_file = translate_audio(audio_path, target_language)
    
    # Merge audio with original video
    output_video_path = merge_audio_with_video(video_path, translated_audio_file)
    
    return extracted_text_file, translated_text_file, translated_audio_file, output_video_path

def extract_audio(video_path):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = video_clip.audio
    audio_path = os.path.splitext(video_path)[0] + ".wav"
    audio_clip.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
        except sr.UnknownValueError:
            text = "Speech recognition could not understand the audio"
    return text

def translate_text(text, target_language='en'):
    translator = Translator()
    translated_text = translator.translate(text, dest=target_language).text
    return translated_text

def translate_audio(audio_path, target_language='en'):
    # Load the audio file
    audio_clip = mp.AudioFileClip(audio_path)
    
    # Convert audio to text
    extracted_text = transcribe_audio(audio_path)
    
    # Translate the text
    translated_text = translate_text(extracted_text, target_language)
    
    # Generate translated audio
    tts = gTTS(text=translated_text, lang=target_language)
    translated_audio_file = os.path.splitext(audio_path)[0] + "_translated.mp3"
    tts.save(translated_audio_file)
    
    return translated_audio_file

def merge_audio_with_video(video_path, translated_audio_file):
    video_clip = mp.VideoFileClip(video_path)
    audio_clip = mp.AudioFileClip(translated_audio_file)
    video_clip = video_clip.set_audio(audio_clip)
    output_path = os.path.splitext(video_path)[0] + "_translated.mp4"
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

if __name__ == "_main_":
    app.run(debug=True)