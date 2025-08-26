#!/bin/bash

# OpenAI GPT API curl script
# Replace YOUR_API_KEY with your actual OpenAI API key

OPENAI_API_KEY="sk-..."
MODEL="gpt-4"

curl -X POST \
  https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "model": "'$MODEL'",
    "messages": [
      {
        "role": "user",
        "content": "hi"
      }
    ],
    "stream": true
  }' \
  --no-buffer