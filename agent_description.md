# Self-Ask with Search Agent

A reasoning agent that breaks down complex questions into simpler sub-questions and uses search capabilities to find intermediate answers before arriving at a final conclusion.

## Overview

This agent implements the "self-ask with search" methodology, where it:
1. Analyzes whether a question requires follow-up questions
2. Generates relevant follow-up questions
3. Searches for intermediate answers
4. Synthesizes the information to provide a final answer

## Key Features

- **Multi-step Reasoning**: Automatically decomposes complex queries into manageable sub-questions
- **Search Integration**: Uses external search tools to find factual information
- **Chain-of-Thought**: Shows its reasoning process through intermediate steps
- **Flexible Search Backend**: Supports Google Serper, SearchAPI, or SerpAPI

## Example Use Cases

- Comparative questions (e.g., "Who lived longer, Muhammad Ali or Alan Turing?")
- Multi-hop queries (e.g., "Who was the maternal grandfather of George Washington?")
- Fact-checking and verification tasks
- Questions requiring multiple pieces of information

## Inputs

- **Medium**: HTTP POST request to `/run` endpoint
- **Format**: JSON object with:
  - `input` (string, required): The question or query to process
  - `chat_history` (array, optional): Previous conversation context

## Outputs

- **Medium**: HTTP response
- **Format**: JSON object containing:
  - `status`: "success" or "error"
  - `output`: The final answer with reasoning steps shown
  - `message`: Error details (only on failure)

## Additional Endpoints

- `GET /`: Health check endpoint
- `GET /tools`: Returns list of available search tools