from models.analyze import SentimentRecord
from models.recent import RecentRequest, RecentResponse
from pymongo import MongoClient, DESCENDING
from typing import List
import logging
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TRACE_LOG is enabled if the TRACE_LOG environment variable is set to "true" or "1"
TRACE_LOG = os.getenv("TRACE_LOG", "False").lower() in ("true", "1")


class MongoDBHandler:
    """
    A class to handle MongoDB connection and operations.
    """

    def __init__(self):
        """
        Initialize the MongoDB client and collection.
        """
        try:
            # MongoDB configuration
            self.mongo_uri = os.getenv("MONGODB_URI", "")
            self.database_name = os.getenv("MONGODB_DATABASE", "")
            self.collection_name = os.getenv("MONGODB_COLLECTION", "")

            if TRACE_LOG:
                logger.info(f"Connecting to MongoDB at {self.mongo_uri}")

            # Initialize MongoDB client and collection
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.database_name]
            self.collection = self.db[self.collection_name]

            if TRACE_LOG:
                logger.info("MongoDB connection established successfully.")

        except Exception as e:
            logger.error(f"Failed to initialize MongoDB: {e}")
            raise RuntimeError(f"Failed to initialize MongoDB: {e}")

    def store_sentiment_record(self, record: SentimentRecord) -> str:
        """
        Store a sentiment analysis record in MongoDB.

        Args:
            record (SentimentRecord): The data to be stored.

        Returns:
            str: The ID of the inserted document.
        """
        try:
            if TRACE_LOG:
                logger.info(f"Storing sentiment record in MongoDB: {record}")

            # Insert the record into the collection
            result = self.collection.insert_one(record.dict())

            return str(result.inserted_id)
        except Exception as e:
            logger.error(f"Failed to store sentiment record: {e}")
            raise RuntimeError(f"Database operation failed: {e}")

    def get_sentiment_records(self, request: RecentRequest) -> List[RecentResponse]:
        """
        Retrieve the most recent sentiment analysis records.

        Args:
            request (RecentRequest): The input containing the number of results to retrieve.

        Returns:
            List[RecentResponse]: A list of the most recent sentiment analysis records.
        """
        try:
            if TRACE_LOG:
                logger.info(f"Fetching the last {request.numberOfResults} sentiment records from MongoDB.")

            # Query the collection and retrieve the most recent records
            records_cursor = (
                self.collection.find()
                .sort("_id", DESCENDING)  # Sort by _id in descending order
                .limit(request.numberOfResults)  # Limit to the number of results requested
            )

            # Convert MongoDB records to a list of RecentResponse objects
            records = [
                RecentResponse(
                    date=record["timestamp"],
                    text=record["text"],
                    sentiment=record["sentiment"],
                    score=record["score"],
                )
                for record in records_cursor
            ]

            if TRACE_LOG:
                logger.info(f"Retrieved {len(records)} sentiment records.")

            return records
        except Exception as e:
            logger.error(f"Failed to retrieve sentiment records: {e}")
            raise RuntimeError(f"Database operation failed: {e}")
