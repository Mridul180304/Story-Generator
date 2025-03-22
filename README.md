# Story Generator

## Overview
This is a Flask-based web application that generates short stories based on user input using Google's Gemini AI model. It allows users to specify age, gender, mood, interests, and other parameters to create customized stories. The application also includes a text-to-speech feature to convert stories into audio in multiple languages.

## Features
- Generate short stories based on user input
- Store generated stories in a database
- Convert stories into speech using Google Text-to-Speech (gTTS)
- Translate stories into different languages (Hindi, Marathi, etc.)

## Technologies Used
- **Flask** (Backend Framework)
- **Google Generative AI (Gemini API)** (Story Generation)
- **Flask-SQLAlchemy** (Database ORM)
- **Google Text-to-Speech (gTTS)** (Audio Generation)
- **Deep Translator** (Language Translation)
- **Dotenv** (Environment Variable Management)

## Installation

### Prerequisites
Make sure you have the following installed:
- Python (>=3.7)
- pip (Python package manager)
- Git (optional)

### Steps
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/Story-Generator.git
   cd Story-Generator
   ```

2. **Create a virtual environment (Optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/macOS
   venv\Scripts\activate    # For Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Create a `.env` file in the project root and add the following:
     ```ini
     API_KEY=your_google_gemini_api_key
     DB_URI=sqlite:///stories.db  # Use SQLite for local development
     ```

5. **Initialize the database**
   ```bash
   python -c "from app import db; db.create_all()"
   ```

6. **Run the application**
   ```bash
   python app.py
   ```
   The application will be available at `http://127.0.0.1:5000/`.

## API Endpoints

### 1. Generate a Story
**Endpoint:** `/generate_story`  
**Method:** `POST`
**Payload:**
```json
{
  "age": 6,
  "gender": "boy",
  "mood": "happy",
  "interests": "adventure",
  "story_length": "short",
  "time_of_day": "bedtime",
  "additional": "Include a magical pet."
}
```
**Response:**
```json
{
  "story": "Once upon a time..."
}
```

### 2. Convert Story to Speech
**Endpoint:** `/speak_story`  
**Method:** `POST`
**Payload:**
```json
{
  "story": "Once upon a time...",
  "language": "hi"
}
```
**Response:** Returns an audio file.

## Folder Structure
```
Story-Generator/
│── templates/
│   ├── form.html
│── app.py  # Main Flask application
│── gemini.py  # Story generation using Gemini API
│── requirements.txt  # Dependencies
│── .env  # Environment variables (not included in repo)
│── README.md  # Project documentation
```

## Contact
For questions or suggestions, feel free to reach out at mridulchawla20@example.com.

## License
This project is licensed under the MIT License.

