# Self-Ask with Search Agent

A question-answering agent that uses a self-referential prompting technique to break down complex questions into simpler sub-questions, then searches for intermediate answers to arrive at a final conclusion.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes if a question requires follow-up questions
2. Generates relevant sub-questions
3. Searches for intermediate answers
4. Combines the information to provide a final answer

## Key Features

- **Self-Referential Reasoning**: Automatically determines when follow-up questions are needed
- **Iterative Search**: Breaks down complex queries into manageable sub-questions
- **Chain-of-Thought**: Shows the reasoning process through intermediate steps
- **Single Tool Design**: Uses one search tool named "Intermediate Answer"

## Example Use Cases

- Comparing attributes of different entities (e.g., "Who lived longer, X or Y?")
- Finding information about relationships (e.g., "Who was the grandfather of X?")
- Verifying facts across multiple sources (e.g., "Are both directors from the same country?")
- Discovering dates and biographical information

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question to answer
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object with:
  - `status`: "success" or "error"
  - `output`: The final answer after self-ask reasoning
  - `message`: Error description (only on failure)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns the list of available tools (single search tool)