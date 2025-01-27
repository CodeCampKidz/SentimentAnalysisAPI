# Sentiment Analysis API

## Overview
Sentiment Analysis API is a Python-based FastAPI application for performing sentiment analysis on text. It leverages the Hugging Face `transformers` library and connects to MongoDB Atlas for storing and retrieving sentiment analysis records.

## Public endpoints
POST /analyze  
Request Model: 
{
    "text": "awesome"
}  
Response Model: 
{
    "sentiment": "positive", 
    "score": 0.9998708963394165
}
  
GET /recent  
Response Model: 
[
  {
    "date": "2025-01-27T16:25:43.168000",
    "text": "Awesome it works v3!",
    "sentiment": "positive",
    "score": 0.9998708963394165
  },
]

## Features
<ul>
<li>FastAPI endpoints</li>
<li>FastAPI startup event</li>
<li>FastAPI background tasks</li>
<li>Pydantic request / response models with validation</li>
<li>Bearer token support with validation</li>
<li>Trace logging</li>
<li>Try / catch error handling</li>
<li>Transformers sentiment analysis</li>
<li>MongoDB Atlas storage</li>
<li>Unittests for endpoints and sentiment model</li>
<li>Docker containerization with uittests</li>
<li>Github Actions that trigger unittests on PR</li>
</ul>

## 1. Installing the app
<ol>
<li>Make a directory for the project.</li>
<li>clone the repository from the command prompt: "git clone https://github.com/CodeCampKidz/SentimentAnalysisAPI.git"</li>
<li>go into the SentimentAnalysisAPI directory: "cd SentimentAnalysisAPI"</li>
<li>setup the virtual environment: "python -m venv venv"</li>
<li>activate the environment: "venv\Scripts\activate"</li>
<li>update pip: "pip install --upgrade pip"</li>
<li>install requirements: "pip install --only-binary :all: -r requirements.txt"</li>
</ol>

## 2. Creating the local .env file
<ol>
<li>Create a .env file at the root of the project at the same level as .env.example.</li>
<li>Copy the key/value pairs from .env.example to the new .env file.</li>
<li>Get the key values for MONGODB_URI, MONGODB_DATABASE, MONGODB_COLLECTION & BEARER_TOKEN from an administrator.</li>

</ol>

## 3a. Running with Uvicorn
<ol>
<li>run endpoint & unit tests: "python -m unittest discover -s tests"</li>
<li>run with uvicorn on port 8000: "uvicorn main:app --reload"</li>
</ol>

## 3b. Running with Docker
<ol>
<li>build the container image: "docker build --no-cache -t sentiment-analysis-api ."</li>
Note: building the container image will automaticaly trigger unittests.
<li>run the container image on port 8000: "docker run -p 8000:8000 sentiment-analysis-api"</li>
</ol>

## 4. Calling the APIs
<ol>
<li>Once the app is running with either Uvicorn or Docker, navigate to the Swagger API documentation for manual testing: "http://127.0.0.1:8000/docs"<br>Note: You will need the bearer token to execute the API calls. This is the same bearer token from the .env file.</li>
</ol>
