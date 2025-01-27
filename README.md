# Sentiment API

## Overview
Sentiment API is a Python-based FastAPI application for performing sentiment analysis on text. It leverages the Hugging Face `transformers` library and connects to MongoDB Atlas for storing and retrieving sentiment analysis records.

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
<li>Bearer token support with valiation</li>
<li>Trace logging</li>
<li>Try / catch error handling</li>
<li>Transformers sentiment analysis</li>
<li>MongoDB Atlas storage</li>
<li>Unittests for endpoints and sentiment model</li>
<li>Docker containerization</li>
</ul>

## How to set up

## How to call the APIs

## How to run tests
