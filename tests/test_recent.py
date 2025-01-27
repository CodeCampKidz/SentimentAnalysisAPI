from fastapi.testclient import TestClient
from main import app
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


class TestRecentEndpoint(unittest.TestCase):
    """
    Test cases for the /recent endpoint in the FastAPI application.
    """

    def test_recent_below_min(self):
        """Test /recent with numberOfResults below the minimum."""
        response = client.get("/recent", headers=HEADERS_VALID, params={"numberOfResults": 0})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        self.assertIn("numberOfResults must be at least", response.text)

    def test_recent_above_max(self):
        """Test /recent with numberOfResults above the maximum."""
        response = client.get("/recent", headers=HEADERS_VALID, params={"numberOfResults": 101})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        self.assertIn("numberOfResults must not exceed", response.text)

    def test_recent_not_a_number(self):
        """Test /recent with numberOfResults not a number."""
        response = client.get("/recent", headers=HEADERS_VALID, params={"numberOfResults": "Z"})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 422) # Unprocessable Entity
        self.assertIn("Input should be a valid integer", response.text)

    def test_recent_missing_bearer_token(self):
        """Test /recent endpoint without a bearer token."""
        response = client.get("/recent", params={"numberOfResults": 5})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 403)  # Forbidden

    def test_recent_invalid_bearer_token(self):
        """Test /recent endpoint with an invalid bearer token."""
        url = "/recent"
        response = client.get(url, headers=HEADERS_INVALID, params={"numberOfResults": 5})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 401)  # Unauthorized

    def test_recent_happy_path(self):
        """Test /recent endpoint with valid input."""
        url = "/recent"
        logger.info(f"Testing URL: {url} with valid input")
        response = client.get(url, headers=HEADERS_VALID, params={"numberOfResults": 3})
        logger.info(f"Response status: {response.status_code}, Response body: {response.text}")
        self.assertEqual(response.status_code, 200) # OK
        response_data = response.json()
        self.assertEqual(len(response_data), 3)
        self.assertTrue(
            all(
                "date" in item and "text" in item and "sentiment" in item and "score" in item
                for item in response_data
            )
        )
