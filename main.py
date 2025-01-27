from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from models.analyze import AnalyzeRequest, AnalyzeResponse
from models.recent import RecentRequest, RecentResponse
from modules.security import BearerTokenValidator
from modules.sentiment import SentimentAnalyzer
from typing import List
import logging
import os

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# TRACE_LOG is enabled if the TRACE_LOG environment variable is set to "true" or "1"
TRACE_LOG = os.getenv("TRACE_LOG", "False").lower() in ("true", "1")

# Create a FastAPI application instance
app = FastAPI()

# Instantiate the classes
sentiment_analyzer = SentimentAnalyzer()
token_validator = BearerTokenValidator()


@app.on_event("startup")
async def startup_event():
    """
    Event triggered on application startup.
    Initializes the sentiment analysis pipeline.
    """
    sentiment_analyzer._initialize_pipeline()


@app.post(
    "/analyze",
    response_model=AnalyzeResponse,
    dependencies=[Depends(token_validator.validate_token)],
    tags=["Sentiment Analysis API"]
)
async def analyze(
    request: AnalyzeRequest,
    background_tasks: BackgroundTasks
) -> AnalyzeResponse:
    """
    Analyze the sentiment of the provided text.

    Args:
        request (AnalyzeRequest): The input data containing the text to analyze.
        background_tasks (BackgroundTasks): FastAPI's background task manager.

    Returns:
        AnalyzeResponse: The analyzed sentiment and score.
    """
    try:
        if TRACE_LOG:
            logger.info(f"Analyze method started with request data: {request}")

        # Analyze the input for sentiment
        response = sentiment_analyzer.analyze_text(request, background_tasks)

        if TRACE_LOG:
            logger.info(f"Analyze method completed with response data: {response}")

        return response
    except Exception as e:
        logger.error(
            f"An error occurred in /analyze endpoint. "
            f"Request: {str(request)}, Error: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )


@app.get(
    "/recent",
    response_model=List[RecentResponse],
    dependencies=[Depends(token_validator.validate_token)],
    tags=["Sentiment Analysis API"]
)
async def recent(request: RecentRequest = Depends()) -> List[RecentResponse]:
    """
    Retrieve recent sentiment analysis results.

    Args:
        request (RecentRequest): The input data containing the number of results to retrieve. Defaults to 5.

    Returns:
        List[RecentResponse]: A list of recent sentiment analysis results.
    """
    try:
        if TRACE_LOG:
            logger.info(f"Recent method started with request data: {request}")

        # Retrieve recent results
        recent_results = sentiment_analyzer.get_sentiment_records(request)

        if TRACE_LOG:
            logger.info(f"Recent method completed with response data: {recent_results}")

        return recent_results
    except Exception as e:
        logger.error(
            f"An error occurred in /recent endpoint. "
            f"Request: {str(request)}, Error: {str(e)}"
        )
        raise HTTPException(
            status_code=500, detail=f"An error occurred: {str(e)}"
        )
