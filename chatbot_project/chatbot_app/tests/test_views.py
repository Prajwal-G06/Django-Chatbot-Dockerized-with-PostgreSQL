# chatbot_app/tests/test_views.py
from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import json

class ChatbotTests(TestCase):

    @patch('chatbot_app.views.openai.Completion.create')  # Mocking OpenAI API call
    def test_chatbot_response(self, mock_openai):
        # Simulate OpenAI response
        mock_openai.return_value = {
            "choices": [{"text": "Hello, how can I assist you?"}]
        }

        # Simulate sending a POST request with user input
        response = self.client.post(reverse('chatbot'), {'user_input': 'Hello'})
        
        # Check that the response is valid and contains expected output
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
        self.assertEqual(response.json()['response'], "Hello, how can I assist you?")

    def test_invalid_method(self):
        """Test that non-POST requests return 405 Method Not Allowed"""
        response = self.client.get(reverse('chatbot'))
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response.json()['error'], "Invalid method. Use POST.")

    @patch('chatbot_app.views.get_movie_info')
    def test_movie_info(self, mock_get_movie_info):
        # Simulate movie information response
        mock_get_movie_info.return_value = "Title: Test Movie\nYear: 2021\nGenre: Action\nPlot: A test movie."

        # Simulate sending a POST request with a movie query
        response = self.client.post(reverse('chatbot'), {'user_input': 'Tell me about the movie Test Movie'})

        # Check that the response contains the movie info
        self.assertEqual(response.status_code, 200)
        self.assertIn('response', response.json())
        self.assertEqual(response.json()['response'], "Title: Test Movie\nYear: 2021\nGenre: Action\nPlot: A test movie.")
