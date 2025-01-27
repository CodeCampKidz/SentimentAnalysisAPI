from datetime import datetime
from dotenv import load_dotenv
from fastapi import HTTPException
from pydantic import BaseModel, Field, field_validator
import os

# Load environment variables
load_dotenv()

# Constants loaded from .env
DEFAULT_NUMBER_OF_RESULTS = int(os.getenv("DEFAULT_NUMBER_OF_RESULTS", 5))  # Default results
MIN_NUMBER_OF_RESULTS = int(os.getenv("MIN_NUMBER_OF_RESULTS", 1))  # Minimum results
MAX_NUMBER_OF_RESULTS = int(os.getenv("MAX_NUMBER_OF_RESULTS", 100))  # Maximum results


class RecentRequest(BaseModel):
    """
    Model for handling requests to retrieve recent sentiment analysis results.
    """
    numberOfResults: int = Field(
        default=DEFAULT_NUMBER_OF_RESULTS,
        description="Number of recent results to return",
    )

    @field_validator("numberOfResults")
    def validate_number_of_results(cls, value: int) -> int:
        """
        Validate that numberOfResults is within the acceptable range.

        Args:
            value (int): The number of results requested.

        Returns:
            int: The validated number of results.

        Raises:
            HTTPException: If the value is out of the defined range.
        """
        if value < MIN_NUMBER_OF_RESULTS:
            raise HTTPException(
                status_code=422,  # Unprocessable Entity
                detail={
                    "loc": ["numberOfResults"],
                    "msg": f"numberOfResults must be at least {MIN_NUMBER_OF_RESULTS}",
                    "type": "value_error",
                },
            )
        if value > MAX_NUMBER_OF_RESULTS:
            raise HTTPException(
                status_code=422,  # Unprocessable Entity
                detail={
                    "loc": ["numberOfResults"],
                    "msg": f"numberOfResults must not exceed {MAX_NUMBER_OF_RESULTS}",
                    "type": "value_error",
                },
            )
        return value


class RecentResponse(BaseModel):
    """
    Model for responses containing recent sentiment analysis results.
    """
    date: datetime
    text: str
    sentiment: str
    score: float
