from fastapi import HTTPException, BackgroundTasks
from models.analyze import SentimentRecord, AnalyzeRequest, AnalyzeResponse
from models.recent import RecentRequest, RecentResponse
from modules.mongodb import MongoDBHandler
from transformers import pipeline, Pipeline
from typing import Optional, List
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TRACE_LOG is enabled if the TRACE_LOG environment variable is set to "true" or "1"
TRACE_LOG = os.getenv("TRACE_LOG", "False").lower() in ("true", "1")


class SentimentAnalyzer:
    """
    A service class for managing sentiment analysis and MongoDB operations.
    """

    def __init__(self):
        """
        Initialize the sentiment analysis pipeline and MongoDB handler.
        """
        self.sentiment_analyzer: Optional[Pipeline] = None
        self.mongo_handler = MongoDBHandler()
        self._initialize_pipeline()

    def _initialize_pipeline(self):
        """
        Initialize the sentiment analysis pipeline.
        This is intended to be called during service initialization.
        """
        try:
            if TRACE_LOG:
                logger.info("Initializing sentiment analysis pipeline...")

            # Specify the model and revision explicitly
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="distilbert-base-uncased-finetuned-sst-2-english",
                revision="af0f99b"
            )

            if TRACE_LOG:
                logger.info("Sentiment analysis pipeline loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize sentiment analysis pipeline: {e}")
            raise RuntimeError(f"Pipeline initialization failed: {e}")

    def store_sentiment_record_async(self, record: SentimentRecord):
        """
        Store the sentiment record asynchronously in MongoDB.

        Args:
            record (SentimentRecord): The sentiment record to store.
        """
        try:
            if TRACE_LOG:
                logger.info(f"Storing sentiment record asynchronously: {record}")

            self.mongo_handler.store_sentiment_record(record)

            if TRACE_LOG:
                logger.info("Sentiment record stored successfully.")
        except Exception as e:
            logger.error(f"Failed to store sentiment record asynchronously: {e}")

    def analyze_text(
        self, request: AnalyzeRequest, background_tasks: BackgroundTasks
    ) -> AnalyzeResponse:
        """
        Perform sentiment analysis on the given input text.

        Args:
            request (AnalyzeRequest): Input containing the text to analyze.
            background_tasks (BackgroundTasks): FastAPI background task manager.

        Returns:
            AnalyzeResponse: The sentiment and confidence score for the input text.

        Raises:
            HTTPException: If the pipeline is not initialized.
        """
        try:
            if TRACE_LOG:
                logger.info(f"Analyze method started with request data: {request}")

            # Check if the pipeline is initialized
            if self.sentiment_analyzer is None:
                logger.error("Sentiment analysis pipeline is not initialized.")
                raise HTTPException(
                    status_code=500,
                    detail="Sentiment analysis pipeline is not initialized.",
                )

            # Perform sentiment analysis
            result = self.sentiment_analyzer(request.text)[0]
            sentiment = result["label"].lower()  # Convert label to lowercase
            score = result["score"]  # Extract confidence score

            if TRACE_LOG:
                logger.info(f"Sentiment analysis result: {result}")

            # Create the sentiment record
            sentiment_record = SentimentRecord(
                text=request.text, sentiment=sentiment, score=score
            )

            # Add MongoDB storage to the background tasks
            background_tasks.add_task(self.store_sentiment_record_async, sentiment_record)

            # Create response
            response = AnalyzeResponse(sentiment=sentiment, score=score)

            if TRACE_LOG:
                logger.info(f"Analyze method completed with response data: {response}")

            return response
        except ValueError as ve:
            if TRACE_LOG:
                logger.error(
                    f"ValueError in /analyze endpoint. Request: {str(request)}, Error: {str(ve)}"
                )
            raise HTTPException(status_code=422, detail=str(ve))
        except Exception as e:
            logger.error(f"An unexpected error occurred in analyze_text: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}",
            )

    def get_sentiment_records(self, request: RecentRequest) -> List[RecentResponse]:
        """
        Retrieve the most recent sentiment records from MongoDB.

        Args:
            request (RecentRequest): Input containing the number of results to retrieve.

        Returns:
            List[RecentResponse]: A list of the most recent sentiment records.
        """
        try:
            if TRACE_LOG:
                logger.info(f"GetSentimentRecords method started with request data: {request}")

            # Retrieve records from MongoDB
            records = self.mongo_handler.get_sentiment_records(request)

            # Convert to RecentResponse list
            response = [
                RecentResponse(
                    date=record.date,
                    text=record.text,
                    sentiment=record.sentiment,
                    score=record.score,
                )
                for record in records
            ]

            if TRACE_LOG:
                logger.info(f"GetSentimentRecords method completed with response data: {response}")

            return response
        except Exception as e:
            logger.error(f"An unexpected error occurred in get_sentiment_records: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {str(e)}",
            )
