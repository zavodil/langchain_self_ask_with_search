# Self-Ask with Search Agent

A question-answering agent that uses a self-ask approach with search capabilities to break down complex questions into simpler sub-questions and find answers iteratively.

## Overview

This agent implements the self-ask-with-search methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

The agent is particularly effective for questions that require multiple steps of reasoning or gathering information from different sources.

## Key Features

- **Iterative Question Decomposition**: Automatically breaks down complex questions into manageable sub-questions
- **Search Integration**: Uses a search tool to find intermediate answers
- **Chain-of-Thought Reasoning**: Shows the reasoning process through follow-up questions and intermediate answers
- **Single Tool Focus**: Designed to work with exactly one search tool named "Intermediate Answer"

## Inputs

- **HTTP POST /run**
  - `input` (string, required): The question or query to be answered
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **HTTP Response**
  - `status`: "success" or "error"
  - `output`: The final answer after processing all follow-up questions and intermediate answers
  - `message`: Error message (only when status is "error")

## Example Usage

The agent excels at answering questions like:
- "Who lived longer, Muhammad Ali or Alan Turing?"
- "When was the founder of craigslist born?"
- "Who was the maternal grandfather of George Washington?"
- "Are both the directors of Jaws and Casino Royale from the same country?"

## API Endpoints

- `POST /run` - Execute the agent with a question
- `GET /` - Health check endpoint
- `GET /tools` - List available tools for the agent