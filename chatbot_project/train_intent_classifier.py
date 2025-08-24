import joblib
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from joblib import Memory

# Preprocessing function to clean up text (removes punctuation and lowercases)
def preprocess_text(text):
    text = text.lower()  # Make text lowercase
    text = ''.join([char for char in text if char not in string.punctuation])  # Remove punctuation
    return text

# Expanded training data with more diverse examples
examples = [
    ("Tell me about Inception", "movie_info"),
    ("What is the plot of The Matrix?", "movie_info"),
    ("Who starred in Titanic?", "movie_info"),
    ("When was The Godfather released?", "movie_info"),
    ("Hi", "greeting"),
    ("Hello", "greeting"),
    ("Hey there", "greeting"),
    ("Bye", "goodbye"),
    ("See you later", "goodbye"),
    ("Can you recommend a movie?", "recommendation"),
    ("Suggest something like Inception", "recommendation"),
    ("What movies are similar to Inception?", "recommendation"),
    ("Who directed Inception?", "followup_info"),
    ("What’s the genre of The Matrix?", "followup_info"),
    ("Tell me about the cast of Interstellar", "followup_info"),
    ("I want to know about the budget of The Dark Knight", "followup_info"),
    ("What’s the weather", "general_chat"),
    ("How are you?", "general_chat"),
    ("What’s your favorite color?", "general_chat"),
    ("Can you help me with programming?", "general_chat"),
    # You can add more examples for each intent
    ("Tell me about The Dark Knight", "movie_info"),
    ("Who was the director of Titanic?", "followup_info"),
    ("What is the genre of The Dark Knight?", "followup_info"),
    ("Do you have any movie recommendations?", "recommendation"),
    ("What’s up?", "general_chat"),
    ("What's your name?", "general_chat")
]

# Preprocess the examples
X = [preprocess_text(text) for text, label in examples]
y = [label for text, label in examples]

# Set up memory caching for the pipeline
memory = Memory("./cachedir", verbose=0)

# Build the pipeline (using TfidfVectorizer and LogisticRegression)
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', LogisticRegression(random_state=42))  # Set random_state for reproducibility
], memory=memory)

# Train the model
pipeline.fit(X, y)

# Save the trained model to a file
joblib.dump(pipeline, 'intent_classifier.pkl')

print("✅ Intent classifier trained and saved!")
