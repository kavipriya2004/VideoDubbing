# Video Translation Application

A web application for translating video content. This app extracts audio from a video, transcribes the audio to text, translates the text to a target language, and merges the translated audio back with the original video.

## Features

- **Video Upload:** Upload videos for translation.
- **Language Selection:** Choose a target language for translation.
- **Audio Extraction:** Extract audio from the video file.
- **Speech-to-Text:** Convert extracted audio to text.
- **Text Translation:** Translate the extracted text to the target language.
- **Text-to-Speech:** Convert the translated text back to audio.
- **Video Merging:** Merge the translated audio with the original video.

## Technologies Used

- **Flask:** Web framework for the server-side application.
- **MoviePy:** Video editing library for audio extraction and video merging.
- **SpeechRecognition:** Library for converting speech to text.
- **Google Translator:** For translating text to the target language.
- **Google Text-to-Speech (gTTS):** For converting translated text to speech.

## Installation

To get started with this project, follow these steps:

### Clone the Repository

```bash
git clone https://github.com/yourusername/videodubbing.git
cd videodubbing
```

### Install Dependencies

Create a virtual environment (recommended) and install the required libraries.

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install Flask moviepy SpeechRecognition googletrans==4.0.0-rc1 gtts
```

### Ensure Proper Files

Make sure you have an `index.html` file in a folder named `templates` in your project directory.

## Usage

### Running the Flask Application

To start the Flask application, run the following command:

```bash
python app.py
```

This will start the server on `http://127.0.0.1:5000/`. Open this URL in your web browser to access the application.

### Using the Application

1. **Upload a Video:** Click the "Choose File" button to upload a video.
2. **Select Target Language:** Choose the language to which you want to translate the video.
3. **Submit the Form:** Click the "Translate Video" button to process the video.
4. **Processing:** Wait for the video to be processed. A link to the translated video will be displayed once the process is complete.

## Code Structure

- `app.py`: Contains the Flask application and the video translation logic.
- `templates/index.html`: The HTML template for the web interface.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
