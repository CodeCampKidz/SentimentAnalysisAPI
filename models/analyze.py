from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
import os

# Constants loaded from environment variables with default values
MIN_TEXT_LENGTH = int(os.getenv("MIN_TEXT_LENGTH", 1))  # Minimum allowed text length
MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", 1000))  # Maximum allowed text length


class AnalyzeRequest(BaseModel):
    """
    Request model for analyzing sentiment in text.
    """
    text: str = Field(
        ...,
        pattern=r"^[a-zA-Z0-9\s.,!?'-]+$",  # Restrict input to alphanumeric and common punctuation
        min_length=MIN_TEXT_LENGTH,
        max_length=MAX_TEXT_LENGTH,
        description="Text to analyze",
        example="What an amazing experience!",
    )

    @field_validator("text")
    def prevent_repetitive_patterns(cls, value: str) -> str:
        """
        Validate that the text does not contain excessive repetitive patterns.

        Args:
            value (str): The input text.

        Returns:
            str: The validated text.

        Raises:
            HTTPException: If the text contains repetitive patterns.
        """
        if len(set(value)) < 5 and len(value) > MIN_TEXT_LENGTH * 5:
            raise HTTPException(
                status_code=422,  # Unprocessable Entity
                detail={
                    "loc": ["text"],
                    "msg": "Input text appears to contain repetitive patterns.",
                    "type": "value_error.repetitive_pattern",
                },
            )
        return value

    @field_validator("text")
    def sanitize_text(cls, value: str) -> str:
        """
        Normalize text by stripping whitespace and ensuring it's not empty.

        Args:
            value (str): The input text.

        Returns:
            str: The sanitized text.

        Raises:
            HTTPException: If the text is empty or whitespace only.
        """
        sanitized = value.strip().replace("\n", " ").replace("\r", "")
        if not sanitized:
            raise HTTPException(
                status_code=422,  # Unprocessable Entity
                detail={
                    "loc": ["text"],
                    "msg": "Input text cannot be empty or whitespace only.",
                    "type": "value_error.empty_text",
                },
            )
        return sanitized


class AnalyzeResponse(BaseModel):
    """
    Response model for the sentiment analysis results.
    """
    sentiment: Literal["positive", "negative"]
    score: float


class SentimentRecord(BaseModel):
    """
    Storage model for saving sentiment analysis records in a database.
    """
    text: str = Field(..., description="The input text analyzed for sentiment.")
    sentiment: str = Field(..., description="The sentiment label (positive or negative).")
    score: float = Field(..., description="The confidence score for the sentiment.")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="The timestamp of the analysis."
    )
