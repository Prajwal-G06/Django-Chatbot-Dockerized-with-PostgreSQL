from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from dotenv import load_dotenv
from openai import OpenAI
from .models import ConversationHistory

# Load environment variables
load_dotenv()

# Load trained intent classifier
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'intent_classifier.pkl')
intent_classifier = joblib.load(model_path)

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# OMDb API
omdb_api_key = os.getenv('OMDB_API_KEY')
movie_metadata_cache = {}

def get_movie_info(movie_name):
    base_url = "http://www.omdbapi.com/"
    params = {"t": movie_name, "apikey": omdb_api_key}
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if data.get("Response") == "False":
            return f"Sorry, I couldn't find any information about '{movie_name}'."
        return (
            f"Title: {data['Title']}\n"
            f"Year: {data['Year']}\n"
            f"Genre: {data['Genre']}\n"
            f"Actors: {data['Actors']}\n"
            f"Plot: {data['Plot']}"
        )
    except Exception as e:
        return f"Error fetching movie info: {e}"

def get_recommendations(movie_name):
    return "Recommendations are not available in this simplified version."

@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        user_input = request.POST.get('user_input', '').strip()

        # classify intent
        probs = intent_classifier.predict_proba([user_input])[0]
        max_prob = max(probs)
        intent = intent_classifier.classes_[probs.argmax()]
        if max_prob < 0.6:
            intent = "general_chat"

        # generate response
        if intent == "movie_info":
            movie_name = user_input.split("movie")[-1].strip()
            response = get_movie_info(movie_name)

        elif intent == "recommendation":
            response = get_recommendations(user_input)

        elif intent == "greeting":
            response = "Hello! 😊 How can I assist you today?"

        elif intent == "goodbye":
            response = "Goodbye! See you next time!"

        else:
            try:
                openai_response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful chatbot."},
                        {"role": "user", "content": user_input}
                    ],
                    max_tokens=150,
                    temperature=0.7
                )
                response = openai_response.choices[0].message.content.strip()
            except Exception as e:
                response = f"Error occurred: {e}"

        # ✅ store in DB, but not used for history
        ConversationHistory.objects.create(
            user_input=user_input,
            bot_response=response
        )

        return JsonResponse({"response": response})

    return JsonResponse({"error": "Invalid method. Use POST."}, status=405)

def index(request):
    return render(request, 'chatbot_app/chatbot.html')
