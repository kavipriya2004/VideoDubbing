from flask import Flask, render_template, request, jsonify
import os
import moviepy.editor as mp
import speech_recognition as sr
from googletrans import Translator

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
    with open(extracted_text_file, 'w') as f:
        f.write(extracted_text)
    
    # Translate extracted text to target language
    translated_text = translate_text(extracted_text, target_language)
    translated_text_file = os.path.splitext(video_path)[0] + "_translated_text.txt"
    with open(translated_text_file, 'w') as f:
        f.write(translated_text)
    
    # Generate audio from translated text
    translated_audio_clip = text_to_audio(translated_text, audio_path)
    translated_audio_file = os.path.splitext(video_path)[0] + "_translated_audio.wav"
    if translated_audio_clip:
        translated_audio_clip.write_audiofile(translated_audio_file)
    else:
        translated_audio_file = None

    # Merge audio with original video
    output_video_path = merge_audio_with_video(video_path, translated_audio_clip)
    
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

def text_to_audio(text, audio_path):
    translator = Translator()
    translated_audio = translator.translate(text, dest='en').pronunciation
    if translated_audio:
        translated_audio_clip = mp.AudioFileClip(translated_audio)
        original_audio_clip = mp.AudioFileClip(audio_path)
        merged_audio = mp.CompositeAudioClip([original_audio_clip, translated_audio_clip])
        return merged_audio
    else:
        return None


def merge_audio_with_video(video_path, audio_clip):
    video_clip = mp.VideoFileClip(video_path)
    video_clip.audio = audio_clip
    output_path = os.path.splitext(video_path)[0] + "_translated.mp4"
    video_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")
    return output_path

if __name__ == "_main_":
    app.run(debug=True)