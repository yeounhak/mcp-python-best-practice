#!/bin/bash

# Anthropic Claude API curl script
# Replace YOUR_API_KEY with your actual Anthropic API key

API_KEY="sk-ant-..."
MODEL="claude-3-5-sonnet-20241022"

curl -X POST \
  https://api.anthropic.com/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "'$MODEL'",
    "max_tokens": 1024,
    "messages": [
      {
        "role": "user",
        "content": "hi"
      }
    ],
    "stream": true
  }' \
  --no-buffer