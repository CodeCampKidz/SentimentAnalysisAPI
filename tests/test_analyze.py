from fastapi.testclient import TestClient
from main import app
from modules.sentiment import SentimentAnalyzer
import logging
import os
import unittest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up TestClient
client = TestClient(app)

# Set bearer tokens for testing
BEARER_TOKEN = os.getenv("BEARER_TOKEN", "")
HEADERS_VALID = {"Authorization": f"Bearer {BEARER_TOKEN}"}
HEADERS_INVALID = {"Authorization": "Bearer invalid-token"}


class TestAnalyzeEndpoint(unittest.TestCase):
    """
    Test cases for the /analyze endpoint in the FastAPI application.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up resources needed for all tests in this class.
        Initialize the SentimentAnalyzer instance.
        """
        cls.sentiment_analyzer = SentimentAnalyzer()

    def test_analyze_negative_cases(self):
        """
        Test /analyze endpoint with invalid inputs.
        Ensures the API returns a 422 status code for invalid input text.
        """
        cases = [
            ("", 422),  # Test empty input
            ("   ", 422),  # Test whitespace-only input
            ("a" * 1001, 422),  # Test input exceeding max length
            ("</>,{}", 422),  # Test input with invalid characters
        ]
        url = "/analyze"
        for text, expected_status in cases:
            with self.subTest(text=text):
                logger.info(f"Testing URL: {url} with text: {text}")
                response = client.post(url, headers=HEADERS_VALID, json={"text": text})
                logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
                self.assertEqual(response.status_code, expected_status)

    def test_analyze_happy_path(self):
        """
        Test /analyze endpoint with valid input.
        Ensures the API returns a valid sentiment analysis response.
        """
        url = "/analyze"
        test_text = "What an amazing experience"
        logger.info(f"Testing URL: {url} with valid text input: {test_text}")

        # Send POST request to the /analyze endpoint
        response = client.post(url, headers=HEADERS_VALID, json={"text": test_text})

        # Log response details
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")

        # Validate response status code
        self.assertEqual(response.status_code, 200)

        # Parse the JSON response
        response_data = response.json()

        # Validate the response schema and values
        self.assertIn("sentiment", response_data, "Response is missing 'sentiment'")
        self.assertIn("score", response_data, "Response is missing 'score'")
        self.assertIsInstance(response_data["sentiment"], str, "'sentiment' should be a string")
        self.assertIsInstance(response_data["score"], float, "'score' should be a float")

        # Verify sentiment and score
        self.assertIn(
            response_data["sentiment"], ["positive", "negative"],
            f"Unexpected sentiment value: {response_data['sentiment']}"
        )
        self.assertGreaterEqual(
            response_data["score"], 0.5,
            f"Score too low: {response_data['score']}"
        )

        # Log response data
        logger.info(f"Verified response: {response_data}")

    def test_analyze_missing_bearer_token(self):
        """
        Test /analyze endpoint without a bearer token.
        Ensures the API returns a 403 status code when the bearer token is missing.
        """
        url = "/analyze"
        response = client.post(url, json={"text": "This is a valid test text."})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 403)

    def test_analyze_invalid_bearer_token(self):
        """
        Test /analyze endpoint with an invalid bearer token.
        Ensures the API returns a 401 status code when the bearer token is invalid.
        """
        url = "/analyze"
        response = client.post(url, headers=HEADERS_INVALID, json={"text": "This is a valid test text."})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 401)
