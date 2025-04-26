from flask import Flask, request, jsonify, render_template
import pandas as pd
from mood_detection import detect_mood
from recommendation import hybrid_recommendation

app = Flask(__name__)

# Load data once when the server starts
meal_data = pd.read_excel("databases/Meal Data.xlsx")
user_data = pd.read_excel("databases/User Data.xlsx")

# Home route (to avoid "Not Found" error)
@app.route('/')
def home():
    return "Welcome to the AI Meal Recommendation System!"

# Recommendation API route
@app.route("/recommend", methods=["POST"])
def recommend():
    try:
        # Get user input from request
        user_input = request.get_json()
        user_id = user_input.get("user_id")
        mood_text = user_input.get("mood")
        preferences = user_input.get("preferences")

        # Mood detection and recommendation
        mood = detect_mood(mood_text)
        recommendations = hybrid_recommendation(user_id, preferences, user_data, meal_data)
        
        # Return recommendations
        return jsonify({
            "status": "success",
            "mood_detected": mood,
            "recommendations": recommendations
        })

    except Exception as e:
        # Return error if something goes wrong
        return jsonify({
            "status": "error",
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)

