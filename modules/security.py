from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
import os

# Load environment variables
load_dotenv()

# TRACE_LOG is enabled if the TRACE_LOG environment variable is set to "true" or "1"
TRACE_LOG = os.getenv("TRACE_LOG", "False").lower() in ("true", "1")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BearerTokenValidator:
    """
    A class to handle Bearer token validation.
    """

    def __init__(self):
        """
        Initialize the BearerTokenValidator with security and expected token.
        """
        self.security = HTTPBearer()
        self.expected_token = os.getenv("BEARER_TOKEN")

        if not self.expected_token:
            logger.error("BEARER_TOKEN is not set in the environment variables.")
            raise RuntimeError("Server configuration error: BEARER_TOKEN not set")

    def validate_token(self, credentials: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> str:
        """
        Validates the Bearer token provided in the Authorization header.

        Args:
            credentials (HTTPAuthorizationCredentials): The credentials provided in the request, containing the scheme
                and token.

        Returns:
            str: The validated Bearer token.

        Raises:
            HTTPException: If the Bearer token is missing, invalid, or does not match the expected value.
        """
        if TRACE_LOG:
            logger.info("Starting token validation.")

        # Set the token
        token = credentials.credentials

        if TRACE_LOG:
            logger.info(f"The token passed in: {token}")

        # Validate the token
        if token != self.expected_token:
            if TRACE_LOG:
                logger.error(f"Invalid bearer token provided: {token}")
            raise HTTPException(status_code=401, detail="Invalid bearer token")

        if TRACE_LOG:
            logger.info("Bearer token successfully validated.")

        return token
