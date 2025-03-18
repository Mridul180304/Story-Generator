import os
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template, Response
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from gtts import gTTS
from deep_translator import GoogleTranslator
import io


load_dotenv()


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DB_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


genai.configure(api_key=os.getenv("API_KEY"), transport="rest")


model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",
    generation_config={
        "temperature": 0.3,
        "top_p": 0.7,
        "top_k": 30,
        "max_output_tokens": 700,
        "response_mime_type": "text/plain",
    }
)


class Story(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    mood = db.Column(db.String(50), nullable=True)
    interests = db.Column(db.String(100), nullable=True)
    story_length = db.Column(db.String(50), nullable=True)
    time_of_day = db.Column(db.String(50), nullable=True)
    additional_data = db.Column(db.String(150), nullable=True)  


with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return render_template('form.html')


@app.route('/generate_story', methods=['POST'])
def generate_story():
    try:
        data = request.json
        additional_requests = data.get('additional', '') 

        prompt = f"""
        Write a simple, easy-to-read short story for a {data.get('age', '6')}-year-old {data.get('gender', 'boy')}.
        - Mood: {data.get('mood', 'happy')}
        - Interests: {data.get('interests', 'adventure')}
        - Story Length: {data.get('story_length', 'short')}
        - Time of Day: {data.get('time_of_day', 'bedtime')}
        - Additional Requests: {additional_requests}
        The story should have:
        - A clear beginning, middle, and proper ending.
        - Simple words and short sentences.
        - No complex or abstract ideas.
        - A moral lesson or positive conclusion.

        
        """

        response = model.generate_content(prompt)
        story = response.text if response else "Sorry, I couldn't generate a story right now."

        
        new_story = Story(
            age=data.get('age', 6),
            gender=data.get('gender', 'boy'),
            mood=data.get('mood', 'happy'),
            interests=data.get('interests', 'adventure'),
            story_length=data.get('story_length', 'short'),
            time_of_day=data.get('time_of_day', 'bedtime'),
            additional_data=additional_requests  
        )
        db.session.add(new_story)
        db.session.commit()

        return jsonify({'story': story})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/speak_story', methods=['POST'])
def speak_story():
    try:
        data = request.json
        story = data.get('story', '')
        language = data.get('language', 'en')

        if language == "hi":
            story = GoogleTranslator(source='en', target='hi').translate(story)
        elif language == "mr": 
            story = GoogleTranslator(source='en', target='mr').translate(story)

        tts = gTTS(story, lang=language)
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        return Response(audio_bytes, mimetype="audio/mpeg")
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)