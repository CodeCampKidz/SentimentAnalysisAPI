from fastapi import BackgroundTasks
from fastapi.exceptions import HTTPException
from models.analyze import AnalyzeRequest, AnalyzeResponse
from modules.sentiment import SentimentAnalyzer
from unittest.mock import Mock
import logging
import unittest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TestSentimentAnalyzer(unittest.TestCase):
    """
    Test cases for the Sentiment class in the FastAPI application.
    """

    @classmethod
    def setUpClass(cls):
        """
        Initialize the SentimentAnalyzer instance before running tests.
        """
        cls.sentiment_analyzer = SentimentAnalyzer()

    def test_1_pipeline_initialization(self):
        """
        Test that the pipeline is initialized properly.
        """
        self.assertIsNotNone(
            self.sentiment_analyzer.sentiment_analyzer,
            "Pipeline initialization failed or returned None.",
        )
        logger.info("Pipeline initialization verified successfully.")

    def test_2_positive_sentiment(self):
        """
        Test the pipeline with positive sentiment text.
        """
        request = AnalyzeRequest(text="This is an amazing experience!")
        background_tasks = Mock(spec=BackgroundTasks)  # Mock BackgroundTasks
        response: AnalyzeResponse = self.sentiment_analyzer.analyze_text(
            request, background_tasks
        )

        self.assertEqual(response.sentiment, "positive")
        self.assertGreater(response.score, 0.5)
        logger.info("Positive sentiment verified successfully.")

    def test_3_negative_sentiment(self):
        """
        Test the pipeline with negative sentiment text.
        """
        request = AnalyzeRequest(text="This is the worst experience ever.")
        background_tasks = Mock(spec=BackgroundTasks)  # Mock BackgroundTasks
        response: AnalyzeResponse = self.sentiment_analyzer.analyze_text(
            request, background_tasks
        )

        self.assertEqual(response.sentiment, "negative")
        self.assertGreater(response.score, 0.5)
        logger.info("Negative sentiment verified successfully.")

    def test_4_pipeline_not_initialized(self):
        """
        Test the behavior when the pipeline is not initialized.
        Expect an HTTPException with a 500 status code.
        """
        # Create a new SentimentAnalyzer instance without reinitializing the pipeline
        uninitialized_analyzer = SentimentAnalyzer()
        uninitialized_analyzer.sentiment_analyzer = None  # Force uninitialized state

        # Confirm pipeline is not initialized
        self.assertIsNone(uninitialized_analyzer.sentiment_analyzer)

        # Try calling analyze_text without initializing the pipeline
        request = AnalyzeRequest(
            text="This text will fail because the pipeline is not initialized."
        )
        background_tasks = Mock(spec=BackgroundTasks)  # Mock BackgroundTasks

        with self.assertRaises(HTTPException) as context:
            uninitialized_analyzer.analyze_text(request, background_tasks)

        exception = context.exception
        self.assertEqual(exception.status_code, 500)
        self.assertIn("Sentiment analysis pipeline is not initialized", exception.detail)
        logger.info("Verified behavior when pipeline is not initialized.")

    @classmethod
    def tearDownClass(cls):
        """
        Clean up resources after tests are done.
        """
        cls.sentiment_analyzer = None
        logger.info("Pipeline reset in tearDownClass.")
