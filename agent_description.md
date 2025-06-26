# Self-Ask with Search Agent

A LangChain-based agent that implements the self-ask-with-search methodology for answering complex questions by breaking them down into simpler sub-questions.

## Overview

This agent uses a unique approach where it:
1. Analyzes if a question requires follow-up questions to answer properly
2. Generates relevant follow-up questions
3. Searches for intermediate answers to each follow-up question
4. Synthesizes the intermediate answers to provide a final answer

The agent is particularly effective for questions that require multiple steps of reasoning or gathering information from different sources.

## Key Features

- **Automatic Question Decomposition**: Breaks complex questions into simpler, answerable sub-questions
- **Iterative Search**: Uses a search tool to find intermediate answers for each sub-question
- **Chain-of-Thought Reasoning**: Shows the reasoning process through follow-up questions and intermediate answers
- **Single Tool Design**: Works with exactly one search tool named "Intermediate Answer"

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation history

Example:
json
{
  "input": "Who was the maternal grandfather of George Washington?",
  "chat_history": []
}


## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer (on success) or error message (on failure)

Example:
json
{
  "status": "success",
  "output": "Joseph Ball"
}


## API Endpoints

- `POST /run`: Execute the agent with a question
- `GET /`: Health check endpoint
- `GET /tools`: List available tools (returns the search tool configuration)

## Example Use Cases

- Answering comparative questions (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Finding specific historical information (e.g., "When was the founder of craigslist born?")
- Verifying facts across multiple entities (e.g., "Are both directors of Jaws and Casino Royale from the same country?")
- Tracing genealogical relationships (e.g., "Who was the maternal grandfather of George Washington?")